"""
Another hexastore implementation.

An implementation of "Sextuple Indexing for Semantic Web Data Management"
from C. Weiss et al.. This is an implementation for fun only, hence may
be used if really needed, else it is adviced to use something more serious.

Example
-------
import hexastore
store = hexastore.Hexastore()
store.insert(["hexastores", "are", "awesome"])
store.insert(["cats", "are", "awesome"])
result = store.search(subject="cats");
"""

from hexastore import version
from hexastore import hexastore

Hexastore = hexastore.Hexastore
__author__ = "Eric Matti"
__version__ = version.__version__
__all__ = [Hexastore]
