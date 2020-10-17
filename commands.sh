youtube-dl -i --geo-bypass --yes-playlist -x --audio-format mp3 --embed-thumbnail --add-metadata -a '~/self/youtube_process/link_list.txt' -o '~/Music/%(title)s.%(ext)s'

python3 mp3_cleanup.py

# -i: ignore errors
# --geo-bypass
# --yes-playlist: dolwoad playlist if url is ambigious
# -x: convert viedo files to audio-only
# --audio-fomat FORMAT
# --embed-thumbnail: embed thumbnail into audio as cover art
# --add-metadata
# -o, --output Template: Output filename template, see the OUTPUT TEMPLATE for all the info

# --playlist-start NUMBER
# --dateafter: dowload only videos uploaded on or after this date
