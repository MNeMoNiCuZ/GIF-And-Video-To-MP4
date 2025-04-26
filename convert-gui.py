import os
import subprocess
import sys
from pathlib import Path
import argparse

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ImportError:
    print("Error: tkinterdnd2 is not installed. Install it using: pip install tkinterdnd2")
    print("GUI mode is unavailable, but command-line mode can still be used.")
    tk = None

def check_writable(directory):
    """Check if the directory is writable."""
    directory = Path(directory)
    try:
        directory.mkdir(parents=True, exist_ok=True)
        test_file = directory / ".test_write"
        test_file.touch()
        test_file.unlink()
        return True
    except (PermissionError, OSError) as e:
        print(f"Error: Cannot write to directory {directory}: {str(e)}")
        return False

def fix_video_encoding(input_path, output_path, suffix="_fixed"):
    """Re-encode video to ensure web compatibility with minimal quality loss using FFmpeg"""
    try:
        input_path = Path(input_path).resolve()
        output_path = Path(output_path).resolve() / input_path.with_stem(input_path.stem + suffix).name
        
        if not check_writable(output_path.parent):
            print(f"Error: Output directory {output_path.parent} is not writable")
            return False
        
        # Get video information to check dimensions
        probe_cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-hide_banner"
        ]
        
        try:
            # This will fail with return code 1, but that's expected
            subprocess.run(probe_cmd, stderr=subprocess.PIPE, text=True, check=False)
        except Exception:
            pass
        
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Ensure even dimensions
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "17",  # Lower CRF for high quality
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            "-pix_fmt", "yuv420p",
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print(f"Successfully fixed encoding: {input_path} -> {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error fixing encoding for {input_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: FFmpeg is not installed or not found in PATH. Please install FFmpeg.")
        return False
    except Exception as e:
        print(f"Unexpected error fixing encoding for {input_path}: {str(e)}")
        return False

def convert_gif_to_mp4(input_path, output_path, suffix=""):
    """Convert GIF to MP4 with appropriate encoding"""
    try:
        input_path = Path(input_path).resolve()
        output_path = Path(output_path).resolve() / input_path.with_stem(input_path.stem + suffix).with_suffix('.mp4').name
        
        if not check_writable(output_path.parent):
            print(f"Error: Output directory {output_path.parent} is not writable")
            return False
        
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", str(input_path),
            "-vf", "scale=trunc(iw/2)*2:trunc(ih/2)*2",  # Ensure even dimensions
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-preset", "fast",
            "-crf", "17",  # Lower CRF for high quality
            "-y",
            str(output_path)
        ]
        
        result = subprocess.run(ffmpeg_cmd, check=True, capture_output=True, text=True)
        print(f"Successfully converted GIF: {input_path} -> {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"Error converting GIF for {input_path}: {e.stderr}")
        return False
    except FileNotFoundError:
        print("Error: FFmpeg is not installed or not found in PATH. Please install FFmpeg.")
        return False
    except Exception as e:
        print(f"Unexpected error converting GIF for {input_path}: {str(e)}")
        return False

def process_file(file_path, output_path, suffix):
    """Process a file based on its type"""
    file_path = Path(file_path).resolve()
    if not file_path.is_file():
        print(f"Error: File not found: {file_path}")
        return False
        
    # Use suffix to check extension
    if file_path.suffix.lower() in ('.mp4', '.mov', '.avi', '.mkv', '.wmv'):
        return fix_video_encoding(file_path, output_path, suffix)
    elif file_path.suffix.lower() == '.gif':
        return convert_gif_to_mp4(file_path, output_path, suffix)
    else:
        print(f"Skipping unsupported file: {file_path}")
        return False

def process_input(input_path, output_path, suffix):
    """Process either a single file or all relevant files in a folder"""
    input_path = Path(input_path).resolve()
    output_path = Path(output_path).resolve()
    
    if not check_writable(output_path):
        print(f"Error: Output directory {output_path} is not writable")
        return False, 0, 0
    
    output_path.mkdir(parents=True, exist_ok=True)
    
    success_count = 0
    total_count = 0
    
    if input_path.is_file():
        total_count = 1
        if process_file(input_path, output_path, suffix):
            success_count += 1
    elif input_path.is_dir():
        supported_extensions = ('.mp4', '.mov', '.avi', '.mkv', '.wmv', '.gif')
        files = [f for f in input_path.iterdir() if f.is_file() and f.suffix.lower() in supported_extensions]
        total_count = len(files)
        for file_path in files:
            if process_file(file_path, output_path, suffix):
                success_count += 1
    else:
        print(f"Error: Input path does not exist: {input_path}")
        return False, 0, 0
        
    return success_count == total_count, success_count, total_count

def handle_drop(event, output_path, suffix):
    """Handle dropped files in GUI mode"""
    files = root.tk.splitlist(event.data)
    success_count = 0
    total_count = len(files)
    
    output_path = Path(output_path).resolve()
    output_path.mkdir(parents=True, exist_ok=True)
    
    for file_path in files:
        if process_file(file_path, output_path, suffix):
            success_count += 1
    
    messagebox.showinfo(
        "Processing Complete",
        f"Processed {success_count} out of {total_count} file(s) successfully."
    )

def run_gui(output_path, suffix):
    """Run the GUI interface"""
    if tk is None:
        print("Error: Cannot run GUI mode without tkinterdnd2 installed")
        sys.exit(1)
        
    global root
    root = TkinterDnD.Tk()
    root.title("Video & GIF Converter")
    root.geometry("500x200")
    
    label = tk.Label(
        root,
        text="Drag and drop video or GIF files here to convert to mp4",
        font=("Arial", 12),
        pady=20
    )
    label.pack(expand=True)
    
    supported_label = tk.Label(
        root,
        text="Supported formats: MP4, MOV, AVI, MKV, WMV, GIF",
        font=("Arial", 10),
        pady=5
    )
    supported_label.pack(expand=False)
    
    root.drop_target_register(DND_FILES)
    root.dnd_bind('<<Drop>>', lambda event: handle_drop(event, output_path, suffix))
    
    root.mainloop()

def run_command_line(input_path, output_path, suffix):
    """Process files from command line arguments"""
    success, success_count, total_count = process_input(input_path, output_path, suffix)
    
    if total_count == 0:
        print("No supported files found to process.")
    else:
        print(f"Processed {success_count} out of {total_count} file(s) successfully.")
    
    return success

def main():
    parser = argparse.ArgumentParser(description="Convert videos and GIFs to MP4")
    parser.add_argument(
        "--input-path",
        help="Input file or folder containing videos or GIFs",
        type=str
    )
    parser.add_argument(
        "--output-path",
        help="Output folder for processed files (default: same as input or current directory)",
        type=str,
        default="."
    )
    parser.add_argument(
        "--suffix",
        help="Suffix to add to output filenames (default: _fixed for videos, none for GIFs)",
        type=str,
        default="_fixed"
    )
    args = parser.parse_args()

    if not args.input_path:
        run_gui(args.output_path, args.suffix)
    else:
        sys.exit(0 if run_command_line(args.input_path, args.output_path, args.suffix) else 1)

if __name__ == "__main__":
    main()