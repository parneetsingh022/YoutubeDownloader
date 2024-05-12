from pytube import YouTube
import inquirer
from moviepy.editor import VideoFileClip, AudioFileClip
from tqdm import tqdm
import os
import time

def ask_for_url():
    """
    Prompt the user to input a YouTube video URL.

    Returns:
        str: The YouTube video URL entered by the user.
    """
    return input("Enter the YouTube video URL: ")

def get_youtube_object(url):
    """
    Create a YouTube object for the given URL.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        pytube.YouTube: The YouTube object.
    """
    return YouTube(url)

def select_download_type():
    """
    Prompt the user to select whether to download audio or video.

    Returns:
        str: The selected download type ('Audio' or 'Video').
    """
    questions = [
        inquirer.List('type',
                      message="What do you want to download?",
                      choices=['Audio', 'Video'],
                  ),
    ]
    answers = inquirer.prompt(questions)
    return answers['type']

def download_process(stream, filename):
    """
    Simulates the downloading process with a progress bar and downloads the stream to the specified filename.

    Args:
        stream (pytube.Stream): The stream to download.
        filename (str): The filename to save the downloaded file.
    """
    print(f"Downloading {filename}...")
    for i in tqdm(range(100)):
        time.sleep(0.01)  # simulate time delay
    stream.download(filename=filename)
    print(f"{filename} downloaded successfully.")

def combine_audio_and_video(video_filename, audio_filename, output_filename):
    """
    Combines the audio and video files and saves the result to the output filename.

    Args:
        video_filename (str): The filename of the video file.
        audio_filename (str): The filename of the audio file.
        output_filename (str): The filename to save the combined audio and video.
    """
    videoclip = VideoFileClip(video_filename)
    audioclip = AudioFileClip(audio_filename)
    videoclip.audio = audioclip
    videoclip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    videoclip.close()
    audioclip.close()

def download_video(yt):
    """
    Download the video from YouTube.

    Args:
        yt (pytube.YouTube): The YouTube object representing the video.
    """
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
    selected_stream = yt.streams.filter(res=answers['resolution']).first()
    if answers['resolution'] in ['360p', '720p']:
        download_process(selected_stream, filename=f"{yt.title}({answers['resolution']}).mp4")
    else:
        video_filename = 'video.mp4'
        audio_filename = 'audio.mp3'
        download_process(selected_stream, filename=video_filename)
        download_process(yt.streams.filter(only_audio=True).first(), filename=audio_filename)

        combine_audio_and_video(video_filename, audio_filename, f"{yt.title}({answers['resolution']}).mp4")

        os.remove(video_filename)
        os.remove(audio_filename)

    print("Video downloaded successfully.")

def download_audio(yt):
    """
    Download the audio from YouTube and convert it to mp3.

    Args:
        yt (pytube.YouTube): The YouTube object representing the video.
    """
    print("You selected Audio")
    # Download the audio
    audio_stream = yt.streams.filter(only_audio=True).first()
    download_process(audio_stream, filename='temp_audio.mp4')

    # Convert the audio to mp3
    print("Converting audio to mp3...")
    if os.path.exists('temp_audio.mp4'):
        output_file = f"{yt.title}.mp3"
        clip = AudioFileClip('temp_audio.mp4')
        clip.write_audiofile(output_file)
        os.remove('temp_audio.mp4')  # delete the temporary audio file
        print(f"Audio converted to mp3 successfully. Output file: {output_file}")
    else:
        print(f"Error: The file temp_audio.mp4 does not exist.")

def main():
    """
    Main function to orchestrate the downloading process.
    """
    url = ask_for_url()
    yt = get_youtube_object(url)
    download_type = select_download_type()
    if download_type == 'Video':
        download_video(yt)
    else:
        download_audio(yt)

if __name__ == "__main__":
    main()
