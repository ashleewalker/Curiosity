import tempfile
import unittest
from pathlib import Path

from curiosity.service import MemoryService


class CuriosityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.service = MemoryService(Path(self.tmp.name) / "test.db")

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_remember_and_get(self) -> None:
        memory = self.service.remember("SQLite is a local database", kind="knowledge", tags=["storage"])
        memories = self.service.list(kind="knowledge")
        self.assertEqual(len(memories), 1)
        self.assertEqual(memories[0].id, memory.id)

    def test_search_ranks_matching_text(self) -> None:
        self.service.remember("Python testing with unittest", tags=["testing"])
        self.service.remember("A recipe for banana bread", tags=["food"])
        results = self.service.search("Python testing")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].memory.text, "Python testing with unittest")
        self.assertGreater(results[0].score, 0)

    def test_kind_filter(self) -> None:
        self.service.remember("Agent deployment skill", kind="skill")
        self.service.remember("Agent deployment knowledge", kind="knowledge")
        results = self.service.search("agent deployment", kind="skill")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].memory.kind, "skill")

    def test_forget(self) -> None:
        memory = self.service.remember("temporary context")
        self.assertTrue(self.service.forget(memory.id))
        self.assertFalse(self.service.forget(memory.id))
        self.assertEqual(self.service.list(), [])

    def test_empty_query(self) -> None:
        self.service.remember("anything")
        self.assertEqual(self.service.search(""), [])


if __name__ == "__main__":
    unittest.main()
