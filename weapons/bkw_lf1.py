# bkw_lf1.py - Version corrigée
import numpy as np
from core.utils import walsh_hadamard_transform
from weapons.bkw_standard import BKWStandard

class BKWLF1(BKWStandard):
    """LF1: BKW avec transformée de Walsh-Hadamard - Version corrigée"""
    
    def solve_block(self, samples, start, end):
        """Résout avec Walsh-Hadamard au lieu de majorité"""
        self.log("✨ Application Walsh-Hadamard", 'info')
        
        if not samples:
            self.log("⚠️ Aucun échantillon pour Walsh-Hadamard", 'warning')
            return [0] * (end - start)
        
        block_size = end - start
        size = 2 ** block_size
        
        # Construire f(x)
        f = [0] * size
        sample_count = 0
        
        for sample in samples:
            try:
                v_block = sample['v'][start:end]
                
                # Convertir en index
                index = sum((v_block[i] << (block_size - 1 - i)) for i in range(block_size))
                
                # Ajouter contribution
                f[index] += (-1) ** sample['c']
                sample_count += 1
            except:
                continue
        
        if sample_count == 0:
            self.log("❌ Aucun échantillon valide pour Walsh-Hadamard", 'error')
            return [0] * block_size
        
        self.log(f"📊 {sample_count} échantillons utilisés pour la transformée", 'info')
        
        # Transformée
        try:
            f_hat = walsh_hadamard_transform(f)
            
            # Trouver maximum
            max_idx = max(range(size), key=lambda i: abs(f_hat[i]))
            max_val = abs(f_hat[max_idx])
            
            self.log(f"🎯 Maximum trouvé à l'index {max_idx} (valeur: {max_val:.2f})", 'info')
            
            # Convertir en bits
            block_secret = []
            for i in range(block_size - 1, -1, -1):
                block_secret.append((max_idx >> i) & 1)
            
            result = list(reversed(block_secret))
            self.log(f"🔑 Bloc trouvé: {result}", 'success')
            return result
            
        except Exception as e:
            self.log(f"❌ Erreur dans Walsh-Hadamard: {str(e)}", 'error')
            return [0] * block_size