from weapons.coded_bkw import CodedBKW
import numpy as np

class CodedBKWSieving(CodedBKW):
    """CODED-BKW avec Sieving (tamisage)"""
    
    def __init__(self, params, log_callback=None):
        super().__init__(params, log_callback)
        self.B = 5  # Borne pour la norme
        self.log("🎯 Mode Sieving: contrôle de norme activé", 'info')
    
    def coded_reduction_step(self, samples, step):
        """Réduction codée avec sieving"""
        # Étape CodeMap standard
        reduced = super().coded_reduction_step(samples, step)
        
        # Sieving: combiner pour réduire norme
        self.log(f"🎯 Sieving: filtrage par norme (B={self.B})", 'info')
        
        sieved = []
        for i, s1 in enumerate(reduced):
            norm1 = np.linalg.norm(s1['v'])
            
            if norm1 <= self.B * np.sqrt(len(s1['v'])):
                sieved.append(s1)
                continue
            
            # Chercher combinaison qui réduit norme
            found = False
            for s2 in reduced[i+1:]:
                new_v = [(s1['v'][j] - s2['v'][j]) % self.q 
                        for j in range(len(s1['v']))]
                new_norm = np.linalg.norm(new_v)
                
                if new_norm < norm1:
                    new_c = (s1['c'] - s2['c']) % self.q
                    sieved.append({'v': new_v, 'c': new_c})
                    found = True
                    break
            
            if not found and norm1 < self.B * np.sqrt(len(s1['v'])) * 2:
                sieved.append(s1)
        
        return sieved