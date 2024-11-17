from pytubefix import YouTube
from pydub import AudioSegment
import moviepy.editor as mpe


#download a yt video and convert it into mp3
def download_audio_and_convert(url, format_to_convert_to="mp3"):
    #download video

    print("Accessing Link... ")
    yt = YouTube(url)
    vid_name = yt.title
    print(f"Link accessed: {vid_name}")

    print("Downloading Video...")
    yt = yt.streams.get_audio_only("mp4")
    yt.download("raw_downloads/raw_m4a")
    print("Downloaded Successfully")

    #convert video
    print(f"Converting Audio to {format_to_convert_to}...")

    m4a_audio = AudioSegment.from_file(f"raw_downloads/raw_m4a/{vid_name}.m4a", format="m4a")
    m4a_audio.export(f"Output/mp3/{vid_name}.{format_to_convert_to}", format=format_to_convert_to)

    print("Done!")

def download_video(url, max_res=1080, audio_format_to_convert_to="mp3"):
    #download video

    yt = YouTube(url)
    vid_name = yt.title

    #vid = yt.streams.get_highest_resolution(False)

    #find the best video with a res lower than the specified max
    vids = yt.streams.filter(progressive=False)
    best_vid = None
    if len(vids) == 0:
        best_vid = yt.streams.get_highest_resolution()
    else:
        for vid in vids:
            if vid.resolution:
                #if the resolution is bigger than the max, skip
                if int(vid.resolution[:-1]) > max_res:
                    continue
                # compare
                if not best_vid: # if there isnt a best video yet then we make this the best by default
                    best_vid = vid
                else:
                    if int(vid.resolution[:-1]) > int(best_vid.resolution[:-1]): # if this video has a higher res than the current best then it is the new best
                            best_vid = vid

    vid = best_vid
    print(f"Downloading:\n{vid.title}\nres: {vid.resolution}")
    vid.download("raw_downloads/mp4_raw")
    print("Downloaded Video")

    print("Downloading Audio...")

    #download the actual audio
    audio = yt.streams.get_audio_only("mp4")
    audio.download("raw_downloads/raw_m4a")
    #convert the audio to mp3
    m4a_audio = AudioSegment.from_file(f"raw_downloads/raw_m4a/{vid_name}.m4a", format="m4a")
    m4a_audio.export(f"Output/mp3/{vid_name}.{audio_format_to_convert_to}", format=audio_format_to_convert_to)

    print("Audio Downloaded ")

    print("Merging Audio and Video... ")
    audio = mpe.AudioFileClip(f"Output/mp3/{vid_name}.mp3")
    video1 = mpe.VideoFileClip(f"raw_downloads/mp4_raw/{vid_name}.mp4")
    final = video1.set_audio(audio)
    final.write_videofile(f"Output/mp4/{vid_name}.mp4")
    print("Merged.\n")

    print(f"Successfully Downloaded:\n{vid_name}\nres: {vid.resolution}\nfps: {vid.fps}")


audio_or_video = input("Download audio only or video and audio? (a, v) ")
link = input("Enter a youtube video URL: ")
if audio_or_video == "a":
    download_audio_and_convert(link, "mp3")
elif audio_or_video == "v":
    download_video(link)

input("Press enter to stop: ")