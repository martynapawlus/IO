import time
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import askopenfilename

import PIL.Image, PIL.ImageTk
import cv2
import main

"""window = tk.Tk()
# Code to add widgets will go here...
window.geometry('400x200')
#Action listeners
filename = ""

def clicked_bt1():
    global filename
    #acceptable_types = [('Pliki wideo', '*.avi;*.mp4;*.mov')]
    filename = askopenfilename()
    l_accept = tk.Label(window, text=filename)
    l_accept.grid(column=2, row=1)


def clicked_bt2():
    if filename != "":
        print(filename)
        main.video_analyze(filename)

def clicked_btn3():
    self.vid = MyVideoCapture("output.avi")
    self.canvas = tk.Canvas(window, width=self.vid.width, height=self.vid.height)
    self.canvas.pack()

#Appereance
l_vid_choice = tk.Label(window, text="Wybierz nagranie\n do analizy")
l_vid_choice.grid(column=0, row=1)
bt_vid_choice = tk.Button(window, text="Przeglądaj", command=clicked_bt1, fg="blue")
bt_vid_choice.grid(column=1, row=1)
l_accept = tk.Label(window, text="Brak wgranego pliku", fg="grey")
l_accept.grid(column=1, row=2)
l_vid_choice = tk.Label(window, text="Rozpocznij analizę\n wybranego nagrania")
l_vid_choice.grid(column=0, row=3)
bt_an_start = tk.Button(window, text="Start analizy", command=clicked_bt2, fg="red")
bt_an_start.grid(column=1, row=3)
l_vid_choice = tk.Label(window, text="Zapisz film\n wynikowy po analizie")
l_vid_choice.grid(column=0, row=4)
bt_save_vid = tk.Button(window, text="Zapisz film", fg="blue")
bt_save_vid.grid(column=1, row=4)
l_vid_choice = tk.Label(window, text="Odtwórz przeanalizowane\n nagranie")
l_vid_choice.grid(column=0, row=5)
bt_play_vid = tk.Button(window, text="Odtwórz film", fg="blue")
bt_play_vid.grid(column=1, row=5)"""

#window.mainloop()

class App:
    def __init__(self):
        # open video source (by default this will try to open the computer webcam)

         # Create a canvas that can fit the above video source size

         # Button that lets the user take a snapshot
         """self.btn_snapshot=tkinter.Button(window, text="Snapshot", width=50, command=self.snapshot)
         self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)

         # After it is called once, the update method will be automatically called every delay milliseconds
         self.delay = 15
         self.update()"""

         self.window = tk.Tk()

         #videoooo
         # Code to add widgets will go here...
         self.window.geometry('400x200')
         self.video_window = 0
         # Action listeners
         self.filename = ""
         self.l_vid_choice = tk.Label(self.window, text="Wybierz nagranie\n do analizy")
         self.l_vid_choice.grid(column=0, row=1)
         self.bt_vid_choice = tk.Button(self.window, text="Przeglądaj", command=self.clicked_bt1, fg="blue")
         self.bt_vid_choice.grid(column=1, row=1)
         self.l_accept = tk.Label(self.window, text="Brak wgranego pliku", fg="grey")
         self.l_accept.grid(column=1, row=2)
         self.l_vid_choice = tk.Label(self.window, text="Rozpocznij analizę\n wybranego nagrania")
         self.l_vid_choice.grid(column=0, row=3)
         self.bt_an_start = tk.Button(self.window, text="Start analizy", command=self.clicked_bt2, fg="red")
         self.bt_an_start.grid(column=1, row=3)
         self.l_vid_choice = tk.Label(self.window, text="Zapisz film\n wynikowy po analizie")
         self.l_vid_choice.grid(column=0, row=4)
         self.bt_save_vid = tk.Button(self.window, text="Zapisz film", fg="blue")
         self.bt_save_vid.grid(column=1, row=4)
         self.l_vid_choice = tk.Label(self.window, text="Odtwórz przeanalizowane\n nagranie")
         self.l_vid_choice.grid(column=0, row=5)
         self.bt_play_vid = tk.Button(self.window, text="Odtwórz film", command=self.clicked_bt3, fg="blue")
         self.bt_play_vid.grid(column=1, row=5)

         self.window.mainloop()

    def clicked_bt1(self):
        # acceptable_types = [('Pliki wideo', '*.avi;*.mp4;*.mov')]
        self.filename = askopenfilename()
        self.l_accept = tk.Label(self.window, text=self.filename)
        self.l_accept.grid(column=2, row=1)

    def clicked_bt2(self):
        if self.filename != "":
            print(self.filename)
            main.video_analyze(self.filename)

    def clicked_bt3(self):
        self.video_window = tk.Toplevel(self.window)
        self.video_window.title("Przeanalizowane video")
        self.vid = MyVideoCapture("output.avi")
        self.canvas = tk.Canvas(self.video_window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self.delay = 15
        self.update()

    def snapshot(self):
             # Get a frame from the video source
             ret, frame = self.vid.get_frame()

             if ret:
                 cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.video_window.after(self.delay, self.update)


class MyVideoCapture:
     def __init__(self, video_source=0):
         # Open the video source

         self.vid = cv2.VideoCapture(video_source)
         if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

         # Get video source width and height
         self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
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
