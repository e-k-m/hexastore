
# Given the triple "s", "p" "o" the hexa store must be something like
# spo: {"a": {"b": "c"}}
# sop: {"s": {"o": "p"}}
# pso: {"p": {"s": "o"}}
# pos: {"p": {"o": "s"}}
# osp: {"o": {"s": "p"}}
# ops: {"o": {"p": "s"}}


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
            if not s in index:
                index[s] = {}
            if not p in index[s]:
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

    def clear(self):
        self.spo = {}
        self.sop = {}
        self.pso = {}
        self.pos = {}
        self.osp = {}
        self.ops = {}



        
