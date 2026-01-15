from weapons.bkw_lwe import BKWLWE

class LMSBKW(BKWLWE):
    """LMS-BKW: BKW avec réduction de modulus"""
    
    def __init__(self, params, log_callback=None):
        super().__init__(params, log_callback)
        self.p = self.q // 2  # Modulus réduit
        self.log(f"🔄 Réduction de modulus: q={self.q} → p={self.p}", 'info')
    
    def reduction_phase(self, samples, block_current):
        """Réduction avec conversion LMS"""
        # Convertir vers Z_p
        converted = []
        for sample in samples:
            v_p = [(v * self.p // self.q) % self.p for v in sample['v']]
            c_p = (sample['c'] * self.p // self.q) % self.p
            converted.append({'v': v_p, 'c': c_p, 'original': sample})
        
        # Réduction standard dans Z_p
        reduced = super().reduction_phase(converted, block_current)
        
        # Reconvertir vers Z_q
        result = []
        for sample in reduced:
            v_q = [(v * self.q // self.p) % self.q for v in sample['v']]
            c_q = (sample['c'] * self.q // self.p) % self.q
            result.append({'v': v_q, 'c': c_q})
        
        return result