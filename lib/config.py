#   lib/config.py
# ===========================================================

DEFAULTS = {
    "pi_digits": 20,
    "sqrt_digits": 20,
    "decimal_digits": 20,
    "rho_seeds": [2, 3, 4, 6, 7, 8, 9],
    "minus_seeds": [2],
    "prime_base_max": 1000,
    "miller_rabin_witness_count": 40,
    "lucas_witness_pair_count": 10,
    "sieve_primes": [2, 3, 5, 7],
}


def default(category):
    return DEFAULTS[category]
