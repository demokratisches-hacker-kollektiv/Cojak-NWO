#!/usr/bin/env python3
"""
Persistent YouTube Downloader - NEVER GIVES UP
Keeps trying until all 229 videos are downloaded as video files
"""

import os
import subprocess
import json
import time
import random
from datetime import datetime

def load_video_ids():
    """Load all video IDs"""
    with open('all_video_ids.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_downloaded_videos():
    """Check what's already downloaded"""
    downloaded = set()
    if os.path.exists('video-archive'):
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv', '.avi', '.mov')):
                video_id = file.split('.')[0].split('-')[0]  # Extract video ID
                downloaded.add(video_id)
    return downloaded

def try_download_with_method(video_id, method_name, cmd):
    """Try downloading with specific method"""
    try:
        print(f"  Trying {method_name}...", end=' ')
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # Check if video file was created
            for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov']:
                video_file = f'video-archive/{video_id}{ext}'
                if os.path.exists(video_file) and os.path.getsize(video_file) > 1000000:  # > 1MB
                    print(f"SUCCESS! ({os.path.getsize(video_file)/1024/1024:.1f}MB)")
                    return True
            
            print("No valid video file created")
            return False
        else:
            print("Failed")
            return False
            
    except subprocess.TimeoutExpired:
        print("Timeout")
        return False
    except Exception as e:
        print(f"Error: {str(e)[:50]}")
        return False

def download_video_persistent(video_id, attempt_num):
    """Try downloading with ALL possible methods"""
    url = f'https://www.youtube.com/watch?v={video_id}'
    
    methods = [
        # Method 1: Android client, low quality
        (f"Android-240p", [
            'python', '-m', 'yt_dlp', url,
            '--output', f'video-archive/{video_id}.%(ext)s',
            '--format', 'worst[height>=240]',
            '--extractor-args', 'youtube:player_client=android',
            '--user-agent', 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
            '--no-playlist',
            '--ignore-errors',
            '--retries', '3'
        ]),
        
        # Method 2: Mweb client, very low quality
        (f"Mweb-144p", [
            'python', '-m', 'yt_dlp', url,
            '--output', f'video-archive/{video_id}.%(ext)s',
            '--format', 'worst[height>=144]',
            '--extractor-args', 'youtube:player_client=mweb',
            '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
            '--no-playlist',
            '--ignore-errors',
            '--retries', '3'
        ]),
        
        # Method 3: TV client
        (f"TV-client", [
            'python', '-m', 'yt_dlp', url,
            '--output', f'video-archive/{video_id}.%(ext)s',
            '--format', 'worst',
            '--extractor-args', 'youtube:player_client=tv_embedded',
            '--user-agent', 'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36',
            '--no-playlist',
            '--ignore-errors',
            '--retries', '3'
        ]),
        
        # Method 4: Invidious instance (alternative frontend)
        (f"Invidious", [
            'python', '-m', 'yt_dlp', f'https://yewtu.be/watch?v={video_id}',
            '--output', f'video-archive/{video_id}.%(ext)s',
            '--format', 'worst[height>=240]',
            '--no-playlist',
            '--ignore-errors',
            '--retries', '3'
        ]),
        
        # Method 5: Different Invidious instance
        (f"Invidious2", [
            'python', '-m', 'yt_dlp', f'https://yewtu.be/watch?v={video_id}?local=1',
            '--output', f'video-archive/{video_id}.%(ext)s',
            '--format', 'worst',
            '--no-playlist',
            '--ignore-errors',
            '--retries', '3'
        ])
    ]
    
    # Rotate methods based on attempt number to distribute load
    rotated_methods = methods[attempt_num % len(methods):] + methods[:attempt_num % len(methods)]
    
    for method_name, cmd in rotated_methods:
        if try_download_with_method(video_id, method_name, cmd):
            return True
    
    return False

def main():
    """Main persistent downloader"""
    print("=" * 60)
    print("PERSISTENT YOUTUBE DOWNLOADER - NEVER GIVES UP")
    print("=" * 60)
    print("Will keep trying until ALL 229 videos are downloaded!")
    print()
    
    os.makedirs('video-archive', exist_ok=True)
    
    video_ids = load_video_ids()
    print(f"Target: {len(video_ids)} videos from PUSH IT H-TOWN channel")
    
    attempt = 0
    max_attempts = 100  # Keep trying up to 100 times
    
    while attempt < max_attempts:
        attempt += 1
        downloaded = get_downloaded_videos()
        missing = [vid for vid in video_ids if vid not in downloaded]
        
        print(f"\n{'='*40}")
        print(f"ATTEMPT #{attempt} - {datetime.now().strftime('%H:%M:%S')}")
        print(f"Downloaded: {len(downloaded)}/{len(video_ids)}")
        print(f"Missing: {len(missing)}")
        print(f"Success Rate: {len(downloaded)/len(video_ids)*100:.1f}%")
        
        if not missing:
            print("\n🎉 ALL VIDEOS DOWNLOADED! MISSION ACCOMPLISHED! 🎉")
            break
        
        print(f"Trying to download {min(10, len(missing))} videos...")
        
        # Try to download first few missing videos
        new_downloads = 0
        for i, video_id in enumerate(missing[:10]):  # Limit to 10 per attempt
            print(f"{i+1:2d}. {video_id}", end=' ')
            
            if download_video_persistent(video_id, attempt):
                new_downloads += 1
            
            # Random delay between videos
            time.sleep(random.uniform(3, 8))
        
        print(f"Attempt #{attempt} result: +{new_downloads} new videos")
        
        # Longer break between attempts
        if len(missing) > 0:
            wait_time = min(60, 10 + attempt * 2)  # Increasing wait times
            print(f"Waiting {wait_time} seconds before next attempt...")
            time.sleep(wait_time)
    
    # Final report
    final_downloaded = get_downloaded_videos()
    print(f"\n{'='*60}")
    print(f"FINAL RESULT: {len(final_downloaded)}/{len(video_ids)} videos downloaded")
    print(f"Total attempts: {attempt}")
    
    # List downloaded files
    print(f"\nDownloaded files:")
    total_size = 0
    for file in sorted(os.listdir('video-archive')):
        if file.endswith(('.mp4', '.webm', '.mkv', '.avi', '.mov')):
            size = os.path.getsize(f'video-archive/{file}') / 1024 / 1024
            total_size += size
            print(f"  {file} ({size:.1f}MB)")
    
    print(f"\nTotal storage: {total_size:.1f}MB")
    print(f"Mission status: {'COMPLETE' if len(final_downloaded) == len(video_ids) else 'ONGOING'}")

if __name__ == "__main__":
    main()
