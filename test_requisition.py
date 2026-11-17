import unittest
from decimal import Decimal
from requisition import Requisition


class TestRequisitionSystem(unittest.TestCase):
    def setUp(self):
        # reset class vars before each test
        Requisition.requisitions = []
        Requisition.next_id = 10000

    def make_req(self, amount):
        r = Requisition("18/11/2026", "FN19", "John Paul")
        r.add_requisition([("Equipment", amount)])
        return r

    def test_auto_approve_under_500(self):
        r = self.make_req("499.99")
        self.assertEqual(r.status, "Approved")
        self.assertEqual(r.approval_reference, "FN19001")

    def test_500_needs_manager(self):
        r = self.make_req("500")
        self.assertEqual(r.status, "Pending")
        r.respond_requisition("Approved")
        self.assertEqual(r.approval_reference, "FN19001")

    def test_stats_count(self):
        reqs = [self.make_req(val) for val in ["450", "500", "3500", "499.99", "700"]]
        stats = Requisition.requisition_statistics()
        self.assertEqual(stats["submitted"], 5)
        self.assertEqual(stats["approved"], 2)
        self.assertEqual(stats["pending"], 3)

        reqs[1].respond_requisition("Approved")
        reqs[2].respond_requisition("Not approved")
        
        updated_stats = Requisition.requisition_statistics()
        self.assertEqual(updated_stats["approved"], 3)
        self.assertEqual(updated_stats["not approved"], 1)
        self.assertEqual(reqs[2].approval_reference, "Not available")

    def test_bad_inputs(self):
        for bad_cost in ["-1", "0", "abc", "1.001"]:
            with self.assertRaises(ValueError):
                self.make_req(bad_cost)
        
        with self.assertRaises(ValueError):
            Requisition("18/11/2026", "FN19", "John").add_requisition([])

        # bad staff id format
        with self.assertRaises(ValueError):
            Requisition("18/11/2026", "19FN", "John")

    def test_cant_change_final_decision(self):
        r = self.make_req("500")
        r.respond_requisition("Not approved")
        with self.assertRaises(ValueError):
            r.respond_requisition("Approved")


if __name__ == "__main__":
    unittest.main()
