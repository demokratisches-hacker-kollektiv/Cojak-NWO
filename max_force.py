#!/usr/bin/env python3
"""
MAXIMUM FORCE DOWNLOADER
Multiple instances running simultaneously for maximum download power
"""

import os
import subprocess
import time
import random

def download_worker(worker_id):
    """Dedicated worker that never stops"""
    print(f"MAX FORCE Worker {worker_id} started - WILL NEVER STOP")
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    while True:
        for video_id in video_ids:
            # Check if downloaded
            downloaded = False
            for ext in ['.mp4', '.webm', '.mkv']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    downloaded = True
                    break
            
            if not downloaded:
                # Try with different strategy based on worker ID
                strategies = [
                    # Strategy 1: Basic
                    ['python', '-m', 'yt_dlp', f'https://www.youtube.com/watch?v={video_id}',
                     '--output', f'video-archive/{video_id}-w{worker_id}.%(ext)s',
                     '--format', 'worst', '--no-playlist', '--ignore-errors'],
                    
                    # Strategy 2: Android
                    ['python', '-m', 'yt_dlp', f'https://www.youtube.com/watch?v={video_id}',
                     '--output', f'video-archive/{video_id}-w{worker_id}.%(ext)s',
                     '--format', 'worst[height>=240]', '--extractor-args', 'youtube:player_client=android',
                     '--user-agent', 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
                     '--no-playlist', '--ignore-errors'],
                    
                    # Strategy 3: Invidious
                    ['python', '-m', 'yt_dlp', f'https://yewtu.be/watch?v={video_id}',
                     '--output', f'video-archive/{video_id}-w{worker_id}.%(ext)s',
                     '--format', 'worst', '--no-playlist', '--ignore-errors']
                ]
                
                strategy = strategies[worker_id % len(strategies)]
                
                try:
                    result = subprocess.run(strategy, capture_output=True, text=True, timeout=45)
                    
                    if result.returncode == 0:
                        # Check and rename file
                        for ext in ['.mp4', '.webm', '.mkv']:
                            test_file = f'video-archive/{video_id}-w{worker_id}{ext}'
                            if os.path.exists(test_file) and os.path.getsize(test_file) > 500000:
                                final_file = f'video-archive/{video_id}{ext}'
                                if not os.path.exists(final_file):
                                    os.rename(test_file, final_file)
                                    print(f"Worker {worker_id}: DOWNLOADED {video_id}!")
                                break
                
                except:
                    pass
                
                time.sleep(random.uniform(2, 5))
        
        time.sleep(10)  # Brief pause before restarting cycle

if __name__ == "__main__":
    worker_id = int(os.getenv('WORKER_ID', '0'))
    download_worker(worker_id)
