import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from requisition import Requisition


def update_display():
    output_text.delete("1.0", tk.END)
    for r in Requisition.requisitions:
        output_text.insert(tk.END, r.details() + "\n" + "-"*25 + "\n")
        
    output_text.insert(tk.END, "\n--- STATISTICS ---\n")
    stats = Requisition.requisition_statistics()
    for key, val in stats.items():
        output_text.insert(tk.END, f"{key.capitalize()}: {val}\n")


def handle_submit():
    try:
        raw_lines = items_input.get("1.0", tk.END).strip().splitlines()
        parsed_items = []
        for line in raw_lines:
            if not line.strip():
                continue
            parts = line.rsplit(",", 1)
            if len(parts) != 2:
                raise ValueError("Format each line as: Item Name, Cost")
            parsed_items.append((parts[0], parts[1].strip()))
            
        req = Requisition(date_input.get(), staff_id_input.get(), name_input.get())
        req.add_requisition(parsed_items)
        
        update_display()
        items_input.delete("1.0", tk.END)
    except Exception as e:
        messagebox.showerror("Input Error", f"{e}\n\nMake sure date is DD/MM/YYYY and items are 'name, cost'.")


def handle_decision(status):
    try:
        req_id = int(mgr_id_input.get().strip())
        target = None
        for r in Requisition.requisitions:
            if r.requisition_id == req_id:
                target = r
                break
                
        if not target:
            raise ValueError("Couldn't find a requisition with that ID.")
            
        target.respond_requisition(status)
        update_display()
    except ValueError as e:
        messagebox.showerror("Error", str(e))


# setup main window
window = tk.Tk()
window.title("Requisition Manager")
window.geometry("700x720")

# form fields
tk.Label(window, text="Date (DD/MM/YYYY):").grid(row=0, column=0, sticky="w", padx=10, pady=5)
date_input = tk.Entry(window, width=30)
date_input.grid(row=0, column=1, sticky="w")
date_input.insert(0, datetime.now().strftime("%d/%m/%Y"))

tk.Label(window, text="Staff ID (e.g. FN19):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
staff_id_input = tk.Entry(window, width=30)
staff_id_input.grid(row=1, column=1, sticky="w")

tk.Label(window, text="Staff Name:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
name_input = tk.Entry(window, width=30)
name_input.grid(row=2, column=1, sticky="w")

tk.Label(window, text="Items (Item, Cost per line):").grid(row=3, column=0, sticky="nw", padx=10, pady=5)
items_input = tk.Text(window, width=35, height=5)
items_input.grid(row=3, column=1, pady=5, sticky="w")

tk.Button(window, text="Submit Request", command=None).grid(row=4, column=1, sticky="w", pady=5)

# manager section
tk.Label(window, text="Manager - Requisition ID:").grid(row=5, column=0, sticky="w", padx=10, pady=10)
mgr_id_input = tk.Entry(window, width=20)
mgr_id_input.grid(row=5, column=1, sticky="w")

btn_frame = tk.Frame(window)
btn_frame.grid(row=6, column=1, sticky="w")
tk.Button(btn_frame, text="Approve", command=lambda: handle_decision("Approved")).pack(side="left", padx=(0, 5))
tk.Button(btn_frame, text="Not Approve", command=lambda: handle_decision("Not approved")).pack(side="left")

# output box
output_text = tk.Text(window, width=78, height=20, wrap="word")
output_text.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

scroll = tk.Scrollbar(window, command=output_text.yview)
scroll.grid(row=7, column=2, sticky="ns")
output_text.config(yscrollcommand=scroll.set)

window.grid_rowconfigure(7, weight=1)
window.grid_columnconfigure(1, weight=1)

update_display()
window.mainloop()
