#!/usr/bin/env python3
"""
Ultimate YouTube Downloader for PUSH IT H-TOWN
Uses multiple advanced strategies to bypass YouTube restrictions
"""

import os
import subprocess
import json
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

def load_video_ids():
    """Load video IDs from file"""
    with open('all_video_ids.txt', 'r') as f:
        return [line.strip() for line in f if line.strip()]

def try_download_video(video_id, strategy_num):
    """Try downloading a single video with specific strategy"""
    url = f'https://www.youtube.com/watch?v={video_id}'
    
    strategies = {
        1: {
            'name': 'Android Client',
            'args': [
                'python', '-m', 'yt_dlp', url,
                '--output', f'video-archive/{video_id}.%(ext)s',
                '--format', 'worst[height>=360]',  # Lower quality
                '--extractor-args', 'youtube:player_client=android',
                '--user-agent', 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
                '--write-info-json',
                '--max-filesize', '50M',  # Limit file size
                '--no-playlist'
            ]
        },
        2: {
            'name': 'Mweb Client',
            'args': [
                'python', '-m', 'yt_dlp', url,
                '--output', f'video-archive/{video_id}.%(ext)s',
                '--format', 'worst[height>=240]',  # Even lower quality
                '--extractor-args', 'youtube:player_client=mweb',
                '--user-agent', 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                '--write-info-json',
                '--no-playlist'
            ]
        },
        3: {
            'name': 'TV Client',
            'args': [
                'python', '-m', 'yt_dlp', url,
                '--output', f'video-archive/{video_id}.%(ext)s',
                '--format', 'worst',
                '--extractor-args', 'youtube:player_client=tv_embedded',
                '--user-agent', 'Mozilla/5.0 (Web0S; Linux/SmartTV) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.34 Safari/537.36 WebAppManager',
                '--write-info-json',
                '--no-playlist'
            ]
        },
        4: {
            'name': 'Audio Only',
            'args': [
                'python', '-m', 'yt_dlp', url,
                '--output', f'video-archive/{video_id}.%(ext)s',
                '--extract-audio',
                '--audio-format', 'mp3',
                '--extractor-args', 'youtube:player_client=android',
                '--user-agent', 'com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip',
                '--write-info-json',
                '--no-playlist'
            ]
        }
    }
    
    strategy = strategies.get(strategy_num, strategies[1])
    
    try:
        # Random delay to avoid detection
        time.sleep(random.uniform(1, 3))
        
        result = subprocess.run(
            strategy['args'],
            capture_output=True,
            text=True,
            timeout=60,
            cwd='c:\\Users\\x\\Documents\\GitHub\\Cojak-NWO'
        )
        
        if result.returncode == 0:
            # Check if file was actually created
            for ext in ['.mp4', '.webm', '.mkv', '.mp3']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    return True, strategy['name'], f"Success with {strategy['name']}"
            
            return False, strategy['name'], "No file created"
        else:
            return False, strategy['name'], result.stderr[:100]
            
    except subprocess.TimeoutExpired:
        return False, strategy['name'], "Timeout"
    except Exception as e:
        return False, strategy['name'], str(e)[:100]

def download_video_with_fallback(video_id):
    """Try downloading with all strategies"""
    print(f"Attempting {video_id}...", end='')
    
    for strategy_num in range(1, 5):
        success, strategy_name, message = try_download_video(video_id, strategy_num)
        
        if success:
            print(f" ✓ ({strategy_name})")
            return True
    
    print(f" ✗ (All strategies failed)")
    return False

def main():
    """Main download process"""
    print("=== ULTIMATE PUSH IT H-TOWN VIDEO DOWNLOADER ===")
    print("Using advanced multi-strategy approach to bypass restrictions\n")
    
    # Ensure directory exists
    os.makedirs('video-archive', exist_ok=True)
    
    # Load video IDs
    video_ids = load_video_ids()
    print(f"Loaded {len(video_ids)} video IDs")
    
    # Check what's already downloaded
    existing_files = set()
    for file in os.listdir('video-archive'):
        if file.endswith(('.mp4', '.webm', '.mkv', '.mp3')):
            video_id = file.split('.')[0]
            existing_files.add(video_id)
    
    print(f"Already downloaded: {len(existing_files)}")
    
    # Filter missing videos
    missing_ids = [vid for vid in video_ids if vid not in existing_files]
    print(f"Need to download: {len(missing_ids)}")
    
    if not missing_ids:
        print("All videos already downloaded!")
        return
    
    # Download with threading for better performance
    success_count = 0
    total_attempts = len(missing_ids)
    
    print(f"\nStarting download with multiple strategies...")
    print("This will try different client types: Android, Mobile Web, TV, Audio-only\n")
    
    # Use smaller thread pool to avoid getting blocked
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit download tasks
        future_to_video = {
            executor.submit(download_video_with_fallback, video_id): video_id 
            for video_id in missing_ids[:50]  # Limit to first 50 for testing
        }
        
        # Process results
        for future in as_completed(future_to_video):
            video_id = future_to_video[future]
            try:
                if future.result():
                    success_count += 1
            except Exception as e:
                print(f"Error with {video_id}: {e}")
    
    # Report results
    print(f"\n=== DOWNLOAD SUMMARY ===")
    print(f"Attempted: {total_attempts}")
    print(f"Successful: {success_count}")
    print(f"Failed: {total_attempts - success_count}")
    print(f"Success Rate: {(success_count/total_attempts)*100:.1f}%")
    print(f"\nFiles saved in: video-archive/")
    
    # Create detailed report
    with open('video-archive/ultimate-download-report.md', 'w') as f:
        f.write(f"""# Ultimate PUSH IT H-TOWN Download Report
        
## Statistics
- **Total Videos**: {len(video_ids)}
- **Previously Downloaded**: {len(existing_files)}
- **Attempted This Session**: {total_attempts}
- **Successfully Downloaded**: {success_count}
- **Failed**: {total_attempts - success_count}
- **Success Rate**: {(success_count/total_attempts)*100:.1f}%

## Strategies Used
1. Android Client (low quality)
2. Mobile Web Client (lowest quality)
3. TV Embedded Client
4. Audio-only extraction

## Notes
- Used multiple client types to bypass YouTube restrictions
- Limited to 360p or lower quality to avoid detection
- Implemented rate limiting and random delays
- Some videos may be unavailable due to age restrictions or removal

Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}
""")

if __name__ == "__main__":
    main()
