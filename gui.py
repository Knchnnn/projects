import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from main import translate_with_steps


# ---------- FUNCTIONS ----------
def compile_code():
    try:
        code = input_box.get("1.0", "end")

        output, steps = translate_with_steps(code)

        output_box.delete("1.0", "end")
        output_box.insert("1.0", output)

        steps_box.delete("1.0", "end")
        steps_box.insert("1.0", steps)

        show_ast(code)

    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_all():
    for box in [input_box, output_box, steps_box, ast_box]:
        box.delete("1.0", "end")


def load_file():
    path = filedialog.askopenfilename(filetypes=[("C Files", "*.c")])
    if path:
        with open(path) as f:
            input_box.delete("1.0", "end")
            input_box.insert("1.0", f.read())


def save_output():
    path = filedialog.asksaveasfilename(defaultextension=".py")
    if path:
        with open(path, "w") as f:
            f.write(output_box.get("1.0", "end"))


# ---------- AST ----------
def show_ast(code):
    ast_box.delete("1.0", "end")
    ast_box.insert("end", "Program\n")

    for line in code.split("\n"):
        line = line.strip()

        if line.startswith(("int", "float")):
            ast_box.insert("end", "  ├─ Declaration\n")
        elif line.startswith("if"):
            ast_box.insert("end", "  ├─ If Statement\n")
        elif line.startswith("while"):
            ast_box.insert("end", "  ├─ While Loop\n")
        elif line.startswith("for"):
            ast_box.insert("end", "  ├─ For Loop\n")
        elif "printf" in line:
            ast_box.insert("end", "  ├─ Print\n")


# ---------- WINDOW ----------
root = tk.Tk()
root.title("C → Python Transpiler")
root.geometry("1000x700")
root.config(bg="#1e1e1e")

tk.Label(root, text="C → Python Transpiler",
         font=("Arial", 16, "bold"),
         bg="#1e1e1e", fg="white").pack(pady=8)

# ---------- BUTTONS ----------
btn_frame = tk.Frame(root, bg="#1e1e1e")
btn_frame.pack(pady=5)

tk.Button(btn_frame, text="Translate", command=compile_code, bg="#007acc", fg="white").grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Clear", command=clear_all).grid(row=0, column=1, padx=5)
tk.Button(btn_frame, text="Load", command=load_file).grid(row=0, column=2, padx=5)
tk.Button(btn_frame, text="Save", command=save_output).grid(row=0, column=3, padx=5)

# ---------- TABS ----------
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", pady=5)

# ---------- TAB 1: EDITOR ----------
editor_tab = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(editor_tab, text="Editor")

frame = tk.Frame(editor_tab, bg="#1e1e1e")
frame.pack(pady=10)

# LEFT (C CODE)
left = tk.Frame(frame, bg="#1e1e1e")
left.grid(row=0, column=0, padx=10)

tk.Label(left, text="C Code",
         bg="#1e1e1e", fg="lightblue",
         font=("Arial", 11, "bold")).pack(anchor="w")

input_box = tk.Text(left, height=20, width=50,
                    bg="#252526", fg="white",
                    font=("Consolas", 10))
input_box.pack()

# RIGHT (PYTHON OUTPUT)
right = tk.Frame(frame, bg="#1e1e1e")
right.grid(row=0, column=1, padx=10)

tk.Label(right, text="Python Output",
         bg="#1e1e1e", fg="lightgreen",
         font=("Arial", 11, "bold")).pack(anchor="w")

output_box = tk.Text(right, height=20, width=50,
                     bg="#252526", fg="white",
                     font=("Consolas", 10))
output_box.pack()

# ---------- TAB 2: STEPS ----------
steps_tab = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(steps_tab, text="Steps")

steps_box = tk.Text(steps_tab,
                    bg="#252526", fg="lightgreen",
                    font=("Consolas", 10))
steps_box.pack(expand=True, fill="both", padx=10, pady=10)

# ---------- TAB 3: AST ----------
ast_tab = tk.Frame(notebook, bg="#1e1e1e")
notebook.add(ast_tab, text="AST")

ast_box = tk.Text(ast_tab,
                  bg="#252526", fg="orange",
                  font=("Consolas", 10))
ast_box.pack(expand=True, fill="both", padx=10, pady=10)

root.mainloop()