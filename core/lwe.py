# lwe.py - Version modifiée
import numpy as np

class LWEInstance:
    """Génère une instance du problème Learning With Errors"""
    
    def __init__(self, n, q, sigma, secret=None):
        """
        n: dimension du secret
        q: modulus
        sigma: écart-type du bruit gaussien
        secret: secret spécifique (optionnel)
        """
        self.n = n
        self.q = q
        self.sigma = sigma
        
        if secret is not None:
            if len(secret) != n:
                raise ValueError(f"Le secret doit avoir {n} valeurs, mais a {len(secret)}")
            if not all(0 <= x < q for x in secret):
                raise ValueError(f"Toutes les valeurs du secret doivent être entre 0 et {q-1}")
            self.secret = secret.copy()
        else:
            self.secret = np.random.randint(0, q, n).tolist()
    
    def generate_samples(self, m):
        """Génère m échantillons (a, b) où b = <a, s> + e mod q"""
        samples = []
        
        for _ in range(m):
            # Vecteur aléatoire
            a = np.random.randint(0, self.q, self.n)
            
            # Produit scalaire
            inner_product = np.dot(a, self.secret) % self.q
            
            # Bruit gaussien discret
            noise = int(np.round(np.random.normal(0, self.sigma)))
            
            # Valeur bruitée
            b = (inner_product + noise) % self.q
            
            samples.append({'v': a.tolist(), 'c': b})
        
        return samples