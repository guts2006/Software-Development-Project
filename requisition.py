from datetime import datetime
from decimal import Decimal
import re


class Requisition:
    next_id = 10000
    requisitions = []

    def __init__(self, date, staff_id, staff_name):
        # make sure date is valid yyyy-mm-dd
        datetime.strptime(date, "%Y-%m-%d")

        staff_id = staff_id.strip().upper()
        if not re.fullmatch(r"[A-Z]{2}\d{2}", staff_id):
            raise ValueError("Staff ID needs 2 letters and 2 numbers (like FN19)")
            
        if not staff_name or not staff_name.strip():
            raise ValueError("Staff name can't be empty")
            
        self.date = date
        self.staff_id = staff_id
        self.staff_name = staff_name.strip()
        self.requisition_id = None
        self.items = []
        self.total = Decimal("0.00")
        self.status = "Pending"
        self.approval_reference = "Not available"

    def add_requisition(self, items):
        if self.requisition_id is not None:
            raise ValueError("Already submitted this one.")
        if not items:
            raise ValueError("Need at least one item.")
            
        clean_items = []
        for item_name, cost in items:
            try:
                price = Decimal(str(cost))
            except Exception:
                raise ValueError(f"Invalid cost: {cost}")
                
            if not item_name.strip() or not price.is_finite() or price <= 0:
                raise ValueError("Item needs a name and cost > 0")
                
            # check decimal places
            if price != price.quantize(Decimal("0.01")):
                raise ValueError("Max 2 decimal places allowed for cost.")
                
            clean_items.append((item_name.strip(), price))
            
        self.items = clean_items
        total_val = Decimal("0.00")
        for _, c in self.items:
         total_val += c
        self.total = total_val
        
        Requisition.next_id += 1
        self.requisition_id = Requisition.next_id
        
        # auto approve if under 500
        self.approve_requisition()
        Requisition.requisitions.append(self)
        return self.total

    def approve_requisition(self):
        if self.requisition_id is None:
            raise ValueError("Submit first.")
        if self.status == "Pending" and self.total < Decimal("500"):
            self.status = "Approved"
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]

    def respond_requisition(self, decision):
        if self.requisition_id is None or self.status != "Pending":
            raise ValueError("Can only update pending requests.")
        if decision not in ["Approved", "Not approved"]:
            raise ValueError("Must be 'Approved' or 'Not approved'")
            
        self.status = decision
        if decision == "Approved":
            self.approval_reference = self.staff_id + str(self.requisition_id)[-3:]

    def details(self):
        return (
            f"Date: {self.date}\n"
            f"Requisition ID: {self.requisition_id}\n"
            f"Staff ID: {self.staff_id}\n"
            f"Staff Name: {self.staff_name}\n"
            f"Total: ${self.total:.2f}\n"
            f"Status: {self.status}\n"
            f"Approval Reference Number: {self.approval_reference}"
        )

    @classmethod
    def display_requisitions(cls):
        for req in cls.requisitions:
            print(req.details())
            print("-" * 20)

    @classmethod
    def requisition_statistics(cls):
        approved = 0
        pending = 0
        not_approved = 0
        for r in cls.requisitions:
            if r.status == "Approved":
                approved += 1
            elif r.status == "Pending":
                pending += 1
            elif r.status == "Not approved":
                not_approved += 1
                
        return {
            "submitted": len(cls.requisitions),
            "approved": approved,
            "pending": pending,
            "not approved": not_approved
        }

    @classmethod
    def display_statistics(cls):
        print("Requisition Stats:")
        stats = cls.requisition_statistics()
        for k, v in stats.items():
            print(f"Total {k}: {v}")
        print()
