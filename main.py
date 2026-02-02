#!/usr/bin/env python3
"""
YouTube Video Downloader
A privacy-focused YouTube video downloader using yt-dlp
"""

import os
from src.downloader import YouTubeDownloader


def main():
    """Main entry point"""
    print("\n" + "="*80)
    print("YouTube Video Downloader (Privacy-Focused)")
    print("="*80 + "\n")
    
    downloader = YouTubeDownloader()
    
    # Get video URL from user
    while True:
        url = input("Enter YouTube video URL: ").strip()
        if not url:
            print("URL cannot be empty. Please try again.")
            continue
        break
    
    # Fetch available formats
    print("\nFetching available formats...")
    formats = downloader.get_available_formats(url)
    
    if not formats:
        print("Failed to fetch formats. Please check the URL and try again.")
        return
    
    # Display formats (returns the list shown)
    top_formats = downloader.display_formats(formats)
    if not top_formats:
        print("Failed to prepare format list.")
        return
    
    # Get user's format selection
    while True:
        try:
            selection = input("Enter format number to download (or 'q' to quit): ").strip()
            
            if selection.lower() == 'q':
                print("Exiting...")
                return
            
            format_idx = int(selection) - 1

            if 0 <= format_idx < len(top_formats):
                selected_format = top_formats[format_idx]
                resolution = selected_format.get('resolution')
                format_id = selected_format.get('format_id')
                ext = selected_format.get('video_ext', 'mp4')
                print(f"\n✓ Selected format: {resolution} ({ext})")
                break
            else:
                print(f"Invalid selection. Please enter a number between 1 and {len(top_formats)}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Get download path from user
    while True:
        download_path = input("\nEnter download path (press Enter for current directory): ").strip()
        
        if not download_path:
            download_path = os.getcwd()
            print(f"Using current directory: {download_path}")
        else:
            download_path = os.path.expanduser(download_path)
        
        # Check if path is valid (parent directory should exist)
        parent_dir = os.path.dirname(download_path) or '.'
        if os.path.isdir(parent_dir):
            break
        else:
            print(f"Invalid path. Parent directory '{parent_dir}' does not exist.")
    
    # Download the video
    downloader.download(url, format_id, download_path)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nDownload cancelled by user.")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
