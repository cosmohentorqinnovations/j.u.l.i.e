import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import cv2
import imageio
import os  # Import os module to handle paths

class FaceRecognitionApp:
    def __init__(self, window, window_title, gif_path):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("1280x720")  # Adjusted window size
        self.window.configure(bg='black')

        # Title label
        self.title_label = Label(window, text="IVAA", fg='cyan', bg='black', font=("Helvetica", 20, "italic"))
        self.title_label.pack(pady=20)

        # Video label
        self.video_label = Label(window)
        self.video_label.pack()

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # Load GIF frames
        self.gif_reader = imageio.get_reader(gif_path)
        self.gif_index = 0

        self.update()

        self.window.mainloop()

    def start_face_recognition(self):
        # This function can be extended to perform actual face recognition
        pass

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = self.face_cascade.detectMultiScale(frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            # Convert frame to PhotoImage
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))

            # Get the current GIF frame
            try:
                gif_frame = self.gif_reader.get_data(self.gif_index)
                self.gif_index = (self.gif_index + 1) % self.gif_reader.get_length()
            except IndexError:
                self.gif_index = 0
                gif_frame = self.gif_reader.get_data(self.gif_index)

            gif_image = Image.fromarray(gif_frame)
            canvas = Image.new("RGB", gif_image.size)
            canvas.paste(gif_image)

            # Position and resize the video feed to fit inside the blue square
            video_width, video_height = 485, 485  # Adjusted size
            video_image = Image.fromarray(cv2.resize(frame, (video_width, video_height)))
            canvas.paste(video_image, (328, 95))  # Adjusted position to fit within the blue square

            self.final_image = ImageTk.PhotoImage(canvas)
            self.video_label.config(image=self.final_image)

        self.window.after(10, self.update)

if __name__ == "__main__":
    # Use a relative path to the GIF file
    gif_path = os.path.join("assets", "BG.gif")  # Make sure the 'assets' folder contains your GIF file
    root = tk.Tk()
    app = FaceRecognitionApp(root, "J.U.L.I.E 1.0.0", gif_path)
