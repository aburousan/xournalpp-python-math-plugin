# Xournal++ Python Math Plugin

A powerful, cross-platform(macos and linux) Xournal++ plugin that lets you write multi-line Python code, solve complex equations using SymPy, and generate transparent Matplotlib graphs directly inside your Xournal++ documents.

## Features
- **Jupyter-like Multi-line Execution**: Write multiple lines of Python code natively. The final expression or plot is automatically evaluated and rendered.
- **Beautiful LaTeX Rendering**: High-res, automatically formatted LaTeX math generation for SymPy output.
- **Seamless Plotting**: Native Matplotlib and SymPy plot support. Backgrounds are automatically forced to be transparent so they sit perfectly on your Xournal++ page.
- **Auto-Environment Detection**: The plugin dynamically scans your system (including Conda environments) to find a Python executable equipped with the necessary scientific libraries.
- **Pre-loaded Libraries**: No need to write imports. `sp` (SymPy), `np` (NumPy), `plt` (Matplotlib), `scipy` (SciPy), and common variables (`x, y, z, t, a, b, c`) are pre-imported automatically.

## Requirements

### Python Dependencies
The plugin requires a Python environment with the following packages installed:
```bash
pip install numpy scipy sympy matplotlib
```
*(Conda environments are highly recommended and are prioritized during auto-detection).*

### System Dependencies
- **macOS**: Works out of the box (uses native AppleScript for clipboard handling).
- **Linux**: Requires `xclip` and `xdotool` to manipulate the clipboard and simulate the paste keystroke.
  ```bash
  sudo apt install xclip xdotool
  ```

## Installation
1. Clone or download this repository.
2. Copy the entire repository folder into your Xournal++ plugins directory and name it `python_math`:
   - **Linux:** `~/.config/xournalpp/plugins/python_math`
   - **macOS:** `~/.config/xournalpp/plugins/python_math`
3. Open Xournal++, go to **Plugin Manager**, and enable the `python_math` plugin.
4. Restart Xournal++.

## Usage
1. Press `Ctrl + Shift + P` inside Xournal++ to open the Python Math Evaluator window.
2. Type your Python code.
3. Press `Cmd + Enter` (macOS) or `Ctrl + Enter` (Linux), or click the "Run Code" button.
4. The result (equation or plot) will be automatically pasted onto your active page!

### Example 1: Solving an ODE
```python
# No imports needed!
ode = sp.Eq(y.diff(x, x) + y, 0)
sp.dsolve(ode, y)
```

### Example 2: Transparent Matplotlib Plot
```python
x_vals = np.linspace(-10, 10, 500)
y_vals = np.sin(x_vals) * np.exp(-0.1 * np.abs(x_vals))

plt.figure(figsize=(7, 4))
plt.plot(x_vals, y_vals, color='blue', linewidth=2)
plt.title("Damped Sine Wave")
plt.grid(color='gray', linestyle='--', alpha=0.5)
```

## Author
**K.A.Rousan**
