from collections import abc
import json


def index_insert(index, s, p, o):
    if s not in index:
        index[s] = {}
    if p not in index[s]:
        index[s][p] = {}
    index[s][p][o] = None


def index_delete(index, s, p, o):
    if s in index and p in index[s] and o in index[s][p]:
        del index[s][p]
        del index[s]


def islist(e):
    return isinstance(e, list)


def ishashable(e):
    return isinstance(e, abc.Hashable)


def istriple(e):
    return (
        islist(e)
        and len(e) == 3
        and ishashable(e[0])
        and ishashable(e[1])
        and ishashable(e[2])
        and e[0] is not None
        and e[1] is not None
        and e[2] is not None
    )


class Hexastore(object):
    """
    Hexastore and utils.
    """

    def __init__(self):
        self._spo = {}
        self._sop = {}
        self._pso = {}
        self._pos = {}
        self._osp = {}
        self._ops = {}

        self._search_dispatch = {
            (False, False, False): lambda s, p, o: self.search_all(),
            (True, False, False): lambda s, p, o: self.search_subject(s),
            (False, True, False): lambda s, p, o: self.search_predicate(p),
            (False, False, True): lambda s, p, o: self.search_object(o),
            (
                True,
                True,
                False,
            ): lambda s, p, o: self.search_subject_predicate(s, p),
            (True, False, True): lambda s, p, o: self.search_subject_object(
                s, o
            ),
            (False, True, True): lambda s, p, o: self.search_predicate_object(
                p, o
            ),
            (
                True,
                True,
                True,
            ): lambda s, p, o: self.search_subject_predicate_object(s, p, o),
        }

    def __len__(self):
        return self.count()

    def __iter__(self):
        return (e for e in self.search_all())

    def count(self):
        """
        Get the number of triples in the store.

        Returns
        -------
        int
            Number of triples in the store.
        """
        count = 0
        for s in self._spo:
            for p in self._spo[s]:
                for o in self._spo[s][p]:
                    count += 1
        return count

    #
    # updates
    #

    def insert(self, triple):
        """
        Insert a triple of the form [subject, predicate, object] to the store.

        Parameters
        ----------
        triple: [hashable, hashable, hashable]
            Triple of the form [subject, predicate, object].
            Each element of the list needs to be hashable.

        Returns
        -------
        self: Hexastore
            The store with the inserted triple.

        Raises
        ------
        ValueError
            If triple are not valid.
        """
        if not istriple(triple):
            raise ValueError(
                "triple is not of form [hashable, hashable, hashable]"
            )

        s, p, o = triple

        index_insert(self._spo, s, p, o)
        index_insert(self._sop, s, o, p)
        index_insert(self._pso, p, s, o)
        index_insert(self._pos, p, o, s)
        index_insert(self._osp, o, s, p)
        index_insert(self._ops, o, p, s)

        return self

    #
    # deletes
    #

    def delete_all(self):
        """
        Delete all triples from the store.

        Returns
        -------
        self: Hexastore
            The store with all triples deleted.
        """
        self._spo = {}
        self._sop = {}
        self._pso = {}
        self._pos = {}
        self._osp = {}
        self._ops = {}

        return self

    def delete(self, triple):
        """
        Delete a certain triple of the form [subject, predicate, object]
        from the store.

        Parameters
        ----------
        triple: [hashable, hashable, hashable]
            Triple of the form [subject, predicate, object].
            Each element of the list needs to be hashable.

        Returns
        -------
        self: Hexastore
            The store with the certain triple deleted.

        Raises
        ------
        ValueError
            If triple are not valid.
        """
        if not istriple(triple):
            raise ValueError(
                "triple is not of form [hashable, hashable, hashable]"
            )

        s, p, o = triple

        index_delete(self._spo, s, p, o)
        index_delete(self._sop, s, o, p)
        index_delete(self._pso, p, s, o)
        index_delete(self._pos, p, o, s)
        index_delete(self._osp, o, s, p)
        index_delete(self._ops, o, p, s)

        return self

    #
    # reads
    #

    def search(self, subject=None, predicate=None, object_=None):
        """
        Get all triples with a certain subject and/or predicate and/or object.

        Only triples are returned for which a subject, predicate or object are
        specified. If None are passed, nothing will be matched.

        Note that this is a wrapper for the more specific searches.

        Parameters
        ----------
        subject: hashable or None
            The subject for which matching triples should be returned.
        predicate: hashable or None
            The predicate for which matching triples should be returned.
        object_: hashable or None
            The object for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].
            Empty list of triples if nothing is found.

        Raises
        ------
        ValueError
            If subject, predicate or object are not valid.
        """
        s = subject
        p = predicate
        o = object_

        if not ishashable(s):
            raise ValueError("subject is not hashable")
        if not ishashable(p):
            raise ValueError("predicate is not hashable")
        if not ishashable(o):
            raise ValueError("object is not hashable")

        return self._search_dispatch[
            (s is not None, p is not None, o is not None)
        ](s, p, o)

    def search_all(self):
        """
        Get all triples of the store.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].
            Empty list of triples if nothing is found.
        """
        res = []
        for s in self._spo:
            for p in self._spo[s]:
                for o in self._spo[s][p]:
                    res.append([s, p, o])
        return res

    def search_subject(self, subject):
        """
        Get all triples with a certain subject.

        Parameters
        ----------
        subject: hashable
            The subject for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].
            Empty list of triples if nothing is found.

        Raises
        ------
        ValueError
            If subject is not valid.
        """
        s = subject

        if not ishashable(s):
            raise ValueError("subject is not hashable")

        res = []
        if s in self._spo:
            for p in self._spo[s]:
                for o in self._spo[s][p]:
                    res.append([s, p, o])
        return res

    def search_predicate(self, predicate):
        """
        Get all triples with a certain predicate.

        Parameters
        ----------
        predicate: hashable
            The predicate for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].
            Empty list of triples if nothing is found.

        Raises
        ------
        ValueError
            If predicate is not valid.
        """
        p = predicate

        if not ishashable(p):
            raise ValueError("predicate is not hashable")

        res = []
        if p in self._pso:
            for s in self._pso[p]:
                for o in self._pso[p][s]:
                    res.append([s, p, o])
        return res

    def search_object(self, object_):
        """
        Get all triples with a certain object.

        Parameters
        ----------
        object_: hashable
            The object for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].
            Empty list of triples if nothing is found.

        Raises
        ------
        ValueError
            If object is not valid.
        """
        o = object_

        if not ishashable(o):
            raise ValueError("object is not hashable")

        res = []
        if o in self._ops:
            for p in self._ops[o]:
                for s in self._ops[o][p]:
                    res.append([s, p, o])
        return res

    def search_subject_predicate(self, subject, predicate):
        """
        Get all triples with a certain subject and predicate.

        Parameters
        ----------
        subject: hashable
            The subject for which matching triples should be returned.
        predicate: hashable
            The subject for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].
            Empty list of triples if nothing is found.

        Raises
        ------
        ValueError
            If subject or predicate are not valid.
        """
        s = subject
        p = predicate

        if not ishashable(s):
            raise ValueError("subject is not hashable")
        if not ishashable(p):
            raise ValueError("predicate is not hashable")

        res = []
        if s in self._spo and p in self._spo[s]:
            for o in self._spo[s][p]:
                res.append([s, p, o])
        return res

    def search_predicate_object(self, predicate, object_):
        """
        Get all triples with a certain predicate and object.

        Parameters
        ----------
        predicate: hashable
            The subject for which matching triples should be returned.
        object_: hashable
            The object for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].

        Raises
        ------
        ValueError
            If predicate or object are not valid.
        """
        p = predicate
        o = object_

        if not ishashable(p):
            raise ValueError("predicate is not hashable")
        if not ishashable(o):
            raise ValueError("object is not hashable")

        res = []
        if p in self._pos and o in self._pos[p]:
            for s in self._pos[p][o]:
                res.append([s, p, o])
        return res

    def search_subject_object(self, subject, object_):
        """
        Get all triples with a certain subject and object.

        Parameters
        ----------
        subject: hashable
            The subject for which matching triples should be returned.
        object_: hashable
            The object for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].

        Raises
        ------
        ValueError
            If subject or object are not valid.
        """
        s = subject
        o = object_

        if not ishashable(s):
            raise ValueError("subject is not hashable")
        if not ishashable(o):
            raise ValueError("object is not hashable")

        res = []
        if s in self._sop and o in self._sop[s]:
            for p in self._sop[s][o]:
                res.append([s, p, o])
        return res

    def search_subject_predicate_object(self, subject, predicate, object_):
        """
        Get all triples with a certain subject, predicate and object.

        Parameters
        ----------
        subject: hashable
            The subject for which matching triples should be returned.
        predicate: hashable
            The predicate for which matching triples should be returned.
        object_: hashable
            The object for which matching triples should be returned.

        Returns
        -------
        triples: [[hashable, hashable, hashable]]
            Triples of the form [[subject, predicate, object]].

        Raises
        ------
        ValueError
            If subject, predicate or object are not valid.
        """
        s = subject
        p = predicate
        o = object_

        if not ishashable(s):
            raise ValueError("subject is not hashable")
        if not ishashable(p):
            raise ValueError("predicate is not hashable")
        if not ishashable(o):
            raise ValueError("object is not hashable")

        if s in self._spo and p in self._spo[s] and o in self._spo[s][p]:
            return [[s, p, o]]
        return []

    #
    # import / export
    #

    def export_json(self, name):
        """
        Export current triples to json.

        Parameters
        ----------
        name: str
            Name of the json file to export to.
        """
        with open("{0}.json".format(name), "w") as f:
            json.dump(self._spo, f)

    def import_json(self, name, overwrite=True):
        """
        Import triples from json.

        Parameters
        ----------
        name: str
            Name of the json file to import from.
        overwrite: bool
            If import should overwrite current triples.
            Default to True.
        """
        with open("{0}.json".format(name), "r") as f:
            triples = json.load(f)
            for s in triples:
                for p in triples[s]:
                    for o in triples[s][p]:
                        self.insert([s, p, o])
