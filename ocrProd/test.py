import subprocess

# hidewindow
startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

ocrSubprocess = subprocess.Popen([r"cmd.exe", "/c", r"ocrProd\test.bat"],
    stdout=subprocess.PIPE, 
    startupinfo=startupinfo,
    stderr=subprocess.PIPE, 
    creationflags=subprocess.CREATE_NO_WINDOW,
    shell=True,
    text=True)
stdout, stderr = ocrSubprocess.communicate()
print(f"{stdout.strip()=}")
print(stdout.strip())