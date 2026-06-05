import sys
import tkinter as tk
from tkinter import scrolledtext
import os
import subprocess

def main():
    root = tk.Tk()
    root.title("Python Math Evaluator")
    root.attributes('-topmost', True)
    
    # macOS bulletproof focus hack: force the OS to give this window keyboard focus
    if sys.platform == 'darwin':
        script = f'''
        tell application "System Events"
            set frontmost of the first process whose unix id is {os.getpid()} to true
        end tell
        '''
        subprocess.run(['osascript', '-e', script])
    
    root.focus_force()
    root.configure(bg="#1e1e1e")
    
    txt = scrolledtext.ScrolledText(root, width=65, height=12, font=("Menlo", 14), background="#1e1e1e", foreground="white", insertbackground="white")
    txt.pack(padx=10, pady=10)
    
    # macOS Tkinter Paste Fix: Sometimes pasting rich text strips newlines and replaces them with spaces.
    # This explicit binding forces Tkinter to grab plain text from the clipboard.
    def paste_plain_text(event):
        try:
            text = root.clipboard_get()
            txt.insert(tk.INSERT, text)
        except tk.TclError:
            pass
        return "break"
        
    txt.bind('<Command-v>', paste_plain_text)
    txt.bind('<Control-v>', paste_plain_text)
    
    def on_run(event=None):
        code = txt.get("1.0", tk.END).strip()
        with open("/tmp/py_code.txt", "w") as f:
            f.write(code)
        root.destroy()
        return "break"
        
    btn = tk.Button(root, text="Run Code (Cmd/Ctrl + Enter)", command=on_run)
    btn.pack(pady=5)
    
    txt.bind('<Command-Return>', on_run)
    txt.bind('<Control-Return>', on_run)
    txt.bind('<Mod1-Return>', on_run)
    txt.bind('<Meta-Return>', on_run)
    
    txt.focus_set()
    root.mainloop()

if __name__ == "__main__":
    main()
