import numpy as np
from math import exp, sqrt, pi, log

def hamming_weight(vector):
    """Calcule le poids de Hamming"""
    return sum(1 for x in vector if x != 0)

def xor_vectors(v1, v2):
    """XOR de deux vecteurs binaires"""
    return [a ^ b for a, b in zip(v1, v2)]

def mod_subtract(v1, v2, q):
    """Soustraction modulaire de deux vecteurs"""
    return [(a - b) % q for a, b in zip(v1, v2)]

def mod_add(v1, v2, q):
    """Addition modulaire de deux vecteurs"""
    return [(a + b) % q for a, b in zip(v1, v2)]

def gaussian_pdf(x, sigma, q):
    """Densité gaussienne discrète"""
    K = 3
    total = 0
    for k in range(-K, K+1):
        total += (1 / (sigma * sqrt(2 * pi))) * exp(-((x + k * q) ** 2) / (2 * sigma ** 2))
    return total

def log_likelihood(error, sigma, q):
    """Score de log-vraisemblance"""
    prob = gaussian_pdf(error, sigma, q)
    if prob < 1e-20:
        return -1000
    return log(prob * q)

def majority_vote(values):
    """Vote à la majorité"""
    return max(set(values), key=values.count)

def walsh_hadamard_transform(f):
    """Transformée de Walsh-Hadamard rapide"""
    n = len(f)
    if n == 1:
        return f
    
    h = n // 2
    f_even = walsh_hadamard_transform([f[i] for i in range(0, n, 2)])
    f_odd = walsh_hadamard_transform([f[i] for i in range(1, n, 2)])
    
    result = [0] * n
    for i in range(h):
        result[i] = f_even[i] + f_odd[i]
        result[i + h] = f_even[i] - f_odd[i]
    
    return result