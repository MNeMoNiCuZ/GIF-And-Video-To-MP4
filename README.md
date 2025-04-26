# GIFAndVideoToMP4

GIFAndVideoToMP4 is a versatile simple designed to convert GIFs and videos (MP4, MOV, AVI, MKV, WMV) to web-compatible MP4 format using FFmpeg. It supports both a drag-and-drop GUI interface and a command-line interface for batch processing.

![image](https://github.com/user-attachments/assets/8cfa38e2-e5a6-4200-92cf-0cb3092a29fc)

*Screenshot: GIFAndVideoToMP4 GUI interface*

## Features

- Converts GIFs to MP4 with high-quality encoding
- Re-encodes videos (MP4, MOV, AVI, MKV, WMV) for web compatibility
- Supports batch processing of files in a folder
- Customizable output filename suffix
- Drag-and-drop GUI interface for easy file conversion
- Command-line interface for automation and scripting
- Cross-platform support (Windows, macOS, Linux)
- Error handling for missing dependencies or permissions
- Ensures even dimensions and web-friendly encoding settings

## Requirements

- Python 3.6 or higher
- FFmpeg

## Installation

1. Clone or download this repository
2. Run `venv_create.bat` to set up your environment:
   - Choose your Python version when prompted
   - Accept the default virtual environment name (venv) or choose your own
   - Allow pip upgrade when prompted
   - Allow installation of dependencies from requirements.txt

The script will create:
- A virtual environment
- `venv_activate.bat` for activating the environment
- `venv_update.bat` for updating pip

3. Install FFmpeg:
   - **Windows**:
     - Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (e.g., `ffmpeg-release-essentials.zip`).
     - Extract and add the `bin` folder to your system PATH (e.g., `C:\ffmpeg\bin`).
     - Verify installation: `ffmpeg -version`.
   - **macOS**:
     - Install via Homebrew: `brew install ffmpeg`.
     - Verify installation: `ffmpeg -version`.
   - **Linux**:
     - Install via package manager, e.g., `sudo apt install ffmpeg` (Ubuntu/Debian) or `sudo dnf install ffmpeg` (Fedora).
     - Verify installation: `ffmpeg -version`.

## Usage

### GUI Mode

1. Activate the virtual environment:
   - Windows: `venv_activate.bat`
   - macOS/Linux: `source venv/bin/activate`
2. Run the application:
   ```bash
   python convert-gui.py
   ```
3. Drag and drop video or GIF files into the GUI window.
4. Converted files will be saved in the current directory with the default suffix `_fixed`.

### Command Line Mode

You can use the tool from the command line for single files, folders, or automation:

1. Activate the virtual environment (see above).
2. Run the script with options:

   ```bash
   python convert-gui.py --input-path <file-or-folder> --output-path <output-folder> [--suffix <suffix>]
   ```

   Common command-line options:
   ```
   --input-path    Input file or folder containing videos or GIFs
   --output-path   Output folder for processed files (default: current directory)
   --suffix        Suffix to add to output filenames (default: _fixed)
   ```

   Examples:
   - Convert a single GIF:
     ```bash
     python convert-gui.py --input-path input.gif --output-path output --suffix _converted
     ```
   - Convert a single video:
     ```bash
     python convert-gui.py --input-path input.mp4 --output-path output --suffix _converted
     ```
   - Convert all supported files in a folder:
     ```bash
     python convert-gui.py --input-path . --output-path output --suffix _converted
     ```

For a full list of options, run:
```bash
python convert-gui.py --help
```

## Output Organization

- Converted files are saved in the specified `--output-path` directory.
- Output filenames include the original name with the specified suffix (e.g., `input_converted.mp4`).
- For GIFs, the output is always `.mp4`; for videos, the original extension is preserved.

## Advanced Options

- **Custom Suffix**: Use `--suffix` to customize the output filename (e.g., `--suffix _web` for `input_web.mp4`).
- **Batch Processing**: Specify a folder with `--input-path` to process all supported files (`.mp4`, `.mov`, `.avi`, `.mkv`, `.wmv`, `.gif`).
- **Overwrite**: The script automatically overwrites existing output files with the same name.

## FFmpeg Requirements

- The tool relies on FFmpeg for video and GIF processing.
- Ensure FFmpeg is installed and accessible in your system PATH.
- The script uses `libx264` for video encoding and `aac` for audio, which are included in standard FFmpeg builds.

## License

This tool is intended for personal use. Ensure your usage complies with FFmpeg’s license (GPL) and any applicable terms for the input files you process.

## Troubleshooting

- **Permission Denied**:
  - Ensure the output directory is writable. Check permissions or try a different directory (e.g., `C:\Users\<YourUsername>\output`).
  - Run the command prompt as Administrator on Windows.
- **FFmpeg Not Found**:
  - Verify FFmpeg is installed and in your PATH: `ffmpeg -version`.
  - Reinstall FFmpeg if needed (see Installation section).
- **GUI Not Working**:
  - Ensure `tkinterdnd2` is installed: `pip install tkinterdnd2`.
  - On Linux, install `python3-tk` (e.g., `sudo apt install python3-tk`).
- **File Not Found**:
  - Check that the input file or folder exists and is accessible.
- **Conversion Errors**:
  - Check the console output for FFmpeg error details.
  - Ensure input files are valid and not corrupted.

## Contributing

Contributions to improve GIFAndVideoToMP4 are welcome. Here's how you can contribute:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add some amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please make sure to update tests and documentation as appropriate.
