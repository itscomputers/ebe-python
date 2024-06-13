#   lib/lucas_sequence/__init__.py
#   - module for lucas sequences

# ===========================================================
from .modular import (
    LucasSequence,
    LucasValue,
    lucas_mod_gen,
    lucas_mod_by_index,
    lucas_mod_double_index,
)

# ===========================================================
__all__ = [
    "LucasSequence",
    "LucasValue",
    "lucas_mod_gen",
    "lucas_mod_by_index",
    "lucas_mod_double_index",
]
