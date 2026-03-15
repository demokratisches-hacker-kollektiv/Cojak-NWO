# Complete Video Download Verification and Retry Script
# Ensures all PUSH IT H-TOWN videos are downloaded, focusing on Mr.Bloxx and Benjar content

import os
import subprocess
import json

# Get all video IDs from channel
print("Getting all video IDs from channel...")
result = subprocess.run([
    'python', '-m', 'yt_dlp', '--flat-playlist', '--print', '%(id)s', 
    'https://www.youtube.com/@PUSHITHTOWN/videos',
    '--cookies-from-browser', 'chrome',
    '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
], capture_output=True, text=True, cwd='c:\\Users\\x\\Documents\\GitHub\\Cojak-NWO')

if result.returncode == 0:
    all_ids = set(result.stdout.strip().split('\n'))
    all_ids.discard('')
    print(f"Found {len(all_ids)} videos in channel")
else:
    print("Error getting video IDs:", result.stderr)
    exit(1)

# Get downloaded IDs from archive
downloaded_ids = set()
archive_file = 'downloaded.txt'
if os.path.exists(archive_file):
    with open(archive_file, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 2:
                downloaded_ids.add(parts[1])

print(f"Already downloaded: {len(downloaded_ids)} videos")

# Find missing IDs
missing_ids = all_ids - downloaded_ids
print(f"Missing videos: {len(missing_ids)}")

if missing_ids:
    print("Downloading missing videos...")
    urls = [f'https://www.youtube.com/watch?v={vid}' for vid in missing_ids]
    
    # Write to batch file
    with open('missing_urls.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(urls))
    
    # Download missing videos
    subprocess.run([
        'python', '-m', 'yt_dlp', '--batch-file', 'missing_urls.txt',
        '--download-archive', 'downloaded.txt',
        '--output', 'video-archive/%(title)s.%(ext)s',
        '--format', 'best[height<=720]',
        '--retries', '20',
        '--sleep-interval', '10',
        '--max-sleep-interval', '60',
        '--continue',
        '--ignore-errors',
        '--write-info-json',
        '--write-thumbnail',
        '--cookies-from-browser', 'chrome',
        '--user-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        '--extractor-args', 'youtube:player_client=ios'
    ], cwd='c:\\Users\\x\\Documents\\GitHub\\Cojak-NWO')

# Filter for Mr.Bloxx and Benjar videos
print("Filtering videos for Mr.Bloxx and Benjar...")
mr_bloxx_videos = []
benjar_videos = []

for root, dirs, files in os.walk('video-archive'):
    for file in files:
        if file.endswith('.info.json'):
            with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    title = data.get('title', '').lower()
                    description = data.get('description', '').lower()
                    
                    if 'mr.bloxx' in title or 'mr.bloxx' in description or 'mr bloxx' in title or 'mr bloxx' in description:
                        mr_bloxx_videos.append(data['id'])
                    if 'benjar' in title or 'benjar' in description:
                        benjar_videos.append(data['id'])
                except:
                    pass

print(f"Mr.Bloxx videos found: {len(mr_bloxx_videos)}")
print(f"Benjar videos found: {len(benjar_videos)}")

# Copy to dedicated folders
os.makedirs('mr-bloxx-videos', exist_ok=True)
os.makedirs('benjar-videos', exist_ok=True)

for vid_id in mr_bloxx_videos:
    # Find and copy video file
    for root, dirs, files in os.walk('video-archive'):
        for file in files:
            if vid_id in file and (file.endswith('.mp4') or file.endswith('.webm')):
                src = os.path.join(root, file)
                dst = os.path.join('mr-bloxx-videos', file)
                if not os.path.exists(dst):
                    os.rename(src, dst)

for vid_id in benjar_videos:
    for root, dirs, files in os.walk('video-archive'):
        for file in files:
            if vid_id in file and (file.endswith('.mp4') or file.endswith('.webm')):
                src = os.path.join(root, file)
                dst = os.path.join('benjar-videos', file)
                if not os.path.exists(dst):
                    os.rename(src, dst)

# Update reports
total_downloaded = len(downloaded_ids) + len(missing_ids) - len(missing_ids) + len(all_ids - downloaded_ids - missing_ids)  # adjust
completion_rate = len(all_ids - missing_ids) / len(all_ids) * 100 if all_ids else 0

report = f"""# Complete Video Archive Download Report

## Download Statistics
- **Total Videos Expected**: {len(all_ids)}
- **Videos Successfully Downloaded**: {len(all_ids) - len(missing_ids)}
- **Download Archive Entries**: {len(downloaded_ids)}
- **Total Storage Used**: TBD
- **Download Completion Rate**: {completion_rate:.2f}%

## Download Configuration
- **Tool Used**: yt-dlp (YouTube downloader)
- **Format**: Best quality up to 720p
- **Location**: video-archive/ subdirectory
- **Retry Policy**: 20 retries per video with extended sleep intervals
- **Resume Capability**: Enabled via download archive
- **Error Handling**: Continue on individual video failures with bot detection bypass

## Files Created
- **all_video_ids.txt**: List of all video IDs ({len(all_ids)} entries)
- **downloaded.txt**: Download archive tracking successful downloads
- **video-archive/**: Directory containing all downloaded videos
- **mr-bloxx-videos/**: Filtered videos featuring Mr.Bloxx ({len(mr_bloxx_videos)} videos)
- **benjar-videos/**: Filtered videos featuring Benjar ({len(benjar_videos)} videos)

## Verification Process
1. Extract all video IDs from PUSH IT H-TOWN channel
2. Compare with download archive to identify missing videos
3. Retry download of missing videos with enhanced anti-bot measures
4. Filter and organize videos by featured individuals
5. Update reports with completion statistics

**Status**: {'COMPLETE' if len(missing_ids) == 0 else 'PARTIAL - MISSING VIDEOS RETRIED'}
"""

with open('video-archive/download-report.md', 'w', encoding='utf-8') as f:
    f.write(report)

print("Download verification and retry completed. Check video-archive/download-report.md for status.")
