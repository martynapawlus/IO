# This script is responsible for graphic user interface of Traffic Analyzer application 

import time
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename

import PIL.Image, PIL.ImageTk
import cv2
import main
import os

# Class representing main window visible in GUI
class App:
    def __init__(self):

         self.window = tk.Tk()
         self.window.title("Analizator ruchu")

         # Adding all widgets
         self.window.geometry('450x220')
         self.window.resizable(False, False)
         self.video_window = 0
         self.filename = ""     # path to the video
         
         # selecting a video for an analysis
         self.l_vid_choice = tk.Label(self.window, text="Wybierz nagranie\n do analizy")
         self.l_vid_choice.grid(column=0, row=1)
         self.bt_vid_choice = tk.Button(self.window, text="Przeglądaj", command=self.search_btn, fg="blue")
         self.bt_vid_choice.grid(column=1, row=1)
         self.l_accept = tk.Label(self.window, text="Brak wgranego pliku", fg="grey")
         self.l_accept.grid(column=1, row=2)
         
         # starting an analysis
         self.l_an_start = tk.Label(self.window, text="Rozpocznij analizę\n wybranego nagrania")
         self.l_an_start.grid(column=0, row=3)
         self.bt_an_start = tk.Button(self.window, text="Start analizy", command=self.analyze_btn, fg="red", state="disabled")
         self.bt_an_start.grid(column=1, row=3)
         self.l_analyze = tk.Label(self.window, fg="grey", text="")
         self.l_analyze.grid(column=1, row=4)
            
         # saving the results to CSV file
         self.l_vid_choice = tk.Label(self.window, text="Zapisz wyniki\n do pliku CSV")
         self.l_vid_choice.grid(column=0, row=5)
         self.bt_save_csv = tk.Button(self.window, text="Zapisz CSV", fg="blue", command=self.save_csv_btn, state="disabled")
         self.bt_save_csv.grid(column=1, row=5)
        
         # playing analyzed video
         self.l_vid_choice = tk.Label(self.window, text="Odtwórz przeanalizowane\n nagranie")
         self.l_vid_choice.grid(column=0, row=6)
         self.bt_play_vid = tk.Button(self.window, text="Odtwórz film", command=self.play_btn, fg="blue", state="disabled")
         self.bt_play_vid.grid(column=1, row=6)
        
         self.window.mainloop()                                         # run Tkinter main window       

# Action listeners
    def search_btn(self):
        acceptable_types = [('Pliki wideo', '*.avi;*.mp4;*.mov')]
        self.filename = askopenfilename(filetype=acceptable_types)
        self.l_accept["text"] = ".../" + os.path.split(self.filename)[1]
        if self.filename != "":
            self.bt_an_start["state"] = "active"


    def analyze_btn(self):
        self.l_analyze["text"] = "Przetwarzanie video ..."
        self.traffic_analyzer = main.Traffic_Analyzer(self.filename)    # creating an object of Traffic_Analyzer class defined in main.py
        self.traffic_analyzer.video_analyze()                           # starting an analysis
        # enabling playing video and saving the results
        self.l_analyze["text"] = "Przetwarzanie video zakończone!"
        self.bt_play_vid["state"] = "active"
        self.bt_save_csv["state"] = "active"

    def save_csv_btn(self):
        self.traffic_analyzer.write_timestamps()                        # saving the results

    def play_btn(self):
        self.video_window = tk.Toplevel(self.window)                    # creating new window in GUI for video playing
        self.video_window.title("Przeanalizowane video")
        self.vid = MyVideoCapture(self.traffic_analyzer.output_video_file)
        self.canvas = tk.Canvas(self.video_window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self.delay = 15
        self.update()

# Functions responsible for playing the video
    def snapshot(self):
             ret, frame = self.vid.get_frame()                          # getting a frame from the video source

             if ret:
                 cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        ret, frame = self.vid.get_frame()                               # getting a frame from the video source

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.video_window.after(self.delay, self.update)

# Class representing playing analyzed video window visible in GUI
class MyVideoCapture:
     def __init__(self, video_source=0):

         self.vid = cv2.VideoCapture(video_source)                      # opening the video source
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)            # getting video source width and height
         self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

     def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (None)

     # Release the video source when the object is destroyed
     def __del__(self):
         if self.vid.isOpened():
             self.vid.release()
# Create a window and pass it to the Application object
App()
