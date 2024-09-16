import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr
import threading

class SpeechToTextApp:
    def __init__(self, master):
        self.master = master
        self.master.title("voice2text")
        self.master.geometry("400x300")

        self.label = tk.Label(master, text="Click the button below to start recording:")
        self.label.pack(pady=10)

        self.start_button = tk.Button(master, text="start recording", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(master, text="stop  recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.text_box = tk.Text(master, width=50, height=10)
        self.text_box.pack(pady=10)

        self.recognizer = sr.Recognizer()
        self.is_recording = False
        self.audio_data = None

    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        threading.Thread(target=self.record).start()

    def stop_recording(self):
        self.is_recording = False

    def record(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.is_recording:
                audio = self.recognizer.listen(source, timeout=None)
                self.audio_data = audio  # ذخیره آخرین داده‌های صوتی ضبط شده
            self.process_audio(self.audio_data)  # پردازش آخرین داده‌های صوتی پس از توقف ضبط

    def process_audio(self, audio):
        try:
            text = self.recognizer.recognize_google(audio, language='fa-IR')
            self.text_box.insert(tk.END, text + '\n')
        except sr.UnknownValueError:
            messagebox.showerror("Error", "we could not recognize your voice.")
        except sr.RequestError as e:
            messagebox.showerror("Erro", f"Error in connection with the speech recognition service: {e}")
        finally:
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
