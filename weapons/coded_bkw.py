import numpy as np
from weapons.bkw_lwe import BKWLWE

class CodedBKW(BKWLWE):
    """CODED-BKW: Utilise des codes linéaires"""
    
    def __init__(self, params, log_callback=None):
        super().__init__(params, log_callback)
        self.t1 = 1  # Étapes BKW standard
        self.t2 = 1  # Étapes codées
        self.log("📡 Mode CODED-BKW: codes linéaires activés", 'info')
    
    def reduction_phase(self, samples, block_current):
        """Réduction avec codes linéaires"""
        # Étapes BKW standard
        temp = samples
        for step in range(1, self.t1 + 1):
            if step < block_current:
                temp = super().reduction_phase(temp, step + 1)
        
        # Étapes codées
        for step in range(self.t1 + 1, self.t1 + self.t2 + 1):
            if step < block_current:
                temp = self.coded_reduction_step(temp, step)
        
        return temp
    
    def coded_reduction_step(self, samples, step):
        """Une étape de réduction codée"""
        n_i = self.b + 1  # Réduire plus de positions
        
        # Code linéaire simple (répétition)
        table = {}
        new_samples = []
        
        block_start = (step - 1) * self.b
        block_end = min(block_start + n_i, self.n)
        
        for sample in samples:
            v_block = sample['v'][block_start:block_end]
            
            # Mapper au mot de code le plus proche
            codeword = self.find_nearest_codeword(v_block)
            key = tuple(codeword)
            
            if key in table:
                other = table.pop(key)
                new_v = [(sample['v'][i] - other['v'][i]) % self.q 
                        for i in range(len(sample['v']))]
                new_c = (sample['c'] - other['c']) % self.q
                new_samples.append({'v': new_v, 'c': new_c})
            else:
                table[key] = sample
        
        return new_samples
    
    def find_nearest_codeword(self, v_block):
        """Trouve le mot de code le plus proche (code de répétition)"""
        if not v_block:
            return []
        
        # Valeur majoritaire
        avg = sum(v_block) / len(v_block)
        closest = min(range(self.q), key=lambda x: abs(x - avg))
        
        return [closest] * len(v_block)