import os
import subprocess
import gdown

# Define installation directories
install_dir = 'C:\\ffmpeg'
bin_dir = os.path.join(install_dir, 'bin')

# Create directories if they don't exist
os.makedirs(bin_dir, exist_ok=True)

# Download ffmpeg and ffprobe
output_file = os.path.join(bin_dir, "ffmpeg.exe")
gdown.download(f"https://drive.google.com/uc?id=1_dHx-GS-3f2ZsNm42pZ5ze50XYqxLb7-", output_file, quiet=False)
output_file = os.path.join(bin_dir, "ffprobe.exe")
gdown.download(f"https://drive.google.com/uc?id=1pYKDIL4F6kNsXmKwUfjJlu8H_YD4Equ6", output_file, quiet=False)

# Add /bin directory to the PATH environment variable
bin_path = os.path.join("C:\\", "ffmpeg", "bin")
current_path = os.environ.get("PATH", "")
if bin_path not in current_path:
    new_path = f"{bin_path};{current_path}"
    subprocess.call(["setx", "PATH", new_path])
    print("FFmpeg has been installed and added to the PATH.")


print("Installation completed successfully.")
print("You may close out of the installer.")