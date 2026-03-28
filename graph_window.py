import tkinter as tk
import math

class GraphWindow(tk.Toplevel):
    def __init__(self, master, function_str):
        super().__init__(master)
        
        self.title("Graph Plotting")
        self.geometry("600x500")
        self.configure(bg="#121212")
        
        self.function_str = function_str
        self.width = 560
        self.height = 400
        
        self.setup_ui()
        self.plot_graph()

    def setup_ui(self):
        self.title_label = tk.Label(
            self, text=f"Graph: y = {self.function_str}", 
            font=("Inter", 16, "bold"), fg="#FFD60A", bg="#121212"
        )
        self.title_label.pack(pady=10)
        
        self.canvas_frame = tk.Frame(self, bg="#181818", bd=0)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.canvas = tk.Canvas(
            self.canvas_frame, width=self.width, height=self.height, 
            bg="#181818", highlightthickness=0
        )
        self.canvas.pack(padx=20, pady=20, expand=True)
        
        # Draw axes
        self.canvas.create_line(0, self.height/2, self.width, self.height/2, fill="#555555", dash=(4, 4))
        self.canvas.create_line(self.width/2, 0, self.width/2, self.height, fill="#555555", dash=(4, 4))

    def plot_graph(self):
        try:
            safe_dict = {
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'sqrt': math.sqrt,
                'log': math.log10,
                'ln': math.log,
                'exp': math.exp,
                'abs': abs,
                'pi': math.pi,
                'e': math.e
            }
            
            expr = self.function_str.replace('^', '**').replace('×', '*').replace('÷', '/')
            
            x_min, x_max = -10, 10
            points = []
            steps = 400
            
            for i in range(steps + 1):
                x = x_min + (x_max - x_min) * (i / steps)
                safe_dict['x'] = x
                
                try:
                    y = eval(expr, {"__builtins__": None}, safe_dict)
                    points.append((x, y))
                except (ValueError, ZeroDivisionError, OverflowError):
                    points.append((x, None))
                    
            valid_y = [p[1] for p in points if p[1] is not None]
            if not valid_y:
                raise Exception("No valid points to plot in range [-10, 10]")
                
            y_min, y_max = min(valid_y), max(valid_y)
            
            if y_max - y_min < 1:
                y_max += 5
                y_min -= 5
                
            if y_max - y_min > 200:
                y_max = 100
                y_min = -100

            scaled_points = []
            for ix, (x, y) in enumerate(points):
                if y is None or y > y_max or y < y_min:
                    continue
                    
                cx = (x - x_min) / (x_max - x_min) * self.width
                cy = self.height - ((y - y_min) / (y_max - y_min) * self.height)
                scaled_points.append((cx, cy))
            
            if len(scaled_points) > 1:
                for i in range(len(scaled_points) - 1):
                    p1 = scaled_points[i]
                    p2 = scaled_points[i+1]
                    if abs(p1[1] - p2[1]) < self.height * 0.8:
                        self.canvas.create_line(p1[0], p1[1], p2[0], p2[1], fill="#FFD60A", width=2)
                        
        except Exception as e:
            self.canvas.create_text(
                self.width/2, self.height/2, 
                text=f"Plot Error: {str(e)}", 
                fill="#ff4444", font=("Inter", 12)
            )
