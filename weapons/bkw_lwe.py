# bkw_lwe.py - Version améliorée
import numpy as np
from core.utils import mod_subtract, mod_add, hamming_weight, log_likelihood

class BKWLWE:
    """BKW adapté pour LWE - Version avec affichage détaillé"""
    
    def __init__(self, params, log_callback=None):
        self.params = params
        self.log = log_callback or print
        self.a = params['a']
        self.b = params['b']
        self.n = params['n']
        self.q = params['q']
        self.sigma = params['sigma']
        
        # Pour le suivi des étapes
        self.step_details = []
    
    def solve(self, samples, true_secret=None):
        """Résout LWE avec BKW - Version détaillée"""
        found_secret = [0] * self.n
        original_samples = [s.copy() for s in samples]
        
        self.log("="*60, 'info')
        self.log("🚀 DÉBUT DE LA RÉSOLUTION LWE AVEC BKW", 'info')
        self.log(f"📊 Paramètres: n={self.n}, q={self.q}, σ={self.sigma}, a={self.a}, b={self.b}", 'info')
        self.log(f"🔑 Secret à retrouver: {true_secret}", 'info')
        self.log("="*60, 'info')
        
        for block in range(self.a, 0, -1):
            self.log(f"\n{'='*50}", 'info')
            self.log(f"🔷 BLOC {block}/{self.a} - Début du traitement", 'info')
            self.log(f"📐 Bloc courant: positions {(block-1)*self.b} à {block*self.b}", 'info')
            
            # Phase 1: Réduction
            self.log(f"\n📉 PHASE 1: Réduction d'échantillons", 'info')
            self.log(f"Objectif: Annuler les blocs 1 à {block-1}", 'info')
            
            temp_samples = self.reduction_phase(original_samples, block)
            
            self.log(f"✅ Réduction terminée: {len(temp_samples)} échantillons réduits", 'success')
            self.log(f"📊 Échantillons après réduction:", 'info')
            for i, sample in enumerate(temp_samples[:3]):  # Montrer seulement 3 échantillons
                v_str = ','.join(str(x) for x in sample['v'])
                self.log(f"  Échantillon {i+1}: v=[{v_str}], c={sample['c']}", 'info')
            if len(temp_samples) > 3:
                self.log(f"  ... et {len(temp_samples)-3} autres", 'info')
            
            # Phase 2: Test d'hypothèse
            self.log(f"\n🔍 PHASE 2: Test d'hypothèse", 'info')
            self.log(f"Objectif: Trouver les {self.b} composantes du secret pour ce bloc", 'info')
            
            block_start = (block - 1) * self.b
            block_end = block * self.b
            
            block_secret = self.hypothesis_testing(temp_samples, block, block_start, block_end)
            
            # Stocker le résultat
            for i, val in enumerate(block_secret):
                found_secret[block_start + i] = val
            
            # Vérifier la précision
            if true_secret is not None:
                correct = sum(1 for i in range(len(block_secret))
                             if block_secret[i] == true_secret[block_start + i])
                
                self.log(f"\n📊 RÉSULTAT DU BLOC {block}:", 'info')
                self.log(f"  Secret trouvé: {block_secret}", 'info' if correct == self.b else 'warning')
                self.log(f"  Secret réel:   {true_secret[block_start:block_end]}", 'info')
                self.log(f"  Exactitude: {correct}/{self.b} composantes correctes", 
                        'success' if correct >= self.b - 1 else 'warning')
                
                # Expliquer les difficultés pour LWE
                if correct < self.b:
                    self.log(f"  ⚠️ Difficulté: LWE avec modulus q={self.q} est plus complexe que LPN", 'warning')
                    self.log(f"  💡 Le bruit gaussien σ={self.sigma} s'accumule lors des réductions", 'info')
                    self.log(f"  💡 La vraisemblance peut être moins discriminante avec grand q", 'info')
            
            # Phase 3: Substitution arrière
            if block > 1:
                self.log(f"\n↩️ PHASE 3: Substitution arrière", 'info')
                self.log(f"Objectif: Éliminer la contribution des bits connus", 'info')
                
                self.back_substitution(original_samples, found_secret, block_start, block_end)
                self.log(f"✅ Substitution terminée pour le bloc {block}", 'success')
        
        self.log(f"\n{'='*60}", 'info')
        self.log("🏁 RÉSOLUTION TERMINÉE", 'info')
        self.log(f"🔑 Secret final trouvé: {found_secret}", 'info')
        
        if true_secret is not None:
            correct_total = sum(1 for i in range(self.n) if found_secret[i] == true_secret[i])
            accuracy = (correct_total / self.n) * 100
            self.log(f"📈 Précision globale: {correct_total}/{self.n} ({accuracy:.1f}%)", 
                    'success' if accuracy > 70 else 'warning')
            
            # Explication finale sur les difficultés LWE
            if accuracy < 80:
                self.log(f"\n💡 EXPLICATION DES DIFFICULTÉS LWE:", 'info')
                self.log(f"  • Le modulus q={self.q} crée un espace de recherche plus grand", 'info')
                self.log(f"  • Le bruit gaussien σ={self.sigma} s'accumule exponentiellement", 'info')
                self.log(f"  • La phase de test d'hypothèse doit explorer q^{self.b} possibilités", 'info')
                self.log(f"  • Pour améliorer: augmenter les échantillons ou réduire le bruit", 'info')
        
        return found_secret
    
    def reduction_phase(self, samples, block_current):
        """Phase de réduction avec affichage détaillé"""
        temp_samples = [s.copy() for s in samples]
        
        for step in range(1, block_current):
            self.log(f"  Étape {step}/{block_current-1}: Réduction du bloc {step}", 'info')
            
            table = {}
            new_samples = []
            collisions = 0
            
            block_start = (step - 1) * self.b
            block_end = step * self.b
            
            for sample in temp_samples:
                v_block = tuple(sample['v'][block_start:block_end])
                
                # Vérifier si déjà zéro
                if all(x == 0 for x in v_block):
                    new_samples.append(sample)
                    continue
                
                # Chercher collision
                if v_block in table:
                    collisions += 1
                    other = table.pop(v_block)
                    new_v = mod_subtract(sample['v'], other['v'], self.q)
                    new_c = (sample['c'] - other['c']) % self.q
                    new_samples.append({'v': new_v, 'c': new_c})
                    
                    # Afficher quelques collisions
                    if collisions <= 2:
                        self.log(f"    Collision #{collisions}:", 'info')
                        self.log(f"      v1={sample['v'][block_start:block_end]}, c1={sample['c']}", 'info')
                        self.log(f"      v2={other['v'][block_start:block_end]}, c2={other['c']}", 'info')
                        self.log(f"      → v_new={new_v[block_start:block_end]}, c_new={new_c}", 'info')
                    
                else:
                    # Chercher opposé
                    v_neg = tuple((-x) % self.q for x in v_block)
                    if v_neg in table:
                        collisions += 1
                        other = table.pop(v_neg)
                        new_v = mod_add(sample['v'], other['v'], self.q)
                        new_c = (sample['c'] + other['c']) % self.q
                        new_samples.append({'v': new_v, 'c': new_c})
                    else:
                        table[v_block] = sample
            
            temp_samples = new_samples
            self.log(f"    Résultat: {collisions} collisions, {len(temp_samples)} échantillons restants", 'info')
        
        return temp_samples
    
    def hypothesis_testing(self, samples, block_current, start, end):
        """Test d'hypothèse avec affichage détaillé"""
        self.log(f"  Filtrage des échantillons (max {2} composantes non nulles)", 'info')
        
        d = 2  # Nombre max de composantes non nulles
        filtered = []
        
        for sample in samples:
            v_block = sample['v'][start:end]
            if hamming_weight(v_block) <= d:
                filtered.append(sample)
        
        self.log(f"  Échantillons après filtrage: {len(filtered)}/{len(samples)}", 'info')
        
        # Partitionner par motif
        partitions = {}
        for sample in filtered:
            v_block = sample['v'][start:end]
            pattern = tuple(1 if x != 0 else 0 for x in v_block)
            
            if pattern not in partitions:
                partitions[pattern] = []
            partitions[pattern].append(sample)
        
        self.log(f"  {len(partitions)} motifs différents trouvés", 'info')
        
        # Tester chaque partition
        block_secret = [0] * self.b
        steps = block_current - 1
        sigma_total = self.sigma * np.sqrt(2 ** steps)
        
        self.log(f"  Bruit accumulé: σ_total = {sigma_total:.3f} (σ_initial × √2^{steps})", 'info')
        
        for pattern, group in partitions.items():
            non_zero_pos = [i for i, p in enumerate(pattern) if p == 1]
            
            if not non_zero_pos:
                continue
            
            self.log(f"  Traitement du motif {pattern} ({len(non_zero_pos)} composantes non nulles)", 'info')
            self.log(f"    Positions non nulles: {non_zero_pos}", 'info')
            self.log(f"    Nombre d'échantillons: {len(group)}", 'info')
            
            # Test exhaustif limité
            best_score = -float('inf')
            best_candidate = [0] * len(non_zero_pos)
            
            # Limiter la recherche pour l'affichage
            search_range = min(self.q, 5)  # Réduit pour l'affichage
            
            self.log(f"    Exploration des candidats (0 à {search_range-1}):", 'info')
            
            for candidate in self.generate_candidates(len(non_zero_pos), search_range):
                score = 0
                
                for sample in group:
                    error = sample['c']
                    for j, pos in enumerate(non_zero_pos):
                        abs_pos = start + pos
                        error = (error - sample['v'][abs_pos] * candidate[j]) % self.q
                    
                    # Normaliser erreur
                    if error > self.q // 2:
                        error -= self.q
                    
                    score += log_likelihood(error, sigma_total, self.q)
                
                # Afficher quelques scores
                if np.random.random() < 0.1:  # Afficher 10% des candidats
                    self.log(f"      Candidat {candidate}: score={score:.2f}", 'info')
                
                if score > best_score:
                    best_score = score
                    best_candidate = candidate[:]
            
            self.log(f"    Meilleur candidat: {best_candidate} (score={best_score:.2f})", 'success')
            
            # Assigner
            for j, pos in enumerate(non_zero_pos):
                block_secret[pos] = best_candidate[j]
        
        return block_secret
    
    def generate_candidates(self, dim, max_val):
        """Génère tous les candidats possibles"""
        if dim == 0:
            yield []
            return
        
        for val in range(max_val):
            for rest in self.generate_candidates(dim - 1, max_val):
                yield [val] + rest
    
    def back_substitution(self, samples, secret, start, end):
        """Substitution arrière avec affichage"""
        updates = 0
        for sample in samples:
            contribution = 0
            for i in range(start, end):
                contribution = (contribution + sample['v'][i] * secret[i]) % self.q
            old_c = sample['c']
            sample['c'] = (sample['c'] - contribution) % self.q
            
            # Afficher quelques mises à jour
            if updates < 2 and old_c != sample['c']:
                self.log(f"    Mise à jour échantillon: c={old_c} → {sample['c']}", 'info')
                self.log(f"      Contribution éliminée: {contribution}", 'info')
                updates += 1