from unittest import TestCase, main
from hexastore.hexastore import Hexastore
import os


class test_initialize(TestCase):
    def test_create_db(self):
        _ = Hexastore()

    def test_empty_db(self):
        db = Hexastore()
        self.assertEqual(db.size(), 0)


class test_create(TestCase):
    def setUp(self):
        self.db = Hexastore()

    def test_put(self):
        self.db.put(["hello world", "is", "sentance"])
        self.assertEqual(self.db.size(), 1)

    def test_putall(self):
        self.db.putall(
            [
                ["hey", "hey", "ho"],
                ["hey", "hay", "ho"],
                ["hey", "hey", "ha"],
                ["hey", "hey", "hon"],
            ]
        )

        self.assertEqual(self.db.size(), 4)

    def test_addSPO(self):
        element = {"a": {"b": {"c": True}}}
        self.db.addSPO(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getSPO(), element)

    def test_addSOP(self):
        element = {"aa": {"bb": {"cc": True}}}
        self.db.addSOP(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getSOP(), element)

    def test_addOSP(self):
        element = {"aaa": {"bbb": {"ccc": True}}}
        self.db.addOSP(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getOSP(), element)

    def test_addOPS(self):
        element = {"aaaa": {"bbbb": {"cccc": True}}}
        self.db.addOPS(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getOPS(), element)

    def test_addPSO(self):
        element = {"aaaaa": {"bbbbb": {"ccccc": True}}}
        self.db.addPSO(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getPSO(), element)

    def test_addPOS(self):
        element = {"aaaaaa": {"bbbbbb": {"cccccc": True}}}
        self.db.addPOS(element)
        self.assertEqual(self.db.size(), 1)
        self.assertDictEqual(self.db.getPOS(), element)

    def test_addDictAsPath(self):

        self.db.addDictAsPath(
            {"know": "joe", "lol": {"wow": "hab"}, "a": 1}, "bob"
        )

        self.assertEqual(self.db.size(), 4)
        self.assertIn(["bob", "know", "joe", True], self.db.all())
        self.assertIn(["bob", "a", "1", True], self.db.all())
        self.assertIn(["bob/lol", "wow", "hab", True], self.db.all())
        self.assertIn(["bob", "lol", "bob/lol", True], self.db.all())

        self.db.addDictAsPath({"a": {"b": 1}}, "bob", ">")
        self.assertIn(["bob", "a", "bob>a", True], self.db.all())
        self.assertIn(["bob>a", "b", "1", True], self.db.all())

    def test_addDictAsJSON(self):
        added = self.db.addDictAsJSON(
            {"know": "joe", "lol": {"wow": "hab"}, "a": 1}
        )
        self.assertEqual(self.db.size(), 4)
        self.assertIn([added, "know", "joe", True], self.db.all())
        self.assertIn([added, "a", "1", True], self.db.all())
        self.assertIn([added, "lol", '{"wow": "hab"}', True], self.db.all())
        self.assertIn(['{"wow": "hab"}', "wow", "hab", True], self.db.all())

    def test_addDictAsUUID(self):
        added = self.db.addDictAsUUID(
            {"know": "joe", "lol": {"wow": "hab"}, "a": 1}
        )
        self.assertEqual(self.db.size(), 4)
        self.assertIn([added, "know", "joe", True], self.db.all())
        self.assertIn([added, "a", "1", True], self.db.all())


class test_copy(TestCase):
    def setUp(self):
        self.db = Hexastore()
        self.db.putall(
            [
                ["hey", "hey", "ho"],
                ["hey", "hay", "ha"],
                ["hi", "hey", "ha"],
                ["hi", "hey", "hon"],
            ]
        )

    def test_copySubject(self):
        self.db.copySubject("hey", "bobie")
        self.assertIn(["bobie", "hey", "ho", True], self.db.all())
        self.assertIn(["bobie", "hay", "ha", True], self.db.all())

    def test_copyPredicate(self):
        self.db.copyPredicate("hey", "bo")
        self.assertIn(["hey", "bo", "ho", True], self.db.all())
        self.assertIn(["hi", "bo", "ha", True], self.db.all())
        self.assertIn(["hi", "bo", "hon", True], self.db.all())

    def test_copyObject(self):
        self.db.copyObject("ha", "lid")
        self.assertIn(["hey", "hay", "lid", True], self.db.all())
        self.assertIn(["hi", "hey", "lid", True], self.db.all())


class test_read(TestCase):
    def setUp(self):
        self.db = Hexastore()
        self.db.addSPO({"a": {"b": {"c": True}}})

    def test_queryXXX(self):
        res = self.db.queryXXX(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_querySXX(self):
        res = self.db.querySXX(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_queryXPX(self):
        res = self.db.queryXPX(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_queryXXO(self):
        res = self.db.queryXXO(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_querySPX(self):
        res = self.db.querySPX(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_querySXO(self):
        res = self.db.querySXO(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_queryXPO(self):
        res = self.db.queryXPO(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_querySPO(self):
        res = self.db.querySPO(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

    def test_queryDispatch(self):
        res = self.db.queryDispatch(["a", "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

        res = self.db.queryDispatch([["a"], "b", "c"])
        self.assertEqual([["a", "b", "c", True]], res)

        res = self.db.queryDispatch(["a", ["b"], "c"])
        self.assertEqual([["a", "b", "c", True]], res)

        res = self.db.queryDispatch([["a"], ["b"], "c"])
        self.assertEqual([["a", "b", "c", True]], res)

        res = self.db.queryDispatch(["a", "b", ["c"]])
        self.assertEqual([["a", "b", "c", True]], res)

        res = self.db.queryDispatch([["a"], "b", ["c"]])
        self.assertEqual([["a", "b", "c", True]], res)

        res = self.db.queryDispatch(["a", ["b"], ["c"]])
        self.assertEqual([["a", "b", "c", True]], res)

        res = self.db.queryDispatch([["a"], ["b"], ["c"]])
        self.assertEqual([["a", "b", "c", True]], res)


class test_search(TestCase):
    def setUp(self):
        self.db = Hexastore()
        self.db.importNt("./tests/smalltestdataset")

    def test_search_filter(self):
        res = self.db.search(
            [
                [
                    "<bizer/bsbm/v01/instances/ProductType1>",
                    ["predicate"],
                    ["object"],
                ],
                [["similar"], ["predicate"], ["object"]],
            ]
        )
        self.assertEqual(72, len(res))

    def test_precise_search(self):
        res = self.db.search(
            [
                [
                    "<bizer/bsbm/v01/instances/ProductType1>",
                    "<dc/elements/1.1/publisher>",
                    ["publisher"],
                ]
            ]
        )

        self.assertEqual(
            "<bizer/bsbm/v01/instances/StandardizationInstitution1>",
            res[0]["publisher"],
        )


class test_import_export(TestCase):
    def setUp(self):
        self.db = Hexastore()
        self.data = {"aaa": {"bbb": {"ccc": True}}}
        self.db.addSPO(self.data)

    def tearDown(self):
        fj = "hexastoretest1.json"
        fn = "hexastoretest1.nt"
        if os.path.exists(fj):
            os.remove(fj)
        if os.path.exists(fn):
            os.remove(fn)

    def test_json(self):
        self.db.exportJSON("hexastoretest1")
        self.db.clear()
        self.db.importJSON("hexastoretest1")
        self.assertEqual(self.db.size(), 1)
        self.assertEqual(self.data, self.db.getSPO())

    def test_nt(self):
        self.db.exportNt("hexastoretest1")
        self.db.clear()
        self.db.importNt("hexastoretest1")
        self.assertEqual(self.db.size(), 1)
        self.assertEqual(self.data, self.db.getSPO())


if __name__ == "__main__":
    main()
