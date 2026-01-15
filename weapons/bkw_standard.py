# bkw_standard.py - Version corrigée
import numpy as np
from core.utils import xor_vectors, hamming_weight, majority_vote

class BKWStandard:
    """Algorithme BKW Standard pour LPN - Version corrigée"""
    
    def __init__(self, params, log_callback=None):
        self.params = params
        self.log = log_callback or print
        self.a = params['a']
        self.b = params['b']
        self.k = params.get('k', 0)
    
    def solve(self, samples, true_secret=None):
        """Résout LPN avec BKW standard - RETOURNE TOUJOURS UN SECRET"""
        try:
            found_secret = [0] * self.k
            original_samples = [s.copy() for s in samples]
            
            self.log("="*60, 'info')
            self.log("🚀 DÉBUT DE LA RÉSOLUTION LPN AVEC BKW STANDARD", 'info')
            self.log(f"📊 Paramètres: k={self.k}, a={self.a}, b={self.b}", 'info')
            if true_secret is not None:
                self.log(f"🔑 Secret à retrouver: {''.join(map(str, true_secret))}", 'info')
            self.log("="*60, 'info')
            
            # Pour chaque bloc (de droite à gauche)
            for block in range(self.a, 0, -1):
                self.log(f"\n{'='*50}", 'info')
                self.log(f"🔷 BLOC {block}/{self.a} - Début du traitement", 'info')
                self.log(f"📐 Positions: {(block-1)*self.b} à {block*self.b}", 'info')
                
                # Phase 1: Réduction
                self.log(f"\n📉 PHASE 1: Réduction pour les blocs 1 à {block-1}", 'info')
                
                temp_samples = [s.copy() for s in original_samples]
                
                for step in range(1, block):
                    self.log(f"  Étape {step}: Réduction du bloc {step}", 'info')
                    temp_samples = self.reduce_block(temp_samples, step)
                    if not temp_samples:
                        self.log(f"  ⚠️ Plus d'échantillons après réduction!", 'warning')
                        break
                    self.log(f"    Résultat: {len(temp_samples)} échantillons", 'info')
                
                if not temp_samples:
                    self.log(f"  ❌ Impossible de continuer - pas d'échantillons", 'error')
                    break
                
                # Phase 2: Résolution
                self.log(f"\n🔍 PHASE 2: Résolution du bloc {block}", 'info')
                
                block_start = (block - 1) * self.b
                block_end = block * self.b
                
                block_secret = self.solve_block(temp_samples, block_start, block_end)
                
                if block_secret is None:
                    self.log(f"  ❌ Impossible de résoudre le bloc {block}", 'error')
                    block_secret = [0] * self.b
                
                # Stocker
                for i, val in enumerate(block_secret):
                    found_secret[block_start + i] = val
                
                # Vérifier la précision
                if true_secret is not None:
                    correct = sum(1 for i in range(len(block_secret)) 
                                 if block_secret[i] == true_secret[block_start + i])
                    
                    self.log(f"\n📊 RÉSULTAT DU BLOC {block}:", 'info')
                    self.log(f"  Secret trouvé: {''.join(map(str, block_secret))}", 
                            'success' if correct == self.b else 'info')
                    self.log(f"  Secret réel:   {''.join(map(str, true_secret[block_start:block_end]))}", 'info')
                    self.log(f"  Exactitude: {correct}/{self.b} bits corrects", 
                            'success' if correct == self.b else 'warning')
                
                # Phase 3: Substitution arrière
                if block > 1:
                    self.log(f"\n↩️ PHASE 3: Substitution arrière", 'info')
                    self.back_substitution(original_samples, found_secret, block_start, block_end)
                    self.log(f"✅ Substitution terminée", 'success')
            
            self.log(f"\n{'='*60}", 'info')
            self.log("🏁 RÉSOLUTION TERMINÉE", 'info')
            secret_str = ''.join(map(str, found_secret))
            self.log(f"🔑 Secret final trouvé: {secret_str}", 'info')
            
            if true_secret is not None:
                true_str = ''.join(map(str, true_secret))
                correct_total = sum(1 for i in range(self.k) if found_secret[i] == true_secret[i])
                accuracy = (correct_total / self.k) * 100
                self.log(f"📈 Précision globale: {correct_total}/{self.k} ({accuracy:.1f}%)", 
                        'success' if accuracy > 90 else 'warning')
            
            return found_secret
            
        except Exception as e:
            self.log(f"❌ Erreur dans solve(): {str(e)}", 'error')
            # Retourner un secret par défaut plutôt que None
            return [0] * self.k
    
    def reduce_block(self, samples, step):
        """Réduit un bloc par regroupement et XOR - Version robuste"""
        if not samples:
            return []
            
        block_start = (step - 1) * self.b
        block_end = step * self.b
        
        self.log(f"    Regroupement par bits {block_start}-{block_end-1}", 'info')
        
        groups = {}
        for sample in samples:
            v = sample['v']
            if len(v) <= block_end:
                continue
            key = tuple(v[block_start:block_end])
            
            if key not in groups:
                groups[key] = []
            groups[key].append(sample)
        
        self.log(f"    {len(groups)} groupes formés", 'info')
        
        # XOR dans chaque groupe
        reduced = []
        total_xor = 0
        
        for key, group in groups.items():
            if len(group) < 2:
                continue
            
            key_str = ''.join(str(x) for x in key)
            self.log(f"    Groupe '{key_str}': {len(group)} échantillons", 'info')
            
            # Prendre un représentant
            repr_sample = group[0]
            
            # XOR avec les autres
            for i, sample in enumerate(group[1:]):
                new_v = xor_vectors(sample['v'], repr_sample['v'])
                new_c = sample['c'] ^ repr_sample['c']
                reduced.append({'v': new_v, 'c': new_c})
                total_xor += 1
        
        self.log(f"    Total: {total_xor} opérations XOR", 'info')
        return reduced if reduced else []
    
    def solve_block(self, samples, start, end):
        """Résout un bloc par vote majoritaire - Version robuste"""
        if not samples:
            self.log(f"  ⚠️ Aucun échantillon pour la résolution", 'warning')
            return [0] * (end - start)
            
        block_size = end - start
        votes = [[] for _ in range(block_size)]
        
        self.log(f"  Filtrage des échantillons de poids de Hamming 1", 'info')
        
        # Filtrer échantillons de poids 1
        valid_samples = 0
        for sample in samples:
            v_block = sample['v'][start:end]
            hw = hamming_weight(v_block)
            
            if hw == 1:
                pos = v_block.index(1)
                votes[pos].append(sample['c'])
                valid_samples += 1
        
        self.log(f"  {valid_samples} échantillons valides trouvés", 'info')
        
        # Si aucun échantillon valide, essayer autre chose
        if valid_samples == 0:
            self.log(f"  ⚠️ Aucun échantillon de poids 1", 'warning')
            self.log(f"  🔍 Utilisation de tous les échantillons pour le vote...", 'info')
            
            # Utiliser tous les échantillons
            for sample in samples:
                v_block = sample['v'][start:end]
                for pos in range(block_size):
                    if v_block[pos] == 1:
                        votes[pos].append(sample['c'])
            
            # Compter combien de votes par position
            for pos in range(block_size):
                if votes[pos]:
                    self.log(f"    Position {pos}: {len(votes[pos])} votes", 'info')
        
        # Vote majoritaire
        block_secret = []
        for pos, pos_votes in enumerate(votes):
            if pos_votes:
                try:
                    majority = majority_vote(pos_votes)
                    block_secret.append(majority)
                    ones = pos_votes.count(1)
                    zeros = pos_votes.count(0)
                    self.log(f"    Position {pos}: majorité = {majority} (1:{ones}, 0:{zeros})", 
                            'success' if len(pos_votes) > 0 else 'info')
                except:
                    block_secret.append(0)
                    self.log(f"    Position {pos}: erreur de vote → 0 par défaut", 'warning')
            else:
                block_secret.append(0)
                self.log(f"    Position {pos}: aucun vote → 0 par défaut", 'warning')
        
        return block_secret
    
    def back_substitution(self, samples, secret, start, end):
        """Met à jour les échantillons avec le secret partiel"""
        updates = 0
        for sample in samples:
            old_c = sample['c']
            contribution = 0
            for i in range(start, end):
                contribution ^= (sample['v'][i] & secret[i])
            sample['c'] ^= contribution
            
            # Afficher quelques mises à jour
            if updates < 2 and old_c != sample['c']:
                v_str = ''.join(str(x) for x in sample['v'])
                self.log(f"    Mise à jour: v={v_str}", 'info')
                self.log(f"      c={old_c} ⊕ {contribution} = {sample['c']}", 'info')
                updates += 1