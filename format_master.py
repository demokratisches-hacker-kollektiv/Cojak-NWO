#!/usr/bin/env python3
"""
FORMAT MASTER DOWNLOADER
Master of all formats and quality settings
"""

import os
import subprocess
import time

def format_master():
    """Master downloader for all formats"""
    print("FORMAT MASTER - CONTROLLING ALL VIDEO FORMATS")
    
    with open('all_video_ids.txt', 'r') as f:
        video_ids = [line.strip() for line in f if line.strip()]
    
    # All possible format combinations
    format_strategies = [
        # Ultra low quality (more likely to succeed)
        ['worst', '144p'],
        ['worst[height>=144]', '144p+'],
        ['worst[height>=240]', '240p'],
        ['worstvideo+worstaudio', 'video+audio'],
        ['worstvideo', 'video only'],
        ['worstaudio', 'audio only'],
        
        # Specific formats
        ['mp4', 'MP4'],
        ['webm', 'WebM'],
        ['3gp', '3GP'],
        ['flv', 'FLV'],
        
        # Slightly higher quality
        ['best[height<=240]', 'best-240p'],
        ['best[height<=360]', 'best-360p'],
        ['best[height<=480]', 'best-480p'],
        
        # Audio formats
        ['bestaudio', 'best audio'],
        ['mp3', 'MP3 audio'],
        ['wav', 'WAV audio'],
        ['aac', 'AAC audio']
    ]
    
    master_round = 0
    
    while True:
        master_round += 1
        print(f"\nFORMAT MASTER ROUND #{master_round} - {time.strftime('%H:%M:%S')}")
        
        # Count current downloads
        downloaded = 0
        total_size = 0
        for file in os.listdir('video-archive'):
            if file.endswith(('.mp4', '.webm', '.mkv', '.avi', '.mov', '.3gp', '.flv', '.mp3', '.wav', '.aac')):
                downloaded += 1
                total_size += os.path.getsize(f'video-archive/{file}')
        
        progress = (downloaded / len(video_ids)) * 100
        print(f"Master control: {downloaded}/{len(video_ids)} ({progress:.1f}%) - {total_size/1024/1024:.1f}MB")
        
        if downloaded >= len(video_ids):
            print("🏆 FORMAT MASTER VICTORY! ALL VIDEOS IN ALL FORMATS! 🏆")
            break
        
        # Find missing videos
        missing = []
        for video_id in video_ids:
            exists = False
            for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.3gp', '.flv', '.mp3', '.wav', '.aac']:
                if os.path.exists(f'video-archive/{video_id}{ext}'):
                    exists = True
                    break
            if not exists:
                missing.append(video_id)
        
        print(f"Master processing {len(missing)} missing videos with format control...")
        
        # Process first 5 missing videos with all format strategies
        for i, video_id in enumerate(missing[:5]):
            print(f"  Master {i+1}: Processing {video_id}...")
            
            for j, (fmt_code, fmt_name) in enumerate(format_strategies):
                print(f"    Format {j+1} ({fmt_name}):", end=' ')
                
                try:
                    # Build command based on format type
                    if 'audio' in fmt_name.lower():
                        cmd = [
                            'python', '-m', 'yt_dlp',
                            f'https://www.youtube.com/watch?v={video_id}',
                            '--output', f'video-archive/{video_id}-fmt{j}.%(ext)s',
                            '--extract-audio',
                            '--audio-format', fmt_code.lower().replace(' ', ''),
                            '--no-playlist',
                            '--ignore-errors'
                        ]
                    else:
                        cmd = [
                            'python', '-m', 'yt_dlp',
                            f'https://www.youtube.com/watch?v={video_id}',
                            '--output', f'video-archive/{video_id}-fmt{j}.%(ext)s',
                            '--format', fmt_code,
                            '--no-playlist',
                            '--ignore-errors'
                        ]
                    
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=40)
                    
                    if result.returncode == 0:
                        # Check for any valid file
                        success = False
                        for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.3gp', '.flv', '.mp3', '.wav', '.aac']:
                            test_file = f'video-archive/{video_id}-fmt{j}{ext}'
                            if os.path.exists(test_file) and os.path.getsize(test_file) > 10000:
                                final_file = f'video-archive/{video_id}{ext}'
                                if not os.path.exists(final_file):
                                    os.rename(test_file, final_file)
                                    size = os.path.getsize(final_file)
                                    print(f"SUCCESS ({size/1024/1024:.1f}MB)")
                                    success = True
                                    break
                        
                        if not success:
                            print("No valid file")
                    else:
                        print("Failed")
                        
                except Exception as e:
                    print(f"Error: {str(e)[:25]}")
                
                # Check if video is now downloaded
                for ext in ['.mp4', '.webm', '.mkv', '.avi', '.mov', '.3gp', '.flv', '.mp3', '.wav', '.aac']:
                    if os.path.exists(f'video-archive/{video_id}{ext}'):
                        print(f"    ✓ {video_id} mastered in format {ext}!")
                        break
                else:
                    continue  # Try next format
                break  # Video downloaded, move to next video
            
            time.sleep(4)  # Wait between videos
        
        print(f"Master round {master_round} completed. Analyzing format data...")
        time.sleep(25)

if __name__ == "__main__":
    format_master()
