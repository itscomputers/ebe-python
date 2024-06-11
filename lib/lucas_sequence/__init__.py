#   lib/lucas_sequence/__init__.py
#   - module for lucas sequences

# ===========================================================
from .modular import (
    lucas_mod_gen,
    lucas_mod_by_index,
)

# ===========================================================
__all__ = [
    "lucas_mod_gen",
    "lucas_mod_by_index",
]
