import os
import platform
import subprocess


def create_disk_image():
    """
    Creates a raw disk image (.img) file by copying a specified disk.
    Works on both Windows and Linux platforms.
    """
    print("=== Disk to IMG Creator ===")

    # Determine platform
    current_os = platform.system().lower()
    is_windows = current_os == "windows"
    print(f"Detected OS: {platform.system()}")

    # Ask for the source disk name
    if is_windows:
        print("For Windows, the disk name should be in the format '\\\\.\\PhysicalDriveX' (e.g., '\\\\.\\PhysicalDrive1').")
    else:
        print("For Linux, the disk name should be in the format '/dev/sdX' (e.g., '/dev/sda').")

    source_disk = input("Enter the source disk name: ").strip()
    if is_windows and not source_disk.startswith(r"\\.\"):
        print("Error: Invalid disk name. Windows disk names should start with '\\\\.\\'.")
        return
    elif not is_windows and not source_disk.startswith("/dev/"):
        print("Error: Invalid disk name. Linux disk names should start with '/dev/'.")
        return

    # Ask for the output image file location
    output_path = input("Enter the output .img file path (e.g., '/path/to/disk_backup.img'): ").strip()
    if not output_path.lower().endswith(".img"):
        print("Error: The output file should have a '.img' extension.")
        return

    # Confirm paths
    print(f"Source Disk: {source_disk}")
    print(f"Output Path: {output_path}")
    confirm = input("Are these correct? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation canceled.")
        return

    # Construct the command
    dd_command = []
    if is_windows:
        # Use `dd` for Windows
        dd_command = [
            "dd",
            f"if={source_disk}",
            f"of={output_path}",
            "bs=4M",
            "--progress"
        ]
    else:
        # Use native `dd` on Linux
        dd_command = [
            "dd",
            f"if={source_disk}",
            f"of={output_path}",
            "bs=4M",
            "status=progress"
        ]

    # Execute the command
    try:
        print("Creating disk image, please wait...")
        subprocess.run(dd_command, check=True)
        print(f"Disk image created successfully: {output_path}")
    except FileNotFoundError:
        print("Error: `dd` command not found. Please ensure `dd` is installed and accessible in your PATH.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while creating the disk image: {e}")
    except PermissionError:
        print("Error: This operation requires administrative/root privileges. Please run the script as an administrator.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    create_disk_image()
