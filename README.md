# hexastore

![](https://github.com/e-k-m/hexastore/workflows/main/badge.svg)

> another hexastore implementation

[Installation](#installation) | [Getting Up And Running](#getting-up-and-running) | [Examples](#examples) | [API](#api) | [See Also](#see-also)

An implementation of ["Sextuple Indexing for Semantic Web Data Management"
from C. Weiss et al.](http://people.csail.mit.edu/tdanford/6830papers/weiss-hexastore.pdf).
This is an implementation for fun only, hence may be used if really needed, else it is
adviced to use something more serious. The main feature are:

- Basic functionality to CRUD triples in the store.

## Installation

```bash
pip install hexastore
```

## Getting Up and Running

```bash
nox -l
```

## Examples

```python
import hexastore
store = hexastore.Hexastore()
store.insert(["hexastores", "are", "awesome"])
store.insert(["cats", "are", "awesome"])
result = store.search(subject="cats")
```

## API

For now `pydoc hexastore.Hexastore`.

## See Also

- See the original paper [here](http://people.csail.mit.edu/tdanford/6830papers/weiss-hexastore.pdf).

- Or for a more serious library, maybe use [this](https://github.com/RDFLib/rdflib).