import tkinter 
import cv2  # pip install opencv-python
import PIL.Image, PIL.ImageTk  # pip install pillow
from functools import partial
import threading
import time
import imutils  # pip install imutils
import os

# Constants
SET_WIDTH = 650
SET_HEIGHT = 368

# Load video stream
stream = cv2.VideoCapture("clip.mp4")
flag = True

# Tkinter window setup
window = tkinter.Tk()
window.title("Third Umpire DRS Simulator by Abhik Mehra")

# Canvas setup
canvas = tkinter.Canvas(window, width=SET_WIDTH, height=SET_HEIGHT)
canvas.pack()

# Load welcome screen image
# Load and display welcome.png properly

img_path = "welcome.png"
if not os.path.exists(img_path):
    print(f"Error: File '{img_path}' not found in directory: {os.getcwd()}")
else:
    welcome_img = cv2.imread(img_path)
    if welcome_img is None:
        print("Error: Image file could not be read, check format or corruption.")
    else:
        welcome_img = cv2.cvtColor(welcome_img, cv2.COLOR_BGR2RGB)
        welcome_img = imutils.resize(welcome_img, width=SET_WIDTH, height=SET_HEIGHT)
        welcome_photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(welcome_img))
        canvas.image = welcome_photo  # Save reference to avoid garbage collection
        canvas.create_image(0, 0, anchor=tkinter.NW, image=welcome_photo)
        print("✅ welcome.png loaded and displayed successfully.")

# Play video frames
def play(speed):
    global flag
    print(f"You clicked on play. Speed is {speed}")

    # Set current frame position
    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    if not grabbed:
        print("End of video or unable to read frame.")
        return
    frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
    frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
    if flag:
        canvas.create_text(134, 26, fill="black", font="Times 26 bold", text="Decision Pending")
    flag = not flag

# Display pending and decision sequence
def pending(decision):
    images = ["pending.png", "sponsor.png", "out.jpg" if decision == "out" else "not_out.png"]
    delays = [1.5, 2.5, 0]

    for img_path, delay in zip(images, delays):
        frame = cv2.imread(img_path)
        if frame is None:
            print(f"Error: {img_path} not found.")
            continue
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = imutils.resize(frame, width=SET_WIDTH, height=SET_HEIGHT)
        frame = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        canvas.image = frame
        canvas.create_image(0, 0, image=frame, anchor=tkinter.NW)
        time.sleep(delay)

# Decision buttons
def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def not_out():
    thread = threading.Thread(target=pending, args=("not out",))
    thread.daemon = 1
    thread.start()
    print("Player is not out")

# Playback control buttons
tkinter.Button(window, text="<< Previous (fast)", width=50, command=partial(play, -25)).pack()
tkinter.Button(window, text="<< Previous (slow)", width=50, command=partial(play, -2)).pack()
tkinter.Button(window, text="Next (slow) >>", width=50, command=partial(play, 2)).pack()
tkinter.Button(window, text="Next (fast) >>", width=50, command=partial(play, 25)).pack()
tkinter.Button(window, text="Give Out", width=50, command=out).pack()
tkinter.Button(window, text="Give Not Out", width=50, command=not_out).pack()

# Start Tkinter loop
window.mainloop()
