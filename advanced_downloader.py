#!/usr/bin/env python3
"""
Advanced YouTube Downloader for PUSH IT H-TOWN Channel
Uses multiple strategies to bypass YouTube restrictions
"""

import os
import subprocess
import json
import time
import random
from urllib.parse import urlparse

def get_video_ids():
    """Get all video IDs from the channel using multiple methods"""
    print("Extracting video IDs from PUSH IT H-TOWN channel...")
    
    strategies = [
        # Strategy 1: Android client
        [
            'python', '-m', 'yt_dlp', '--flat-playlist', '--print', '%(id)s',
            'https://www.youtube.com/@PUSHITHTOWN/videos',
            '--extractor-args', 'youtube:player_client=android',
            '--user-agent', 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip'
        ],
        # Strategy 2: Mweb client  
        [
            'python', '-m', 'yt_dlp', '--flat-playlist', '--print', '%(id)s',
            'https://www.youtube.com/@PUSHITHTOWN/videos',
            '--extractor-args', 'youtube:player_client=mweb',
            '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        ],
        # Strategy 3: TV client
        [
            'python', '-m', 'yt_dlp', '--flat-playlist', '--print', '%(id)s', 
            'https://www.youtube.com/@PUSHITHTOWN/videos',
            '--extractor-args', 'youtube:player_client=tv_embedded',
            '--user-agent', 'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36 WebAppManager'
        ]
    ]
    
    for i, strategy in enumerate(strategies):
        print(f"Trying strategy {i+1}...")
        try:
            result = subprocess.run(strategy, capture_output=True, text=True, 
                                  cwd='c:\\Users\\x\\Documents\\GitHub\\Cojak-NWO', timeout=300)
            
            if result.returncode == 0 and result.stdout.strip():
                video_ids = set(result.stdout.strip().split('\n'))
                video_ids.discard('')
                if len(video_ids) > 100:  # Reasonable number for a channel
                    print(f"SUCCESS: Strategy {i+1} successful: Found {len(video_ids)} videos")
                    return video_ids
                else:
                    print(f"FAILED: Strategy {i+1} failed: Too few videos ({len(video_ids)})")
            else:
                print(f"FAILED: Strategy {i+1} failed: {result.stderr[:200]}")
        except Exception as e:
            print(f"ERROR: Strategy {i+1} error: {str(e)}")
            
        time.sleep(2)  # Wait between attempts
    
    return set()

def download_videos(video_ids):
    """Download videos using robust configuration"""
    if not video_ids:
        print("No video IDs to download")
        return
    
    print(f"Starting download of {len(video_ids)} videos...")
    
    # Create URLs file
    urls = [f'https://www.youtube.com/watch?v={vid}' for vid in video_ids]
    with open('video_urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(urls))
    
    # Enhanced download configuration
    download_configs = [
        # Config 1: Android with throttling
        [
            'python', '-m', 'yt_dlp', '--batch-file', 'video_urls.txt',
            '--download-archive', 'downloaded.txt',
            '--output', 'video-archive/%(title)s.%(ext)s',
            '--format', 'best[height<=720]',
            '--retries', '10',
            '--sleep-interval', '5',
            '--max-sleep-interval', '30',
            '--continue',
            '--ignore-errors',
            '--write-info-json',
            '--write-thumbnail',
            '--extractor-args', 'youtube:player_client=android',
            '--user-agent', 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
            '--rate-limit', '1M'
        ],
        # Config 2: Mweb with different approach
        [
            'python', '-m', 'yt_dlp', '--batch-file', 'video_urls.txt',
            '--download-archive', 'downloaded.txt',
            '--output', 'video-archive/%(title)s.%(ext)s',
            '--format', 'worst[height>=360]',  # Lower quality to avoid detection
            '--retries', '5',
            '--sleep-interval', '10',
            '--max-sleep-interval', '60',
            '--continue',
            '--ignore-errors',
            '--write-info-json',
            '--extractor-args', 'youtube:player_client=mweb',
            '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
        ]
    ]
    
    for i, config in enumerate(download_configs):
        print(f"Attempting download with configuration {i+1}...")
        
        # Random delay before starting
        time.sleep(random.randint(5, 15))
        
        result = subprocess.run(config, cwd='c:\\Users\\x\\Documents\\GitHub\\Cojak-NWO')
        
        if result.returncode == 0:
            print(f"SUCCESS: Configuration {i+1} completed successfully")
            break
        else:
            print(f"FAILED: Configuration {i+1} encountered issues, trying next...")
            time.sleep(30)  # Wait longer between configs

def main():
    """Main download process"""
    print("=== PUSH IT H-TOWN Complete Video Downloader ===")
    print("This tool will attempt to download all videos from the channel")
    print("using multiple strategies to bypass YouTube restrictions.\n")
    
    # Ensure directories exist
    os.makedirs('video-archive', exist_ok=True)
    os.makedirs('mr-bloxx-videos', exist_ok=True) 
    os.makedirs('benjar-videos', exist_ok=True)
    
    # Get video IDs
    video_ids = get_video_ids()
    
    if not video_ids:
        print("ERROR: Failed to extract video IDs. Please check the channel URL.")
        return
    
    print(f"SUCCESS: Found {len(video_ids)} videos in the channel")
    
    # Check what's already downloaded
    downloaded_ids = set()
    if os.path.exists('downloaded.txt'):
        with open('downloaded.txt', 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:
                    downloaded_ids.add(parts[1])
    
    missing_ids = video_ids - downloaded_ids
    print(f"Already downloaded: {len(downloaded_ids)}")
    print(f"Need to download: {len(missing_ids)}")
    
    if missing_ids:
        download_videos(missing_ids)
    else:
        print("SUCCESS: All videos already downloaded!")
    
    # Generate report
    generate_report(video_ids, downloaded_ids)

def generate_report(total_ids, downloaded_ids):
    """Generate completion report"""
    completion_rate = len(downloaded_ids) / len(total_ids) * 100 if total_ids else 0
    
    report = f"""# PUSH IT H-TOWN Video Archive Report

## Download Statistics
- **Total Videos in Channel**: {len(total_ids)}
- **Successfully Downloaded**: {len(downloaded_ids)}
- **Completion Rate**: {completion_rate:.2f}%
- **Storage Location**: video-archive/

## Technical Details
- **Tool**: yt-dlp with multi-strategy approach
- **Quality**: Up to 720p (adaptive based on availability)
- **Format**: MP4/WebM with metadata
- **Retry Logic**: Multiple client types and configurations
- **Anti-Detection**: Rotating user agents and rate limiting

## Files Created
- video-archive/: Downloaded videos
- downloaded.txt: Download archive tracking
- video_urls.txt: Batch download URLs

## Status
{'COMPLETE' if completion_rate >= 95 else 'PARTIAL - Some videos may be unavailable'}

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open('video-archive/download-report.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nDownload Report:")
    print(f"   Total videos: {len(total_ids)}")
    print(f"   Downloaded: {len(downloaded_ids)}")
    print(f"   Completion: {completion_rate:.1f}%")
    print(f"\nCheck video-archive/download-report.md for details")

if __name__ == "__main__":
    main()
