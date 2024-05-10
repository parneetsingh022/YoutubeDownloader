from pytube import YouTube
import inquirer
from moviepy.editor import AudioFileClip
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
    video_streams = [stream for stream in yt.streams.filter(progressive=True)]

    # Create a list of available resolutions
    resolutions = [stream.resolution for stream in video_streams]

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
    yt.streams.filter(progressive=True, resolution=answers['resolution']).first().download()
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