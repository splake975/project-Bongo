import subprocess
import time
import sys
import signal
import os

def startOCRServer()->subprocess.Popen:
    """
    Start the OCR server as a subprocess.
    """
    serverPath = "./ocrProd/pyfiles/ocrServer.py"

    try:
        # Start the server in a subprocess
        server_process = subprocess.Popen(
            ".\\ocrProd\\codeOCR.bat",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        print("OCR server started.")
        return server_process
    except Exception as e:
        print(f"Failed to start the server: {e}")
        return None

def stopOCRServer(server_process:subprocess.Popen):
    """
    Stop the OCR server subprocess.
    """
    if server_process:
        print("Stopping the OCR server...")
        try:
            os.kill(server_process.pid,signal.SIGINT)
            server_process.wait(2)
        except:
            pass
        server_process.terminate()  # Gracefully terminate the server
        try:
            # Wait for the server to terminate (timeout after 5 seconds)
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Forcefully kill the server if it doesn't terminate
            server_process.kill()
            print("Server forcefully terminated.")
        print("OCR server stopped.")

def startOCRServerMain():
    # Start the server
    server_process = startOCRServer()
    if not server_process:
        sys.exit(1)

    try:
        # Keep the main script running while the server is active
        print("Press Ctrl+C to stop the server.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        # Stop the server when Ctrl+C is pressed
        stopOCRServer(server_process)

if __name__ == "__main__":
    startOCRServerMain()