import sys
import sympy as sp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import ast
import io
import contextlib
import traceback
import numpy as np
import scipy

# Force completely transparent backgrounds for all plots (Matplotlib and SymPy)
plt.rcParams.update({
    "savefig.transparent": True,
    "axes.facecolor": "none",
    "figure.facecolor": "none",
    "savefig.dpi": 300,
    "font.size": 14
})

# Pre-define common symbols globally so they are included in globals().copy()
x, y, z, t = sp.symbols('x y z t')
a, b, c = sp.symbols('a b c')

def create_text_image(text, color='black'):
    plt.figure(figsize=(8, 4))
    plt.text(0.01, 0.99, text, fontsize=14, ha='left', va='top', family='monospace', color=color, wrap=True)
    plt.axis('off')
    plt.savefig('/tmp/py_out.png', bbox_inches='tight', transparent=True, dpi=300)
    plt.close()

def run_code(code):
    try:
        tree = ast.parse(code)
    except Exception as e:
        create_text_image(f"Syntax Error:\n{traceback.format_exc()}", 'red')
        return
        
    if not tree.body:
        return
        
    last_node = tree.body[-1]
    env = globals().copy()
    
    stdout_capture = io.StringIO()
    res = None
    
    try:
        with contextlib.redirect_stdout(stdout_capture):
            if isinstance(last_node, ast.Expr):
                if len(tree.body) > 1:
                    exec_tree = ast.Module(body=tree.body[:-1], type_ignores=[])
                    exec(compile(exec_tree, filename="<ast>", mode="exec"), env)
                
                eval_tree = ast.Expression(body=last_node.value)
                res = eval(compile(eval_tree, filename="<ast>", mode="eval"), env)
            else:
                exec(compile(tree, filename="<ast>", mode="exec"), env)
                res = None
                
        # If res is None, check stdout
        if res is None:
            printed = stdout_capture.getvalue().strip()
            if printed:
                create_text_image(printed, 'black')
                return
            
            if plt.get_fignums():
                fig = plt.gcf()
                fig.savefig('/tmp/py_out.png', transparent=True, dpi=300)
                plt.close(fig)
                return
                
        # 1. Check if res is explicitly a SymPy plot
        if hasattr(res, 'save') and 'plot' in str(type(res)).lower():
            res.save('/tmp/py_out.png')
            return
            
        # 2. If any Matplotlib figures were generated (like plt.plot()), save the plot!
        if plt.get_fignums():
            fig = plt.gcf()
            fig.savefig('/tmp/py_out.png', transparent=True, dpi=300)
            plt.close(fig)
            return
            
        # 3. Otherwise, render the result as LaTeX math
        if res is not None:
            latex_str = f"${sp.latex(res)}$"
            fig, ax = plt.subplots(figsize=(0.01, 0.01))
            ax.text(0, 0, latex_str, fontsize=48, ha='center', va='center')
            ax.axis('off')
            plt.savefig('/tmp/py_out.png', bbox_inches='tight', transparent=True, dpi=300)
            plt.close(fig)
            
    except Exception as e:
        create_text_image(f"Execution Error:\n{traceback.format_exc()}", 'red')

try:
    if os.path.exists('/tmp/py_code.txt'):
        with open('/tmp/py_code.txt', 'r') as f:
            code = f.read()
        run_code(code)
except Exception as e:
    create_text_image(f"Fatal Error:\n{traceback.format_exc()}", 'red')
