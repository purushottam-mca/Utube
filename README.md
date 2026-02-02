# Utube - YouTube Video Downloader

A simple, privacy-focused YouTube video downloader built with `yt-dlp`.

## Features

- Download YouTube videos in your preferred format
- View top 10 available resolutions
- Prioritizes **MP4** format (falls back to WebM or others)
- Shows file type and estimated file size

## Installation

### Prerequisites

- Python 3.8+
- yt-dlp

### Setup

```bash
# Install dependencies
pip install -r requirements.txt
```

Or with `uv`:

```bash
uv sync
```

## Quick Start

```bash
python main.py
```

Then:

1. Paste a YouTube video URL
2. Select your preferred resolution from the list
3. Enter a download directory (or press Enter for current directory)
4. Wait for the download to complete!

## Example

```
Enter YouTube video URL: https://www.youtube.com/watch?v=dQw4w9WgXcQ

Fetching available formats...

================================================================================
#    Resolution  Type     Size      
--------------------------------------------------------------------------------
1    2160p       mp4      450.5MB   
2    1440p       mp4      280.3MB   
3    1080p       mp4      150.2MB   
4    720p        webm     85.1MB    
5    480p        mp4      45.5MB    
================================================================================

Enter format number to download (or 'q' to quit): 3

✓ Selected format: 18 (1080p)

Enter download path (press Enter for current directory): 
Using current directory: /home/user/downloads

Downloading to: /home/user/downloads
This may take a while...

✓ Download completed successfully!
```

## Troubleshooting

### "Error fetching formats"
- Check your internet connection
- Verify the YouTube URL is valid and not private/age-restricted

### "ffmpeg not found"
- Install ffmpeg: `sudo apt install ffmpeg` (Linux) or `brew install ffmpeg` (macOS)
- Only needed if extracting audio

## License

MIT
