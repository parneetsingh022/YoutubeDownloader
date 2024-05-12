from pytube import YouTube
import inquirer
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm
import os
import time

# Ask for the YouTube video URL
url = input("Enter the YouTube video URL: ")

# Create a YouTube object
yt = YouTube(url)

# Ask the user if they want to download audio or video
questions = [
  inquirer.List('type',
                message="What do you want to download?",
                choices=['Audio', 'Video'],
            ),
]
answers = inquirer.prompt(questions)

if answers['type'] == 'Video':
    print("Loading available resolutions...")
    # Get the available streams and filter out audio-only streams
    video_streams = [stream for stream in yt.streams.filter(file_extension='mp4')]

    # Create a list of available resolutions
    resolutions = sorted(set([stream.resolution for stream in video_streams if stream.resolution]))

    # Filtering non-desired resolutions
    resolutions = [res for res in resolutions if res in ['144p', '240p', '360p', '480p', '720p', '1080p']]
    if '1080p' in resolutions:
        resolutions.remove('1080p')
        resolutions.append('1080p')  # Add 1080p to the bottom of the list

    # Create the questions
    questions = [
      inquirer.List('resolution',
                    message="Select a resolution",
                    choices=resolutions,
                ),
    ]

    # Prompt the user to select a resolution
    answers = inquirer.prompt(questions)

    # Print the selected resolution
    print(f"You selected {answers['resolution']}")

    # Download the video with the selected resolution
    print("Downloading video...")
    for i in tqdm(range(100)):
        time.sleep(0.01)  # simulate time delay
    if answers['resolution'] in ['360p', '720p']:
        yt.streams.filter(res=answers['resolution']).first().download(filename=f"{yt.title}({answers['resolution']}).mp4")
    else:
        video = yt.streams.filter(res=answers['resolution']).first().download(filename='video.mp4')
        audio = yt.streams.filter(only_audio=True).first().download(filename='audio.mp3')

        videoclip = VideoFileClip("video.mp4")
        videoclip.audio = AudioFileClip("audio.mp3")

        videoclip.write_videofile(f"{yt.title}({answers['resolution']}).mp4")

        os.remove('video.mp4')
        os.remove('audio.mp3')

    print("Video downloaded successfully.")
else:
    print("You selected Audio")
    # Download the audio
    print("Downloading audio...")
    for i in tqdm(range(100)):
        time.sleep(0.01)  # simulate time delay
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_file = 'temp_audio.mp4'
    audio_stream.download(filename=audio_file)
    print("Audio downloaded successfully.")

    # Convert the audio to mp3
    print("Converting audio to mp3...")
    if os.path.exists(audio_file):
        for i in tqdm(range(100)):
            time.sleep(0.01)  # simulate time delay
        output_file = f"{yt.title}.mp3"
        clip = AudioFileClip(audio_file)
        clip.write_audiofile(output_file)
        os.remove(audio_file)  # delete the temporary audio file
        print(f"Audio converted to mp3 successfully. Output file: {output_file}")
    else:
        print(f"Error: The file {audio_file} does not exist.")