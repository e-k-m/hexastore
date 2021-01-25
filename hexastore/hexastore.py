# Given the triple "s", "p" "o" the hexa store must be something like
# spo: {"a": {"b": "c"}}
# sop: {"s": {"o": "p"}}
# pso: {"p": {"s": "o"}}
# pos: {"p": {"o": "s"}}
# osp: {"o": {"s": "p"}}
# ops: {"o": {"p": "s"}}

import json
import uuid
import csv
import copy


class Hexastore(object):
    def __init__(self):
        self.spo = {}
        self.sop = {}
        self.pso = {}
        self.pos = {}
        self.osp = {}
        self.ops = {}

    def size(self):
        count = 0
        for s in self.spo:
            for p in self.spo[s]:
                for o in self.spo[s][p]:
                    count += 1
        return count

    def put(self, element):
        s = element[0]
        p = element[1]
        o = element[2]
        v = True
        if len(element) == 4:
            v = element[3]

        def f(index, s, p, o):
            if s not in index:
                index[s] = {}
            if p not in index[s]:
                index[s][p] = {}
            index[s][p][o] = v

        f(self.spo, s, p, o)
        f(self.sop, s, o, p)
        f(self.pso, p, s, o)
        f(self.pos, p, o, s)
        f(self.osp, o, s, p)
        f(self.ops, o, p, s)

    def putall(self, elements):
        for e in elements:
            self.put(e)

    def _addSPO(self, element, put):
        for s in element:
            for p in element[s]:
                for o in element[s][p]:
                    v = element[s][p][o]
                    put(s, p, o, v)

    def addSPO(self, element):
        def f(s, p, o, v):
            self.put([s, p, o, v])

        self._addSPO(element, f)

    def addSOP(self, element):
        def f(s, o, p, v):
            self.put([s, p, o, v])

        self._addSPO(element, f)

    def addPSO(self, element):
        def f(p, s, o, v):
            self.put([s, p, o, v])

        self._addSPO(element, f)

    def addPOS(self, element):
        def f(p, o, s, v):
            self.put([s, p, o, v])

        self._addSPO(element, f)

    def addOSP(self, element):
        def f(o, s, p, v):
            self.put([s, p, o, v])

        self._addSPO(element, f)

    def addOPS(self, element):
        def f(o, p, s, v):
            self.put([s, p, o, v])

        self._addSPO(element, f)

    def getSPO(self):
        return self.spo

    def getSOP(self):
        return self.sop

    def getPSO(self):
        return self.pso

    def getPOS(self):
        return self.pos

    def getOSP(self):
        return self.osp

    def getOPS(self):
        return self.ops

    def all(self):
        res = []
        for s in self.spo:
            for p in self.spo[s]:
                for o in self.spo[s][p]:
                    v = self.spo[s][p][o]
                    res.append([s, p, o, v])
        return res

    def clear(self):
        self.spo = {}
        self.sop = {}
        self.pso = {}
        self.pos = {}
        self.osp = {}
        self.ops = {}

    def addDictAsPath(self, obj, name, seperator="/"):
        if isinstance(obj, dict):
            for p in obj:
                self.put(
                    [
                        name,
                        p,
                        self.addDictAsPath(
                            obj[p],
                            "{0}{1}{2}".format(name, seperator, p),
                            seperator,
                        ),
                        True,
                    ]
                )
            return name
        elif isinstance(obj, str):
            return obj
        else:
            return json.dumps(obj)

    def addDictAsJSON(self, obj):
        if isinstance(obj, dict):
            name = json.dumps(obj)
            for p in obj:
                self.put([name, p, self.addDictAsJSON(obj[p])])
            return name
        elif isinstance(obj, str):
            return obj
        else:
            return json.dumps(obj)

    def addDictAsUUID(self, obj):
        if isinstance(obj, dict):
            name = str(uuid.uuid4())
            for p in obj:
                self.put([name, p, self.addDictAsUUID(obj[p])])
            return name
        elif isinstance(obj, str):
            return obj
        else:
            return json.dumps(obj)

    def copySubject(self, subj, newsubj):
        res = self.querySXX([subj, None, None])
        self.putall([[newsubj, el[1], el[2], el[3]] for el in res])
        return len(res)

    def copyPredicate(self, pred, newpred):
        res = self.queryXPX([None, pred, None])
        self.putall([[el[0], newpred, el[2], el[3]] for el in res])
        return len(res)

    def copyObject(self, obj, newobj):
        res = self.queryXXO([None, None, obj])
        self.putall([[el[0], el[1], newobj, el[3]] for el in res])
        return len(res)

    def queryXXX(self, element):
        res = []
        for s in self.spo:
            for p in self.spo[s]:
                for o in self.spo[s][p]:
                    val = self.spo[s][p][o]
                    res.append([s, p, o, val])
        return res

    def querySXX(self, element):
        s = element[0]
        res = []
        for p in self.spo[s]:
            for o in self.spo[s][p]:
                val = self.spo[s][p][o]
                res.append([s, p, o, val])
        return res

    def queryXPX(self, element):
        p = element[1]
        res = []
        for s in self.pso[p]:
            for o in self.pso[p][s]:
                val = self.pso[p][s][o]
                res.append([s, p, o, val])
        return res

    def queryXXO(self, element):
        o = element[2]
        res = []
        for p in self.ops[o]:
            for s in self.ops[o][p]:
                val = self.ops[o][p][s]
                res.append([s, p, o, val])
        return res

    def querySPX(self, element):
        s = element[0]
        p = element[1]
        res = []
        for o in self.spo[s][p]:
            val = self.spo[s][p][o]
            res.append([s, p, o, val])
        return res

    def queryXPO(self, element):
        p = element[1]
        o = element[2]
        res = []
        for s in self.pos[p][o]:
            val = self.pos[p][o][s]
            res.append([s, p, o, val])
        return res

    def querySXO(self, element):
        s = element[0]
        o = element[2]
        res = []
        for p in self.sop[s][o]:
            val = self.sop[s][o][p]
            res.append([s, p, o, val])
        return res

    def querySPO(self, element):
        s = element[0]
        p = element[1]
        o = element[2]
        val = self.spo[s][p][o]
        return [[s, p, o, val]]

    def queryDispatch(self, element):
        def islist(e):
            return isinstance(e, list)

        if islist(element[0]):
            if islist(element[1]):
                if islist(element[2]):
                    return self.queryXXX(element)
                else:
                    return self.queryXXO(element)
            else:
                if islist(element[2]):
                    return self.queryXPX(element)
                else:
                    return self.queryXPO(element)
        else:
            if islist(element[1]):
                if islist(element[2]):
                    return self.querySXX(element)
                else:
                    return self.querySXO(element)
            else:
                if islist(element[2]):
                    return self.querySPX(element)
                else:
                    return self.querySPO(element)

    def search(self, query):
        def instantiateVariablesInQuery(result, query):
            res = []
            for q in query:
                r = []
                for e in q:
                    if isinstance(e, list) and e[0] in result:
                        r.append(result[e[0]])
                    else:
                        r.append(e)
                res.append(r)
            return res

        def instantiateVariablesInResult(result, query, triples):
            res = [None] * len(triples)
            for i in range(len(triples)):
                res[i] = copy.copy(result)
                for j in range(3):
                    if isinstance(query[j], list):
                        res[i][query[j][0]] = triples[i][j]
            return res

        def doSearch(result, theQuery):
            query = instantiateVariablesInQuery(result, theQuery)
            triples = self.queryDispatch(query[0])
            results = instantiateVariablesInResult(result, query[0], triples)
            query = query[1:]
            res = []
            if len(query) > 0:
                for result in results:
                    res = res + doSearch(result, query)
            else:
                res = results
            return res

        return doSearch({}, query)

    def exportJSON(self, dbname):
        with open("{0}.json".format(dbname), "w") as f:
            json.dump(self.spo, f)

    def importJSON(self, dbname):
        with open("{0}.json".format(dbname), "r") as f:
            self.addSPO(json.load(f))

    # FIXME: Buggy, since format is <> <> <> [<>].
    def exportNt(self, ntname):
        s = "".join(
            (
                "{0} {1} {2} {3} .\n".format(
                    e[0], e[1], e[2], json.dumps(e[3])
                )
                for e in self.all()
            )
        )
        with open("{0}.nt".format(ntname), "w") as f:
            f.write(s)

    # FIXME: Buggy, since format is <> <> <> [<>].
    def importNt(self, ntname):
        with open("{0}.nt".format(ntname), "r") as f:
            r = csv.reader(f, delimiter=" ", quotechar="|")
            for e in r:
                if len(e) == 5:
                    try:
                        self.put([e[0], e[1], e[2], json.loads(e[3])])
                    except ValueError:
                        self.put([e[0], e[1], e[2], e[3]])
                else:
                    self.put([e[0], e[1], e[2], True])
