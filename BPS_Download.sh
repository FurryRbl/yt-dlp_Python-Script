yt-dlp \
--continue \
-f "ba+bv" \
--format "bestvideo[height=1080]+bestaudio/best" \
-o ".\Video\%(upload_date)s\%(title)s\%(title)s.%(ext)s" \
--write-thumbnail \
--convert-thumbnails "png" \
--write-info-json \
--write-description \
--write-annotations \
--sub-format srt \
--sub-langs "all" \
--write-subs \
--write-pages \
--write-info-json \
--retries infinite \
--write-playlist-metafiles \
"https://www.youtube.com/@BlackPlasmaStudios"
