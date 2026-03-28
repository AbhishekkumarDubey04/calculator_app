# Premium Calculator App

A modern, visually stunning desktop calculator built entirely in Python using standard `tkinter`. Designed with a premium `#121212` dark mode aesthetic and vibrant `#FFD60A` neon accents, this calculator breaks the mold of traditional, dated Tkinter interfaces by utilizing flattened widget styles and custom hover logic.

## Features

*   **Dark Mode & Neon Accents:** A completely custom dark theme built on top of standard Tkinter.
*   **Scientific Operations:** A modular, expandable interface that hides scientific functions (`sin`, `cos`, `tan`, `log`, `ln`, `sqrt`, `^`, `pi`, `e`) until needed.
*   **Real-time Previews:** The calculator predicts and evaluates your equations on the fly, showing complex functions as $y = f(x)$ or resolving basic arithmetic live as you type.
*   **Native Graph Plotting:** A separate pop-up canvas plots valid algebraic formulas containing the variable `x` (e.g. `sin(x) * x`) purely using `math` logic and `Tkinter.Canvas`.
*   **Calculation History:** Easily expand a side panel to view your last equations, copy results, and export your session history to a `.txt` file.
*   **Interactive Error Handling:** Inputting invalid mathematical syntax triggers a visual error featuring a smooth `.after()` window-shake animation and a striking crimson text highlight.
*   **Memory Variables:** Classic memory storage actions (`MC`, `MR`, `M+`, `M-`) fully implemented.
*   **Zero Dependencies:** Designed to work directly with Python's standard library. No `matplotlib`, `numpy`, or `customtkinter` needed.

## Installation & Running

Since this project requires no external build tools or pip modules, you can launch it instantly on any system with Python 3.

```bash
# Clone the repository
git clone https://github.com/USERNAME/premium-calculator.git

# Navigate to the project directory
cd premium-calculator

# Run the app
python main.py
```

## Tech Stack
*   **Language:** Pure Python 3
*   **GUI Framework:** `tkinter`
*   **Math Engine:** Python's built-in `eval` operating rigorously within a confined, safe dictionary mapping internal `math` module functions.

## ScreenShots
<img width="504" height="852" alt="image" src="https://github.com/user-attachments/assets/1d558d62-b703-453a-8856-ff6282932675" />
<img width="508" height="1012" alt="image" src="https://github.com/user-attachments/assets/11e0c087-935e-4476-935a-820632775985" />


