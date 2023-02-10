
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
    


def checkbox_status():
    youtube_link = input_text.get()
    checkbox1_status = checkbox1.get()
    checkbox2_status = checkbox2.get()
    checkbox3_status = checkbox3.get()
    #Get status of dropdown menu
    selected_value_status = selected_value.get()
    print("Selected value:", selected_value_status)
    print("YouTube Link:", youtube_link)
    print("Checkbox 1:", checkbox1_status)
    #if checkbox1_status == 1, download audio
    if checkbox1_status == 1:
        Download_audio(youtube_link)
        
    if checkbox2.get() == 1:
        Download_video(youtube_link)
        
    if checkbox3.get() == 1:
        transcribe_audio(selected_value_status)
    
def transcribe_audio(model_selection):
    #convert model selection to lowercase
    model_selection = model_selection.lower()
    
    model = whisper.load_model(model_selection)
    
    #change directory to Audio
    os.chdir('Audio')
    
    result = model.transcribe("audio.mp3")
    #save result to a text file and go back to main directory
    os.chdir('..')
    with open("transcription.txt", "w") as f:
        f.write(result['text'])
    #save the whole dictionary to a json file
    with open("transcription.json", "w") as f:
        json.dump(result, f)
    #create an srt file
    create_srt_file()


def Replace_spaces_with_underscores(string):
    # Replace all spaces with underscores
    string = string.replace(" ", "_")
    return string

def create_srt_file():
    with open("transcription.json", "r") as f:
        data = json.load(f)
    segments = data['segments']
    count = 1
    for segment in segments:
        start_time = segment['start']
        end_time = segment['end']
        text = segment['text']
        with open("subtitles.srt", "a") as f:
            # Write the segment number, then the start and end times in correct SRT format
            f.write(f"{count}\n")
            f.write(f"{time.strftime('%H:%M:%S', time.gmtime(start_time))},{int((start_time - int(start_time)) * 1000)} --> {time.strftime('%H:%M:%S', time.gmtime(end_time))},{int((end_time - int(end_time)) * 1000)}\n")
            # Write the text
            f.write(f"{text}\n\n")
            count += 1
    

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
        #download the video
        youtubeObject.streams.filter(only_audio=True).first().download()
        mp4_files = glob.glob('*.mp4')
        new_filename = "video.mp4"
        
        os.rename(f'{mp4_files[0]}', new_filename)
                
        #convert to mp3 named audio.mp3 using the python os module
        mp3_string = "ffmpeg -i video.mp4 audio.mp3"
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
    
    #create a dropdown menu with 5 options that is greyed out until the user clicks checkbox3
    selected_value = tk.StringVar()
    dropdown = tk.OptionMenu(root, selected_value, "Tiny", "Base", "Small", "Medium", "Large")
    dropdown.pack()
    
    
    #create a submit button
    


    submit_button = tk.Button(root, text="Submit", command=checkbox_status)
    submit_button.pack()

    root.mainloop()