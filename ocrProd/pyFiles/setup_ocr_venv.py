import os
import subprocess
import sys

def add_pyenv_to_path():
    """Add pyenv-win to the system PATH."""
    pyenv_bin = os.path.expanduser("~/.pyenv/pyenv-win/bin")
    pyenv_shims = os.path.expanduser("~/.pyenv/pyenv-win/shims")

    if pyenv_bin not in os.environ["PATH"]:
        os.environ["PATH"] = f"{pyenv_bin};{os.environ['PATH']}"
    if pyenv_shims not in os.environ["PATH"]:
        os.environ["PATH"] = f"{pyenv_shims};{os.environ['PATH']}"

    print("Added pyenv-win to PATH.")

def install_pyenv_win():
    """Install pyenv-win if it is not already installed."""
    try:
        # Check if pyenv is installed
        subprocess.run(["pyenv", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("pyenv-win is already installed.")
    except FileNotFoundError:
        print("pyenv-win is not installed. Installing pyenv-win...")
        # Download the pyenv-win installer script using curl
        subprocess.run(
            [
                "curl", "-o", "install-pyenv-win.ps1",
                "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1"
            ], check=True
        )
        # Run the installer script using PowerShell
        subprocess.run(
            [
                "powershell", "-ExecutionPolicy", "Bypass", "-File", "install-pyenv-win.ps1"
            ], check=True
        )
        print("pyenv-win installed successfully.")
        # Add pyenv-win to PATH
        add_pyenv_to_path()

def check_python_version():
    """Check if Python 3.12.4 is installed using pyenv-win. If not, install it."""
    try:
        # Check if Python 3.12.4 is installed
        result = subprocess.run(["pyenv", "versions"], capture_output=True, text=True, shell=True)
        if "3.12.4" not in result.stdout:
            print("Python 3.12.4 is not installed. Installing it using pyenv-win...")
            subprocess.run(["pyenv", "install", "3.12.4"], check=True, shell=True)
        print("Python 3.12.4 is available.")
    except subprocess.CalledProcessError as e:
        print(f"Error checking or installing Python 3.12.4: {e}")
        sys.exit(1)

def create_venv():
    """Create a virtual environment with Python 3.12.4 using pyenv-win."""
    venv_dir = "ocr_venv"
    if not os.path.exists(venv_dir):
        print("Creating virtual environment with Python 3.12.4...")
        # Use pyenv-win to set the local Python version to 3.12.4 (specific to CWD)
        subprocess.run(["pyenv", "local", "3.12.4"], check=True, shell=True)
        # Create the virtual environment
        subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
    else:
        print("Virtual environment already exists.")
    return venv_dir

def install_dependencies(venv_dir):
    """Install Python dependencies in the virtual environment."""
    pip_path = os.path.join(venv_dir, "Scripts", "pip.exe")
    print("Installing Python dependencies...")
    subprocess.run([pip_path, "install", "easyocr", "opencv-python"], check=True)

def main():
    print("Setting up OCR environment...")

    # Install pyenv-win if not already installed
    install_pyenv_win()

    # Check and install Python 3.12.4 if necessary
    check_python_version()

    # Create virtual environment with Python 3.12.4
    venv_dir = create_venv()

    # Install dependencies
    install_dependencies(venv_dir)

    print("Setup complete. Activate the virtual environment using:")
    print(f"  .\\{venv_dir}\\Scripts\\activate")

if __name__ == "__main__":
    main()