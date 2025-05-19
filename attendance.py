import os
import cv2
import datetime
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import face_recognition

import util


class FaceAttendanceApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("1200x520+350+100")
        self.window.title("Face Attendance System")

        # Buttons
        util.get_button(self.window, 'Login', 'green', self.login).place(x=750, y=200)
        util.get_button(self.window, 'Logout', 'red', self.logout).place(x=750, y=280)
        util.get_button(self.window, 'Register New User', 'gray', self.register_new_user, fg='black').place(x=750, y=360)

        # Webcam label
        self.video_label = util.get_img_label(self.window)
        self.video_label.place(x=10, y=0, width=700, height=500)

        # Camera
        self.cap = cv2.VideoCapture(0)
        self.update_video()

        # Directories
        self.db_dir = './db'
        self.log_path = './log.txt'
        os.makedirs(self.db_dir, exist_ok=True)

    def update_video(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame = frame
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            imgtk = ImageTk.PhotoImage(image=img)
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        self.video_label.after(20, self.update_video)

    def recognize_face(self, frame):
        encodings_current = face_recognition.face_encodings(frame)
        if not encodings_current:
            return 'no_persons_found'

        for filename in os.listdir(self.db_dir):
            with open(os.path.join(self.db_dir, filename), 'rb') as f:
                saved_encoding = pickle.load(f)
            match = face_recognition.compare_faces([saved_encoding], encodings_current[0])[0]
            if match:
                return filename.replace('.pickle', '')
        return 'unknown_person'

    def log_attendance(self, name, status):
        with open(self.log_path, 'a') as f:
            f.write(f"{name},{datetime.datetime.now()},{status}\n")

    def login(self):
        name = self.recognize_face(self.current_frame)
        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Login Failed', 'Face not recognized. Please try again or register.')
        else:
            util.msg_box('Login Successful', f"Welcome back, {name}!")
            self.log_attendance(name, 'in')

    def logout(self):
        name = self.recognize_face(self.current_frame)
        if name in ['unknown_person', 'no_persons_found']:
            util.msg_box('Logout Failed', 'Face not recognized. Please try again.')
        else:
            util.msg_box('Logout Successful', f"Goodbye, {name}!")
            self.log_attendance(name, 'out')

    def register_new_user(self):
        self.reg_window = tk.Toplevel(self.window)
        self.reg_window.geometry("1200x520+370+120")
        self.reg_window.title("Register New User")

        util.get_button(self.reg_window, 'Accept', 'green', self.save_new_user).place(x=750, y=300)
        util.get_button(self.reg_window, 'Cancel', 'red', self.reg_window.destroy).place(x=750, y=380)

        self.entry_name = util.get_entry_text(self.reg_window)
        self.entry_name.place(x=750, y=150)

        util.get_text_label(self.reg_window, 'Enter username:').place(x=750, y=100)

        self.capture_label = util.get_img_label(self.reg_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)

        self.capture_frame()

    def capture_frame(self):
        img = cv2.cvtColor(self.current_frame, cv2.COLOR_BGR2RGB)
        self.captured_image = self.current_frame.copy()
        imgtk = ImageTk.PhotoImage(Image.fromarray(img))
        self.capture_label.imgtk = imgtk
        self.capture_label.configure(image=imgtk)

    def save_new_user(self):
        name = self.entry_name.get("1.0", "end-1c").strip()
        if not name:
            util.msg_box("Error", "Username cannot be empty!")
            return

        encodings = face_recognition.face_encodings(self.captured_image)
        if not encodings:
            util.msg_box("Error", "No face detected. Please try again.")
            return

        with open(os.path.join(self.db_dir, f"{name}.pickle"), 'wb') as f:
            pickle.dump(encodings[0], f)

        util.msg_box("Success", f"User '{name}' registered successfully.")
        self.reg_window.destroy()

    def start(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = FaceAttendanceApp()
    app.start()
