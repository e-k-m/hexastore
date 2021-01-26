import unittest
import os

from hexastore import Hexastore


class TestCreate(unittest.TestCase):
    def test_store_create(self):
        store = Hexastore()
        self.assertEqual(store.count(), 0)


class TestInterfaces(unittest.TestCase):
    def setUp(self):
        self.store = Hexastore()
        self.store.insert(["hello world", "is", "sentance"])
        self.store.insert(["hello yal", "is", "sentance"])

    def test_len(self):
        self.assertEqual(len(self.store), 2)

    def test_iter(self):
        for i, e in enumerate(self.store):
            if i == 0:
                self.assertEqual(e, ["hello world", "is", "sentance"])
            elif i == 1:
                self.assertEqual(e, ["hello yal", "is", "sentance"])


class TestInsert(unittest.TestCase):
    def setUp(self):
        self.store = Hexastore()

    def test_insert(self):
        r = self.store.insert(["hello world", "is", "sentance"])
        self.assertEqual(r, self.store)
        self.assertEqual(self.store.count(), 1)
        self.assertRaises(ValueError, self.store.insert, [])
        self.assertRaises(ValueError, self.store.insert, [None, None, None])
        self.assertRaises(ValueError, self.store.insert, [{}, {}, {}])


class TestDelete(unittest.TestCase):
    def setUp(self):
        self.store = Hexastore()
        self.store.insert(["a", "b", "c"]).insert(["e", "f", "g"])

    def test_delete_all(self):
        self.assertEqual(self.store.count(), 2)
        r = self.store.delete_all()
        self.assertEqual(r, self.store)
        self.assertEqual(self.store.count(), 0)

    def test_delete(self):
        self.assertTrue(self.store.search("e", "f", "g"))
        r = self.store.delete(["e", "f", "g"])
        self.assertEqual(r, self.store)
        self.assertFalse(self.store.search("e", "f", "g"))
        self.assertRaises(ValueError, self.store.delete, [])
        self.assertRaises(ValueError, self.store.delete, [None, None, None])
        self.assertRaises(ValueError, self.store.delete, [{}, {}, {}])
        r = self.store.delete(["dummy", "dummy", "dummy"])


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.store = Hexastore()
        self.should = ["a", "b", "c"]
        self.store.insert(self.should).insert(["e", "f", "g"])

    def test_search(self):
        r = self.store.search(subject="a")
        self.assertEqual(r, [self.should])

        r = self.store.search(None, "b")
        self.assertEqual(r, [self.should])

        r = self.store.search(None, None, "c")
        self.assertEqual(r, [self.should])

        r = self.store.search("a", "b", None)
        self.assertEqual(r, [self.should])

        r = self.store.search("a", None, "c")
        self.assertEqual(r, [self.should])

        r = self.store.search(None, "b", "c")
        self.assertEqual(r, [self.should])

        r = self.store.search("a", "b", "c")
        self.assertEqual(r, [self.should])

        r = self.store.search()
        self.assertEqual(r, [self.should, ["e", "f", "g"]])

        self.assertRaises(ValueError, self.store.search, {}, None, None)
        self.assertRaises(ValueError, self.store.search, None, {}, None)
        self.assertRaises(ValueError, self.store.search, None, None, {})

    def test_search_subject(self):
        r = self.store.search_subject("a")
        self.assertEqual(r, [self.should])

        r = self.store.search_subject("dummy")
        self.assertEqual(r, [])

    def test_search_predicate(self):
        r = self.store.search_predicate("b")
        self.assertEqual(r, [self.should])

        r = self.store.search_predicate("dummy")
        self.assertEqual(r, [])

    def test_search_object(self):
        r = self.store.search_object("c")
        self.assertEqual(r, [self.should])

        r = self.store.search_object("dummy")
        self.assertEqual(r, [])

    def test_search_subject_predicate(self):
        r = self.store.search_subject_predicate("a", "b")
        self.assertEqual(r, [self.should])

        r = self.store.search_subject_predicate("dummy", "dummy")
        self.assertEqual([], r)

        r = self.store.search_subject_predicate("a", "dummy")
        self.assertEqual([], r)

    def test_search_subject_object(self):
        r = self.store.search_subject_object("a", "c")
        self.assertEqual(r, [self.should])

        r = self.store.search_subject_object("a", "dummy")
        self.assertEqual(r, [])

        r = self.store.search_subject_object("dummy", "dummy")
        self.assertEqual(r, [])

    def test_search_predicate_object(self):
        r = self.store.search_predicate_object("b", "c")
        self.assertEqual(r, [self.should])

        r = self.store.search_predicate_object("b", "dummy")
        self.assertEqual(r, [])

        r = self.store.search_predicate_object("dummy", "dummy")
        self.assertEqual(r, [])

    def test_search_subject_predicate_object(self):
        r = self.store.search_subject_predicate_object("a", "b", "c")
        self.assertEqual(r, [self.should])

        r = self.store.search_subject_predicate_object("a", "dummy", "dummy")
        self.assertEqual(r, [])

        r = self.store.search_subject_predicate_object("a", "b", "dummy")
        self.assertEqual(r, [])

        r = self.store.search_subject_predicate_object("a", "dummy", "c")
        self.assertEqual(r, [])

        r = self.store.search_subject_predicate_object(
            "dummy", "dummy", "dummy"
        )
        self.assertEqual(r, [])


class TestImportExport(unittest.TestCase):
    def setUp(self):
        self.store = Hexastore()
        self.data = {"aaa": {"bbb": {"ccc": None}}}
        self.store.insert(["aaa", "bbb", "ccc"])
        self.name = "hexastore"

    def tearDown(self):
        path = f"./{self.name}.json"
        if os.path.exists(path):
            os.remove(path)

    def test_json(self):
        self.store.export_json(self.name)
        self.store.delete_all()
        self.store.import_json(self.name)
        self.assertEqual(self.store.count(), 1)
        self.assertEqual(self.data, self.store._spo)


if __name__ == "__main__":
    unittest.main()
