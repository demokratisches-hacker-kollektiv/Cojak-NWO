@echo off
echo Starting download of 229 PUSH IT H-TOWN videos...
echo This may take several hours depending on your connection speed.
echo.

REM Create URLs from video IDs
powershell -Command "Get-Content 'all_video_ids.txt' | ForEach-Object { 'https://www.youtube.com/watch?v=' + $_ } | Set-Content 'video_urls.txt'"

echo Created video_urls.txt with 229 URLs
echo.

REM Download with yt-dlp using Android client to avoid restrictions
python -m yt_dlp ^
--batch-file "video_urls.txt" ^
--download-archive "downloaded.txt" ^
--output "video-archive\%%(title)s.%%(ext)s" ^
--format "best[height<=720]" ^
--retries "10" ^
--sleep-interval "3" ^
--max-sleep-interval "15" ^
--continue ^
--ignore-errors ^
--write-info-json ^
--write-thumbnail ^
--extractor-args "youtube:player_client=android" ^
--user-agent "com.google.android.youtube/17.36.4 (Linux; U; Android 12; US) gzip" ^
--no-playlist

echo.
echo Download completed! Check video-archive folder for downloaded videos.
echo Downloaded videos are tracked in downloaded.txt
pause
