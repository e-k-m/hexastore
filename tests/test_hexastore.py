from unittest import TestCase, main
from hexa.hexastore import Hexastore


class test_initialize(TestCase):

    def test_create_db(self):
            db = Hexastore()

    def test_empty_db(self):
        db = Hexastore()
        self.assertEqual(db.size(), 0)


class test_create(TestCase):

    def setUp(self):
        self.db = Hexastore();

    def test_put(self):
        self.db.put(['hello world', 'is', 'sentance'])
        self.assertEqual(self.db.size(), 1)

    def test_putall(self):
        self.db.putall([['hey', 'hey', 'ho'],
                        ['hey', 'hay', 'ho'],
                        ['hey', 'hey', 'ha'],
                        ['hey', 'hey', 'hon']])

        self.assertEqual(self.db.size(), 4)

    def test_addSPO(self):
        element = {'a': {'b': {'c': True}}}
        self.db.addSPO(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getSPO(), element)


    def test_addSOP(self):
        element = {'aa': {'bb': {'cc': True}}}
        self.db.addSOP(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getSOP(), element)

    def test_addOSP(self):
        element = {'aaa': {'bbb': {'ccc': True}}}
        self.db.addOSP(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getOSP(), element)

    def test_addOPS(self):
        element = {'aaaa': {'bbbb': {'cccc': True}}}
        self.db.addOPS(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getOPS(), element)

    def test_addPSO(self):
        element = {'aaaaa': {'bbbbb': {'ccccc': True}}}
        self.db.addPSO(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getPSO(), element)

    def test_addPOS(self):
        element = {'aaaaaa': {'bbbbbb': {'cccccc': True}}}
        self.db.addPOS(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getPOS(), element)





if __name__ == '__main__':
    main()
