
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

import tkinter as tk

def checkbox_status():
    youtube_link = input_text.get()
    checkbox1_status = checkbox1.get()    
    print("YouTube Link:", youtube_link)
    print("Checkbox 1:", checkbox1_status)
    #if checkbox1_status == 1, download audio
    if checkbox1_status == 1:
        Download_audio(youtube_link)
        
    else:
        Download_video(youtube_link)
    
    


def Replace_spaces_with_underscores(string):
    # Replace all spaces with underscores
    string = string.replace(" ", "_")
    return string


def Download_video(link):
    # Create a folder named 'Videos', if there isn't one already
    if not os.path.exists('Videos'):
        os.mkdir('Videos')
    # Save video in the 'Videos' folder
    os.chdir('Videos')
    # Download the video
    youtubeObject = YouTube(link)
    
    try:
        youtubeObject.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().download()
        #rename the file to video
        new_filename = "video.mp4"
        os.rename(f'{youtubeObject.title}.mp4', new_filename)
    except:
        print("Download failed")
    print("Download complete")
    # return to the main directory
    os.chdir('..')
    
def Download_audio(link):
    # Create a folder named 'Audio', if there isn't one already
    if not os.path.exists('Audio'):
        os.mkdir('Audio')
    # Save audio in the 'Audio' folder
    os.chdir('Audio')
    # Download the audio
    youtubeObject = YouTube(link)
    
    try:
        
        youtubeObject.streams.filter(only_audio=True).first().download()
        #rename the file and replace spaces with underscores
        new_filename = "video.mp4"
        os.rename(f'{youtubeObject.title}.mp4', new_filename)
                
        #convert to mp3 named audio.mp3
        mp3_string = "ffmpeg -i video.mp4 -ab 160k -ac 2 -ar 44100 -vn audio.mp3"
        print(mp3_string)
        os.system(mp3_string)
        
        
        #find all mp4 files and delete them
        for file in os.listdir():
            if file.endswith(".mp4"):
                os.remove(file)
        
        
    except:
        print("Download failed")
    print("Download complete")
    # return to the main directory
    os.chdir('..')


    
if __name__ == "__main__":
    
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
    
    #Creates a box that outputs the status of the functions
    checkbox2_label = tk.Checkbutton(root, text="Video?", variable=checkbox2)
    checkbox2_label.pack()
    
    checkbox3_label = tk.Checkbutton(root, text="Transcribe?", variable=checkbox3)
    checkbox3_label.pack()


    submit_button = tk.Button(root, text="Submit", command=checkbox_status)
    submit_button.pack()

    root.mainloop()