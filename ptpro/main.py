import tkinter as tk
from tkinter import messagebox, ttk
from pagereplace import fifo, lru, optimal, parse_reference_string, validate_inputs

class SimplePageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Page Replacement Simulator")
        self.root.geometry("750x500")

        panel = tk.Frame(root, padx=10, pady=10)
        panel.pack(fill=tk.X)

        tk.Label(panel, text="Reference String:").pack(side=tk.LEFT)
        self.pages_entry = tk.Entry(panel, width=22)
        self.pages_entry.insert(0, "7 0 1 2 0 3 0 4 2 3 0 3 2")
        self.pages_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(panel, text="Frames:").pack(side=tk.LEFT, padx=(10, 0))
        self.frames_spin = tk.Spinbox(panel, from_=1, to=10, width=4)
        self.frames_spin.delete(0, "end")
        self.frames_spin.insert(0, "3")
        self.frames_spin.pack(side=tk.LEFT, padx=5)

        tk.Label(panel, text="Algorithm:").pack(side=tk.LEFT, padx=(10, 0))
        self.algo_cb = ttk.Combobox(
            panel,
            values=["FIFO", "LRU", "Optimal", "Compare All"],
            width=12,
            state="readonly",
        )
        self.algo_cb.set("FIFO")
        self.algo_cb.pack(side=tk.LEFT, padx=5)

        tk.Button(
            panel,
            text="Run",
            command=self.run_simulation,
            bg="#18f009",
            fg="black",
            padx=10,
        ).pack(side=tk.LEFT, padx=10)

     
        self.output = tk.Text(
            root, font=("Consolas", 10), bg="#de73c2", padx=10, pady=10
        )
        self.output.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def run_simulation(self):
        try:
            pages = parse_reference_string(self.pages_entry.get())
            frames_count = validate_inputs(pages, self.frames_spin.get())
            selected = self.algo_cb.get()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
            return

        algos = {"FIFO": fifo, "LRU": lru, "Optimal": optimal}
        self.output.delete("1.0", tk.END)

        target_algos = ["FIFO", "LRU", "Optimal"] if selected == "Compare All" else [selected]

        for name in target_algos:
            faults, hits, trace = algos[name](pages, frames_count)
            text_result = self.format_output(name, frames_count, trace, faults, hits)
            self.output.insert(tk.END, text_result + "\n" + "=" * 65 + "\n\n")

    def format_output(self, name, frames_count, trace, faults, hits):
        res = f"Algorithm: {name}  |  Faults: {faults}  |  Hits: {hits}\n"
        res += "-" * 55 + "\n"

     
        res += "Page:  " + "  ".join(f"{p}" for p, _, _ in trace) + "\n"
        res += "-" * 55 + "\n"

      
        for f in range(frames_count):
            vals = [t[1][f] for t in trace]
            res += f"F{f+1}:    " + "  ".join(f"{v}" for v in vals) + "\n"

        res += "-" * 55 + "\n"
  
        statuses = [t[2] for t in trace]
        res += "Stat:  " + "  ".join(s for s in statuses) + "\n"
        return res

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplePageApp(root)
    root.mainloop()