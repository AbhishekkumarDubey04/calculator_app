import tkinter as tk
import os
from calculator_logic import CalculatorLogic
from graph_window import GraphWindow

# Theme Colors
BG_COLOR = "#121212"
ACCENT_COLOR = "#FFD60A"
BTN_DARK = "#282B33"
BTN_HOVER = "#3D414D"
TEXT_COLOR = "#FFFFFF"

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Premium Calculator")
        self.geometry("400x650")
        self.configure(bg=BG_COLOR)
        self.resizable(False, False)
        
        self.logic = CalculatorLogic()
        self.history = []
        
        self.setup_ui()
        self.bind("<Key>", self.handle_keypress)

    def bind_hover(self, widget, normal_bg, hover_bg):
        widget.bind("<Enter>", lambda e: widget.configure(bg=hover_bg))
        widget.bind("<Leave>", lambda e: widget.configure(bg=normal_bg))

    def setup_ui(self):
        # 1. Top Panel (Display + History Preview)
        self.top_frame = tk.Frame(self, bg=BG_COLOR)
        self.top_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        self.history_label = tk.Label(
            self.top_frame, text="", font=("Inter", 12), fg="#A0A0A0", bg=BG_COLOR, anchor="e"
        )
        self.history_label.pack(fill="x")
        
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            self.top_frame, textvariable=self.display_var, font=("Inter", 48, "bold"),
            fg=TEXT_COLOR, bg=BG_COLOR, justify="right", bd=0, highlightthickness=0,
            state="readonly", readonlybackground=BG_COLOR
        )
        self.display.pack(fill="x", pady=(5, 10))
        
        self.preview_label = tk.Label(
            self.top_frame, text="", font=("Inter", 14), fg="#777777", bg=BG_COLOR, anchor="e"
        )
        self.preview_label.pack(fill="x")

        # 2. Keypad Frame
        self.keypad_frame = tk.Frame(self, bg=BG_COLOR)
        self.keypad_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        for i in range(5):
            self.keypad_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.keypad_frame.grid_columnconfigure(i, weight=1)

        # Advanced/Memory controls header
        self.top_controls_frame = tk.Frame(self.keypad_frame, bg=BG_COLOR)
        self.top_controls_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 10))
        
        mem_btns = ["MC", "MR", "M+", "M-", "Hist", "Sci"]
        for i, text in enumerate(mem_btns):
            btn = tk.Button(
                self.top_controls_frame, text=text, font=("Inter", 10, "bold"), 
                width=4, bg="#181818", fg=TEXT_COLOR, activebackground=BTN_HOVER,
                activeforeground=TEXT_COLOR, relief="flat", bd=0,
                command=lambda t=text: self.handle_special(t)
            )
            btn.pack(side="left", padx=2, expand=True, fill="both")
            self.bind_hover(btn, "#181818", BTN_HOVER)

        # Basic Keypad Layout
        buttons = [
            ('C', '#ff4444', TEXT_COLOR), ('⌫', BTN_DARK, TEXT_COLOR), ('%', BTN_DARK, TEXT_COLOR), ('÷', BTN_DARK, ACCENT_COLOR),
            ('7', BTN_DARK, TEXT_COLOR), ('8', BTN_DARK, TEXT_COLOR), ('9', BTN_DARK, TEXT_COLOR), ('×', BTN_DARK, ACCENT_COLOR),
            ('4', BTN_DARK, TEXT_COLOR), ('5', BTN_DARK, TEXT_COLOR), ('6', BTN_DARK, TEXT_COLOR), ('-', BTN_DARK, ACCENT_COLOR),
            ('1', BTN_DARK, TEXT_COLOR), ('2', BTN_DARK, TEXT_COLOR), ('3', BTN_DARK, TEXT_COLOR), ('+', BTN_DARK, ACCENT_COLOR),
            ('Graph', BTN_DARK, TEXT_COLOR), ('0', BTN_DARK, TEXT_COLOR), ('.', BTN_DARK, TEXT_COLOR), ('=', ACCENT_COLOR, "#000000")
        ]
        
        row_val = 1
        col_val = 0
        for (text, bg, fg) in buttons:
            hover_c = BTN_HOVER if bg == BTN_DARK else "#ff6666" if text == 'C' else "#ffe34d"
            
            # Encapsulate in frame to simulate padding/margin easily in pure tk if needed
            # Here we just use grid padx/y
            btn = tk.Button(
                self.keypad_frame, text=text, font=("Inter", 20, "bold"),
                bg=bg, fg=fg, activebackground=hover_c, activeforeground=fg,
                relief="flat", bd=0,
                command=lambda t=text: self.handle_click(t)
            )
            btn.grid(row=row_val, column=col_val, sticky="nsew", padx=3, pady=3)
            self.bind_hover(btn, bg, hover_c)
            
            col_val += 1
            if col_val > 3:
                col_val = 0
                row_val += 1

        # Scientific Panel (Hidden initially)
        self.sci_frame = tk.Frame(self, bg="#181818")
        sci_buttons = ['sin', 'cos', 'tan', 'sqrt', 'log', 'ln', '(', ')', '^', 'pi', 'e', 'x']
        
        for i in range(3):
            self.sci_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            self.sci_frame.grid_columnconfigure(i, weight=1)
            
        r, c = 0, 0
        for text in sci_buttons:
            btn = tk.Button(
                self.sci_frame, text=text, font=("Inter", 14),
                bg=BTN_DARK, fg=TEXT_COLOR, activebackground=BTN_HOVER,
                activeforeground=TEXT_COLOR, relief="flat", bd=0,
                command=lambda t=text: self.handle_click(t)
            )
            btn.grid(row=r, column=c, sticky="nsew", padx=2, pady=2)
            self.bind_hover(btn, BTN_DARK, BTN_HOVER)
            c += 1
            if c > 3:
                c = 0
                r += 1

        self.sci_visible = False
        
        # History Panel
        self.history_frame = tk.Frame(self, bg="#181818")
        self.history_text = tk.Text(
            self.history_frame, font=("Inter", 12), width=40, height=8, 
            bg="#181818", fg=TEXT_COLOR, bd=0, highlightthickness=0
        )
        self.history_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        export_btn = tk.Button(
            self.history_frame, text="Export History", font=("Inter", 10, "bold"), 
            bg=ACCENT_COLOR, fg="#000", activebackground="#ffe34d", activeforeground="#000",
            relief="flat", bd=0, command=self.export_history
        )
        export_btn.pack(pady=10)
        self.bind_hover(export_btn, ACCENT_COLOR, "#ffe34d")
        
        self.history_visible = False

    def handle_click(self, char):
        current = self.display_var.get()
        
        if current == "Error" or current == "0":
            if char not in ['+', '-', '×', '÷', '^', '%', '=', 'C', '⌫', 'Graph']:
                current = ""
            elif current == "Error":
                current = "0"
            
        if char == 'C':
            self.display_var.set("0")
            self.preview_label.configure(text="")
        elif char == '⌫':
            new_val = current[:-1]
            self.display_var.set(new_val if new_val else "0")
            self.update_preview(new_val)
        elif char == '=':
            self.evaluate()
        elif char == 'Graph':
            self.open_graph()
        else:
            if current and char in ['+', '-', '×', '÷', '^', '%'] and current[-1] in ['+', '-', '×', '÷', '^', '%']:
                current = current[:-1]
            self.display_var.set(current + char)
            self.update_preview(current + char)

    def handle_special(self, op):
        current = self.display_var.get()
        if op == "MC":
            self.logic.memory_clear()
        elif op == "MR":
            val = self.logic.memory_recall()
            if current == "0":
                self.display_var.set(val)
            else:
                self.display_var.set(current + val)
        elif op == "M+":
            self.logic.memory_add(current)
        elif op == "M-":
            self.logic.memory_subtract(current)
        elif op == "Hist":
            self.toggle_history()
        elif op == "Sci":
            self.toggle_scientific()

    def update_preview(self, expr):
        if any(op in expr for op in ['+', '-', '×', '÷', '^', 'sin', 'cos', 'tan', 'sqrt', 'log', '(']):
            res = self.logic.evaluate(expr, is_preview=True)
            self.preview_label.configure(text=res if 'x' not in expr else "y = f(x)")
        else:
            self.preview_label.configure(text="")

    def evaluate(self):
        expr = self.display_var.get()
        if 'x' in expr:
            self.open_graph()
            return
            
        res = self.logic.evaluate(expr)
        
        if res.startswith("Error") or res == "":
            self.trigger_error()
        else:
            self.history.append(f"{expr} = {res}")
            if len(self.history) > 5:
                self.history.pop(0)
            self.history_label.configure(text=f"{expr} =")
            self.display_var.set(res)
            self.preview_label.configure(text="")
            self.update_history_panel()

    def update_history_panel(self):
        self.history_text.delete("1.0", "end")
        for item in reversed(self.history):
            self.history_text.insert("end", item + "\n")

    def toggle_scientific(self):
        if self.sci_visible:
            self.sci_frame.pack_forget()
            self.geometry("400x650")
        else:
            if self.history_visible:
                self.toggle_history()
            self.geometry("400x800")
            self.sci_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.sci_visible = not self.sci_visible

    def toggle_history(self):
        if self.history_visible:
            self.history_frame.pack_forget()
            self.geometry(f"400x{800 if self.sci_visible else 650}")
        else:
            if self.sci_visible:
                self.toggle_scientific()
            self.geometry("400x820")
            self.history_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
            self.update_history_panel()
        self.history_visible = not self.history_visible

    def open_graph(self):
        expr = self.display_var.get()
        if not expr or expr == "0" or expr == "Error":
            self.trigger_error()
            return
        GraphWindow(self, expr)

    def trigger_error(self):
        original_color = self.display.cget("fg")
        self.display.configure(fg="#ff4444")
        
        def shake(count):
            if count > 0:
                dx = 5 if count % 2 == 0 else -5
                self.geometry(f"+{self.winfo_x() + dx}+{self.winfo_y()}")
                self.after(50, shake, count - 1)
            else:
                self.display.configure(fg=original_color)
                self.display_var.set("Error")
                
        self.after(10, shake, 6)

    def export_history(self):
        try:
            with open("history.txt", "w") as f:
                for item in self.history:
                    f.write(item + "\n")
            self.history_text.insert("end", "\n-- Exported to history.txt --")
        except:
            pass

    def handle_keypress(self, event):
        key = event.char
        keysym = event.keysym
        
        valid_chars = '0123456789.+-*/^%()'
        if key in valid_chars:
            if key == '*': key = '×'
            elif key == '/': key = '÷'
            self.handle_click(key)
        elif keysym == "Return" or keysym == "KP_Enter":
            self.evaluate()
        elif keysym == "BackSpace":
            self.handle_click('⌫')
        elif keysym == "Escape" or keysym == "c" or keysym == "C":
            self.handle_click('C')

if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
