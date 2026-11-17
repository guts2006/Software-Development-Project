from requisition import Requisition


def run_tests():
    # sample data from the brief
    sample_data = [
        ("18/11/2026", "FN19", "John Paul", [("Paper", "150"), ("Ink", "300")]),
        ("18/11/2026", "FN20", "Tracy Brown", [("Monitor", "500")]),
        ("18/11/2026", "FN15", "Emma Wellington", [("Laptop", "3500")]),
        ("18/11/2026", "FN02", "Catlin White", [("Chair", "499.99")]),
        ("18/11/2026", "FN21", "Sam Lee", [("Desk", "700")])
    ]
    
    reqs = []
    for d, s_id, name, item_list in sample_data:
        r = Requisition(d, s_id, name)
        r.add_requisition(item_list)
        reqs.append(r)

    print("=== BEFORE MANAGER DECISIONS ===\n")
    Requisition.display_requisitions()
    Requisition.display_statistics()

    # manager updates a couple of them, leaving Sam's pending
    reqs[1].respond_requisition("Approved")
    reqs[2].respond_requisition("Not approved")
    
    print("=== AFTER MANAGER DECISIONS ===\n")
    Requisition.display_requisitions()
    Requisition.display_statistics()


if __name__ == "__main__":
    run_tests()
