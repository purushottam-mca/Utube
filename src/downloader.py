"""Main downloader module"""

import os
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed. Install it using: pip install yt-dlp")
    exit(1)


class YouTubeDownloader:
    """Privacy-focused YouTube video downloader using yt-dlp"""
    
    def __init__(self):
        """Initialize the downloader"""
        self.ydl_opts = {
            'quiet': False,
            'no_warnings': False,
        }
    
    def get_available_formats(self, url: str):
        """
        Get all available formats for a video
        
        Args:
            url: YouTube video URL
            
        Returns:
            List of format dictionaries or None if error
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'no_warnings': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                formats = info.get('formats', [])
                return formats
        except Exception as e:
            print(f"Error fetching formats: {e}")
            return None
    
    def display_formats(self, formats):
        """
        Display available formats with numbering
        
        Args:
            formats: List of format dictionaries
        """
        if not formats:
            print("No formats available")
            return
        
        print("\n" + "="*80)
        print("Available Formats:")
        print("="*80)
        print(f"{'#':<4} {'Format ID':<12} {'Resolution':<12} {'Video Codec':<15} {'Audio Codec':<15}")
        print("-"*80)
        
        for idx, fmt in enumerate(formats, 1):
            format_id = fmt.get('format_id', 'N/A')
            resolution = fmt.get('format_note', 'N/A')
            vcodec = fmt.get('vcodec', 'N/A').split('.')[0]
            acodec = fmt.get('acodec', 'N/A').split('.')[0]
            
            # Truncate long values
            vcodec = vcodec[:14]
            acodec = acodec[:14]
            
            print(f"{idx:<4} {format_id:<12} {resolution:<12} {vcodec:<15} {acodec:<15}")
        
        print("="*80 + "\n")
    
    def download(self, url: str, format_id: str, output_path: str = None):
        """
        Download a video from YouTube
        
        Args:
            url: YouTube video URL
            format_id: Format ID to download
            output_path: Output directory for the downloaded video (defaults to current directory)
        """
        if output_path is None:
            output_path = os.getcwd()
        else:
            output_path = os.path.expanduser(output_path)
        
        # Ensure output directory exists
        Path(output_path).mkdir(parents=True, exist_ok=True)
        
        ydl_opts = {
            'format': format_id,
            'outtmpl': os.path.join(output_path, '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            print(f"\nDownloading to: {output_path}")
            print("This may take a while...\n")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("\n✓ Download completed successfully!")
        except Exception as e:
            print(f"\n✗ Error downloading: {e}")
