# hexa

> another hexastore implementation

A pure Python triple store / graph database implementation. The
implementation is based on
[this paper](http://karras.rutgers.edu/hexastore.pdf). This is a
project in its infancy, its usage is with risk and is mainly an
exploration for a more serious implementation.

## Installation

To install use pip:

	$ pip install hexa


Or clone the repo:

	$ git clone <...>
	$ python setup.py install

## API and Usage

```python
from hexa.hexastore import Hexastore

# create a new database
db = Hexastore()

# add a single triple
db.put(["hexastores", "are", "awesome"])

# add a collection of triples
db.putall([["hexastore", "is", "nice"],
		   ["hexastore", "speed", "fast"],
		   ["javascript", "is", "nice"]])


# add triples represented as dictionaries
db.addSPO({'hexastore': {'is': {'awesome': True, 'nice': True},
						 'speed': {'fast': True}},
		   'javascript': {'is': {'nice': True}}})

# or using
db.addSPO(...)
db.addSOP(...)
db.addOSP(...)
db.addOPS(...)
db.addPSO(...)
db.addPOS(...)

# import and export
db.import("mydatabase")    # import mydatabase.json
db.importNt("mydatabase")  # import mydatabase.nt

db.export("mydatabase")    # export mydatabase.json
db.exportNt("mydatabase")  # export mydatabase.json


# searching (stuff in list are to be bound variables)
result = db.search([ [["what"],"is","nice"]]);

# -> [{'what': 'hexastore'}, {'what': 'javascript'}]

# and since search result are only a list you can use
# map, filter and reduce to your hart delight.
```

## TODO

- [ ] Extend by implementing features from levelgraph

