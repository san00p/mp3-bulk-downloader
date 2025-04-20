# YouTube to MP3 Downloader
Go to any yotube playlist and copy the URL
A Python GUI application that downloads audio from YouTube videos and converts them to MP3 files with customizable quality settings.

![Application Screenshot](screenshot.png) *Example screenshot would go here*

## Features

- Batch download multiple YouTube URLs simultaneously
- Three audio quality options (320kbps, 192kbps, 128kbps)
- Real-time download progress tracking
- Detailed download log with success/failure indicators
- Customizable output directory
- Queue-based downloading system
- Responsive GUI with Tkinter

## Requirements

- Python 3.8+
- FFmpeg
- Required Python packages (automatically installed):

## Installation

1. **Install Python** (3.8 or newer) from [python.org](https://www.python.org/downloads/)
2. **Install FFmpeg**:
   - Windows: Download from [ffmpeg.org](https://ffmpeg.org/) and add to PATH
   - macOS: `brew install ffmpeg`
   - Linux: `sudo apt install ffmpeg`
3. **Install dependencies**:
   ```bash
   pip install yt-dlp tkinter
Usage
Run the application:

bash
python youtube_to_mp3.pyw
Enter YouTube URLs (one per line)

Select audio quality (default: 192kbps)

Choose output directory (default: Downloads folder)

Click "Download All"

Command Line Options
bash
python youtube_to_mp3.pyw [--quality 192] [--output /path/to/save]
Troubleshooting
If downloads fail, check that:

FFmpeg is properly installed

YouTube URLs are valid

You have write permissions for the output directory

For network issues, try using a VPN

License
MIT License - Free for personal and educational use


---

## `PRECONDITIONS.md`

```markdown
# Preconditions for YouTube to MP3 Downloader

## System Requirements

### Hardware
- Minimum 2GB RAM
- 500MB free disk space
- Internet connection

### Software
1. **Python 3.8+** must be installed
   - Verify with: `python --version`
2. **FFmpeg** must be available in system PATH
   - Verify with: `ffmpeg -version`
3. **Required Python packages**:
   - yt-dlp (latest version)
   - tkinter (usually included with Python)

## Configuration

1. **FFmpeg Path**:
   - The application looks for FFmpeg at:
     ```python
     FFMPEG_PATH = r'C:\path\to\ffmpeg.exe'
     ```
   - Modify this in the script if using a custom location

2. **Output Directory**:
   - Default: User's Downloads folder
   - Change via GUI or modify:
     ```python
     self.location_entry.insert(0, str(Path.home() / "Downloads"))
     ```

## Legal Considerations

1. **Copyright Compliance**:
   - Only download content you have rights to
   - Respect YouTube's Terms of Service
   - Not for commercial use without permission

2. **Rate Limiting**:
   - Avoid mass downloads to prevent IP blocking
   - Recommended: < 100 videos per session

## Known Limitations

1. **Video Length**:
   - Maximum recommended: 4 hours (may timeout)
   
2. **Formats**:
   - Output is always MP3
   - Some rare audio formats may not convert properly

3. **Platform Support**:
   - Fully tested on Windows 10/11
   - Should work on macOS/Linux but FFmpeg path may need adjustment

## Troubleshooting Setup

If you get errors about missing dependencies:

```bash
# On Windows
python -m pip install --upgrade pip setuptools wheel

# Cross-platform
pip install yt-dlp==2023.7.6 ffmpeg-python==0.2.0
For FFmpeg issues, verify installation with:

bash
ffmpeg -version

---

These documents provide users with:
1. Clear installation/usage instructions (README)
2. Technical requirements and setup details (PRECONDITIONS)
3. Legal considerations
4. Troubleshooting guidance

Would you like me to modify any section or add specific details about your environment?
