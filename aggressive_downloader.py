#!/usr/bin/env python3
"""
AGGRESSIVE PARALLEL DOWNLOADER
Maximum effort to download all videos FAST
"""

import os
import subprocess
import threading
import time
import random
from concurrent.futures import ThreadPoolExecutor

video_ids = []
downloaded_lock = threading.Lock()
downloaded_count = 0

def load_video_ids():
    global video_ids
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    print(f"Loaded {len(video_ids)} video IDs")

def is_already_downloaded(video_id):
    """Check if video is already downloaded"""
    for ext in ['.mp4', '.webm', '.mkv']:
        if os.path.exists(f'video-archive/{video_id}{ext}'):
            return True
    return False

def download_worker(worker_id):
    """Worker thread that continuously downloads videos"""
    global downloaded_count
    
    print(f"Worker {worker_id} started")
    
    while True:
        # Find a video that hasn't been downloaded
        for video_id in video_ids:
            if not is_already_downloaded(video_id):
                # Try to download this video
                success = try_download_video(video_id, worker_id)
                if success:
                    with downloaded_lock:
                        downloaded_count += 1
                        print(f"Worker {worker_id}: SUCCESS! Total downloaded: {downloaded_count}")
                break
        else:
            # All videos downloaded
            print(f"Worker {worker_id}: All videos downloaded!")
            break
        
        time.sleep(random.uniform(1, 3))

def try_download_video(video_id, worker_id):
    """Try downloading with multiple methods"""
    url = f'https://www.youtube.com/watch?v={video_id}'
    
    # Method 1: Android client
    cmd1 = [
        'python', '-m', 'yt_dlp', url,
        '--output', f'video-archive/{video_id}.%(ext)s',
        '--format', 'worst[height>=240]',
        '--extractor-args', 'youtube:player_client=android',
        '--user-agent', 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
        '--no-playlist',
        '--ignore-errors',
        '--retries', '1'
    ]
    
    # Method 2: Mweb client  
    cmd2 = [
        'python', '-m', 'yt_dlp', url,
        '--output', f'video-archive/{video_id}.%(ext)s',
        '--format', 'worst[height>=144]',
        '--extractor-args', 'youtube:player_client=mweb', 
        '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15',
        '--no-playlist',
        '--ignore-errors',
        '--retries', '1'
    ]
    
    # Method 3: Invidious
    cmd3 = [
        'python', '-m', 'yt_dlp', f'https://yewtu.be/watch?v={video_id}',
        '--output', f'video-archive/{video_id}.%(ext)s',
        '--format', 'worst',
        '--no-playlist', 
        '--ignore-errors',
        '--retries', '1'
    ]
    
    methods = [cmd1, cmd2, cmd3]
    
    for i, cmd in enumerate(methods):
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                # Check if file was created
                for ext in ['.mp4', '.webm', '.mkv']:
                    if os.path.exists(f'video-archive/{video_id}{ext}'):
                        size = os.path.getsize(f'video-archive/{video_id}{ext}')
                        if size > 1000000:  # > 1MB
                            print(f"Worker {worker_id}: Downloaded {video_id} using method {i+1} ({size/1024/1024:.1f}MB)")
                            return True
        except:
            continue
    
    return False

def main():
    print("=" * 60)
    print("AGGRESSIVE PARALLEL YOUTUBE DOWNLOADER")
    print("=" * 60)
    
    os.makedirs('video-archive', exist_ok=True)
    load_video_ids()
    
    # Start multiple worker threads
    num_workers = 5
    print(f"Starting {num_workers} parallel download workers...")
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = [executor.submit(download_worker, i) for i in range(num_workers)]
        
        # Monitor progress
        try:
            while True:
                time.sleep(10)
                print(f"Progress: {downloaded_count}/{len(video_ids)} downloaded")
                
                if downloaded_count >= len(video_ids):
                    print("🎉 ALL VIDEOS DOWNLOADED! 🎉")
                    break
                    
        except KeyboardInterrupt:
            print("\nDownload interrupted by user")
    
    print(f"Final result: {downloaded_count}/{len(video_ids)} videos downloaded")

if __name__ == "__main__":
    main()
