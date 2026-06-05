function initUi()
  app.registerUi({["menu"] = "Run Python Math", ["callback"] = "run_python", ["accelerator"] = "<Control><Shift>P"})
end

function get_os_name()
  local os_name = "Linux"
  local f = io.popen("uname -s")
  if f then
    os_name = f:read("*l")
    f:close()
  end
  return os_name:gsub("%s+", "")
end

function get_python_exe(plugin_dir)
  local cache_file = plugin_dir .. "python_path.cache"
  local f = io.open(cache_file, "r")
  if f then
    local exe = f:read("*l")
    f:close()
    -- Quick check if it's still valid
    if os.execute(string.format('"%s" -c "import numpy" >/dev/null 2>&1', exe)) == 0 or os.execute(string.format('"%s" -c "import numpy" >/dev/null 2>&1', exe)) == true then
      return exe
    end
  end
  
  -- Auto-detect python
  local detect_script = plugin_dir .. "detect_python.sh"
  os.execute(string.format('chmod +x "%s"', detect_script))
  local handle = io.popen(string.format('bash "%s"', detect_script))
  if handle then
    local result = handle:read("*l")
    handle:close()
    if result and result ~= "" then
      local f_out = io.open(cache_file, "w")
      if f_out then
        f_out:write(result)
        f_out:close()
      end
      return result
    end
  end
  
  -- Fallback
  return "python3"
end

function run_python()
  local plugin_dir = debug.getinfo(1).source:match("@?(.*/)")
  local gui_script = plugin_dir .. "gui.py"
  local eval_script = plugin_dir .. "xournal_eval.py"
  local python_exe = get_python_exe(plugin_dir)
  local os_name = get_os_name()
  
  -- We MUST use env -i to wipe Xournal++'s GTK variables so Tkinter uses Cocoa correctly on macOS.
  local path = os.getenv("PATH") or "/usr/bin:/bin:/usr/sbin:/sbin"
  local home = os.getenv("HOME") or ""
  
  -- 1. Show the multiline GUI
  os.execute("rm -f /tmp/py_code.txt /tmp/py_out.png")
  local cmd_gui = string.format('env -i PATH="%s" HOME="%s" "%s" "%s"', path, home, python_exe, gui_script)
  os.execute(cmd_gui)
  
  -- 2. If the user typed code and clicked Run, evaluate it!
  local f = io.open("/tmp/py_code.txt", "r")
  if not f then return end
  local code = f:read("*a")
  f:close()
  if code == "" then return end
  
  local cmd_eval = string.format('env -i PATH="%s" HOME="%s" "%s" "%s"', path, home, python_exe, eval_script)
  os.execute(cmd_eval)
  
  -- 3. Check for output image and copy to clipboard
  local f2 = io.open("/tmp/py_out.png", "r")
  if f2 then
    f2:close()
    
    if os_name == "Darwin" then
      os.execute('osascript -e \'set the clipboard to (read (POSIX file "/tmp/py_out.png") as TIFF picture)\'')
      os.execute([[osascript << 'EOF'
try
  delay 0.2
  tell application "System Events"
    repeat with proc in (every application process)
      if (name of proc) contains "xournal" or (name of proc) contains "Xournal" then
        set frontmost of proc to true
        delay 0.2
        keystroke "v" using {command down}
        exit repeat
      end if
    end repeat
  end tell
end try
EOF]])
    else
      -- Linux
      os.execute('xclip -selection clipboard -target image/png -i /tmp/py_out.png')
      os.execute('sleep 0.2 && xdotool key ctrl+v')
    end
  else
    if os_name == "Darwin" then
      os.execute('osascript -e \'display notification "Python encountered an error or no output generated." with title "Python Math Error"\'')
    else
      os.execute('notify-send "Python Math Error" "Python encountered an error or no output generated."')
    end
  end
end
