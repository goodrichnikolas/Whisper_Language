'''
This program will allow you to input a YouTube link and download the video in the highest resolution possible.
Transcribe the video into a text file.
Convert the video into an audio file.
Finally, it will apply the subtitles to the video file using SRT files.
'''

from pytube import YouTube
import os
import whisper
import time
import tkinter as tk
import json
import glob
import torch
import shutil


def checkbox_status():
    '''
    Reads the Tkinter box and returns the status of the checkboxes and dropdown menu
    '''
    #clear out files
    clear_files()
    
    
    youtube_link = input_text.get()
    checkbox1_status = checkbox1.get()
    checkbox2_status = checkbox2.get()
    checkbox3_status = checkbox3.get()
    # Get status of dropdown menu
    selected_value_status = selected_value.get()
    print("Selected value:", selected_value_status)
    print("YouTube Link:", youtube_link)
    print("Checkbox 1:", checkbox1_status)
    # if checkbox1_status == 1, download audio
    if checkbox1_status == 1:
        download_audio(youtube_link)

    if checkbox2.get() == 1:
        download_video(youtube_link)

    if checkbox3.get() == 1:
        transcribe_audio(selected_value_status)


def transcribe_audio(model_selection):
    '''
    Uses the whisper library to transcribe the audio file
    '''
    # convert model to lowercase
    model_selection = model_selection.lower()

    # change directory to Audio
    os.chdir('Audio')

    if model_selection == 'large':
        cmd = f"whisper audio.mp3 --model {model_selection}"
    else:    
        cmd = f"whisper audio.mp3 --model {model_selection}.en"
    os.system(cmd)

    # save result to a text file and go back to main directory
    os.chdir('..')

    # add srt to video
    add_srt_to_video()



def download_video(link):
    '''
    Downloads the youtube video in the highest resolution possible
    '''
    # Create a folder named 'Videos', if there isn't one already
    if not os.path.exists('Videos'):
        os.mkdir('Videos')
    # Save video in the 'Videos' folder
    os.chdir('Videos')
    # Download the video
    youtubeObject = YouTube(link)

    try:
        youtubeObject.streams.filter(progressive=True, file_extension='mp4').order_by(
            'resolution').desc().first().download()
        # rename the file to video
        new_filename = "video.mp4"
        print(f'{youtubeObject.title}.mp4')
        name = glob.glob(f'*.mp4')
        #rename the file
        os.rename(f'{name[0]}', new_filename)
    except:
        print("Download failed")
    print("Download complete")
    # return to the main directory
    os.chdir('..')


def download_audio(link):
    '''
    Downloads the video's audio in the highest resolution possible
    '''
    
    # Create a folder named 'Audio', if there isn't one already
    if not os.path.exists('Audio'):
        os.mkdir('Audio')
    # Save audio in the 'Audio' folder
    os.chdir('Audio')
    # Download the audio
    youtubeObject = YouTube(link)

    try:
        # download the video
        youtubeObject.streams.filter(only_audio=True).first().download()
        mp4_files = glob.glob('*.mp4')
        new_filename = "video.mp4"

        os.rename(f'{mp4_files[0]}', new_filename)

        # convert to mp3 named audio.mp3 using the python os module
        mp3_string = "ffmpeg -i video.mp4 audio.mp3"
        print(mp3_string)
        os.system(mp3_string)

        # find all mp4 files and delete them
        for file in os.listdir():
            if file.endswith(".mp4"):
                os.remove(file)

    except:
        print("Download failed")
    print("Download complete")
    # return to the main directory
    os.chdir('..')


def add_srt_to_video():
    '''
    Takes the SRT video generated by the whisper model and
    adds it to the video file
    '''
    # change directory to videos
    os.chdir('Videos')

    # copy audio.mp3.srt from the Audio folder to here
    shutil.copy('../Audio/audio.mp3.srt', '.')

    # rename the file to subtitles.srt
    new_filename = "subtitles.srt"
    os.rename(f'audio.mp3.srt', new_filename)

    # use ffmpeg to add the subtitles to the video
    ffmpeg_string = "ffmpeg -i video.mp4 -vf subtitles=subtitles.srt video_with_subtitles.mp4"
    os.system(ffmpeg_string)

    # delete srt file
    os.remove('subtitles.srt')

    # return to main directory
    os.chdir('..')


def clear_files():
    '''
    Clears out all files for debugging reasons
    '''
     # delete the audio and video folders if they exist
    if os.path.exists('Audio'):
        shutil.rmtree('Audio')
    if os.path.exists('Videos'):
        shutil.rmtree('Videos')

if __name__ == "__main__":
    
    # delete transcription.json, transcription.txt, and subtitles.srt if they exist
    file_list = ['transcription.json', 'transcription.txt', 'subtitles.srt']
    for file in file_list:
        if os.path.exists(file):
            os.remove(file)

    link = 'https://www.youtube.com/watch?v=xH9c_fehh9c'
    root = tk.Tk()
    root.geometry("400x200")
    root.title("YouTube Link Checker")

    input_text = tk.StringVar()
    checkbox1 = tk.IntVar()
    checkbox2 = tk.IntVar()
    checkbox3 = tk.IntVar()

    input_label = tk.Label(root, text="Enter YouTube Link:")
    input_label.pack()

    input_entry = tk.Entry(root, textvariable=input_text)
    input_entry.pack()

    checkbox1_label = tk.Checkbutton(root, text="Audio?", variable=checkbox1)
    checkbox1_label.pack()

    # Creates a box that outputs the status of the functions
    checkbox2_label = tk.Checkbutton(root, text="Video?", variable=checkbox2)
    checkbox2_label.pack()

    checkbox3_label = tk.Checkbutton(
        root, text="Transcribe?", variable=checkbox3)
    checkbox3_label.pack()

    # create a dropdown menu with 5 options that is greyed out until the user clicks checkbox3
    selected_value = tk.StringVar()
    dropdown = tk.OptionMenu(root, selected_value,
                             "Tiny", "Base", "Small", "Medium", "Large")
    dropdown.pack()

    # create a submit button

    submit_button = tk.Button(root, text="Submit", command=checkbox_status)
    submit_button.pack()

    root.mainloop()