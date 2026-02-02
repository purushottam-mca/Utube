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
        # Build a map of resolution -> best format for that resolution
        candidates = []
        for fmt in formats:
            # only consider video-containing formats
            if fmt.get('vcodec') == 'none':
                continue

            # resolution height (prefer numeric height key)
            height = fmt.get('height')
            if height is None:
                # try to parse from format_note (e.g. "720p")
                note = fmt.get('format_note') or ''
                try:
                    if note.endswith('p') and note[:-1].isdigit():
                        height = int(note[:-1])
                    else:
                        # fallback: look for any digits
                        import re
                        m = re.search(r"(\d{3,4})p", note)
                        height = int(m.group(1)) if m else -1
                except Exception:
                    height = -1

            # file type (extension)
            ext = fmt.get('ext', 'N/A')

            # video codec
            vcodec = (fmt.get('vcodec') or 'N/A').split('.')[0]

            # filesize or approximation
            filesize = fmt.get('filesize') or fmt.get('filesize_approx')

            # total bitrate for heuristic (tbr may be None)
            tbr = fmt.get('tbr') or 0

            candidates.append({
                'height': height if isinstance(height, int) else -1,
                'fmt': fmt,
                'ext': ext,
                'vcodec': vcodec,
                'filesize': filesize,
                'tbr': tbr,
                'has_audio': (fmt.get('acodec') != 'none')
            })

        # select best format per resolution: prefer formats that include audio, then higher tbr
        best_by_height = {}
        for c in candidates:
            h = c['height']
            cur = best_by_height.get(h)
            if cur is None:
                best_by_height[h] = c
                continue

            # prefer formats with audio
            if not cur['has_audio'] and c['has_audio']:
                best_by_height[h] = c
            elif cur['has_audio'] == c['has_audio']:
                # prefer mp4, then webm, then higher bitrate
                priority = {'mp4': 2, 'webm': 1}
                cur_pr = priority.get((cur.get('ext') or '').lower(), 0)
                c_pr = priority.get((c.get('ext') or '').lower(), 0)
                if c_pr > cur_pr:
                    best_by_height[h] = c
                elif c_pr == cur_pr:
                    if (c['tbr'] or 0) > (cur['tbr'] or 0):
                        best_by_height[h] = c

        # build sorted list of best formats by descending resolution
        best_list = sorted(best_by_height.values(), key=lambda x: (x['height'] or -1), reverse=True)

        # limit to top 10 resolutions
        top = best_list[:10]

        # helper to format filesize
        def human_size(n):
            if not n or not isinstance(n, (int, float)):
                return 'Unknown'
            n = float(n)
            for unit in ['B','KB','MB','GB','TB']:
                if n < 1024.0:
                    return f"{n:3.1f}{unit}"
                n /= 1024.0
            return f"{n:.1f}PB"

        print("="*80)
        print(f"{'#':<4} {'Resolution':<12} {'Type':<8} {'Size':<10}")
        print("-"*80)

        # prepare returned list of formats in display order
        top_formats = []
        for idx, c in enumerate(top, 1):
            fmt = c['fmt']
            resolution = f"{c['height']}p" if c['height'] and c['height'] > 0 else (fmt.get('format_note') or 'Unknown')
            ext = c['ext']
            size = human_size(c['filesize'])
            print(f"{idx:<4} {resolution:<12} {ext:<8} {size:<10}")
            top_formats.append(fmt)

        print("="*80 + "\n")

        # return the list of format dicts shown (so caller can map selection)
        return top_formats
    
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
