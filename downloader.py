import yt_dlp

url = str(input("video URL: "))

ydl = yt_dlp.YoutubeDL()

info = ydl.extract_info(url, download=False)

#get all formats
formats = info.get('formats', [])
resolutions = set()

for x in formats:
    resolution = x.get('height')
    if resolution is not None and int(resolution) >= int(144):
        resolutions.add(resolution)

resolutions = list(resolutions)
resolutions.sort(reverse=True)

print(resolutions)
choice = input(f"choose resolution (1-{len(resolutions)}): ")

selected_resolution = resolutions[int(choice) - 1] # which resolution to use

# find format with the specified resolution
selected_format = next((f for f in formats if f.get('height') == selected_resolution), None)

if selected_format:
    id = selected_format['format_id']
    height = selected_format['height']

    audiof = next((f for f in formats if f.get('acodec') != 'none'), None)
    audiofID = audiof['format_id'] if audiof else 'bestaudio'

    #options
    ydl_opts = {
        'format': f"{id}+{audiofID}",  # both video and audio are downloaded at same quality
        'outtmpl': f"%(title)s_{height}p.%(ext)s",
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }
else: # the fallback (highest quality)
    print("error - selecting highest quality")
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'merge_output_format': 'mp4',
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4'
        }]
    }

#download video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download([url])
        print("downloaded successfully: ")
    except Exception as e:
        print("error: ", e)