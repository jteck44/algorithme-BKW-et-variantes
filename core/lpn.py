# lpn.py - Version modifiée
import numpy as np

class LPNInstance:
    """Génère une instance du problème Learning Parity with Noise"""
    
    def __init__(self, k, tau, secret=None):
        """
        k: dimension du secret
        tau: paramètre de bruit (probabilité qu'un bit soit inversé)
        secret: secret spécifique (optionnel)
        """
        self.k = k
        self.tau = tau
        
        if secret is not None:
            if len(secret) != k:
                raise ValueError(f"Le secret doit avoir {k} bits, mais a {len(secret)}")
            self.secret = secret.copy()
        else:
            self.secret = np.random.randint(0, 2, k).tolist()
    
    def generate_samples(self, n):
        """Génère n échantillons (v, c) où c = <v, s> ⊕ noise"""
        samples = []
        
        for _ in range(n):
            # Vecteur aléatoire
            v = np.random.randint(0, 2, self.k)
            
            # Produit scalaire modulo 2
            inner_product = np.dot(v, self.secret) % 2
            
            # Bruit de Bernoulli
            noise = 1 if np.random.random() < self.tau else 0
            
            # Valeur bruitée
            c = inner_product ^ noise
            
            samples.append({'v': v.tolist(), 'c': c})
        
        return samples
    
    def verify_sample(self, sample):
        """Vérifie si un échantillon est cohérent (pour debug)"""
        v = np.array(sample['v'])
        c = sample['c']
        expected = np.dot(v, self.secret) % 2
        return c == expected