import customtkinter as ctk
from customtkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import analyzer
import report_view # NEW IMPORT
import sounddevice as sd
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class PitchApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Real-Time Vocal Analyzer")
        self.geometry("1000x700")
        self.fs = None
        self.ref_audio = None
        self.duration = 0
        self.is_recording = False
        self.ref_history = []
        self.user_history = []
        self.setup_ui()

    def setup_ui(self):
        self.control_frame = ctk.CTkFrame(self)
        self.control_frame.pack(pady=20, padx=20, fill="x")
        self.btn_load = ctk.CTkButton(self.control_frame, text="Browse Reference", command=self.load_audio)
        self.btn_load.pack(side="left", padx=20)
        self.btn_record = ctk.CTkButton(self.control_frame, text="Start Real-Time", command=self.start_live, state="disabled", fg_color="darkred")
        self.btn_record.pack(side="left", padx=20)
        self.status = ctk.CTkLabel(self.control_frame, text="Upload .wav to start", font=("Helvetica", 14))
        self.status.pack(side="right", padx=20)

        self.graph_frame = ctk.CTkFrame(self)
        self.graph_frame.pack(pady=10, padx=20, fill="both", expand=True)
        self.fig, self.ax = plt.subplots()
        self.fig.patch.set_facecolor('#2b2b2b')
        self.ax.set_facecolor('#2b2b2b')
        self.ax.tick_params(colors='white')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.graph_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_audio(self):
        path = filedialog.askopenfilename(filetypes=[("WAV Audio", "*.wav")])
        if path:
            self.fs, self.ref_audio, self.duration = analyzer.load_reference(path)
            self.status.configure(text=f"Ready: {round(self.duration, 1)}s")
            self.btn_record.configure(state="normal")

    def start_live(self):
        self.is_recording, self.ref_history, self.user_history = True, [], []
        self.btn_record.configure(state="disabled")
        threading.Thread(target=self.audio_thread, daemon=True).start()
        self.update_graph_loop()

    def audio_thread(self):
        chunk = int(self.fs * 0.1)
        with sd.InputStream(samplerate=self.fs, channels=1, blocksize=chunk) as stream:
            for i in range(int(len(self.ref_audio) / chunk)):
                if not self.is_recording: break
                user_chunk, _ = stream.read(chunk)
                ref_chunk = self.ref_audio[i*chunk : (i+1)*chunk]
                self.ref_history.append(analyzer.get_pitch_autocorr(ref_chunk, self.fs))
                self.user_history.append(analyzer.get_pitch_autocorr(user_chunk[:, 0], self.fs))
        self.is_recording = False

    def update_graph_loop(self):
        if not self.is_recording and self.user_history:
            score = analyzer.calculate_final_score(self.ref_history, self.user_history)
            self.ax.set_title(f"Final Score: {score}%", color="white")
            self.btn_record.configure(state="normal")
            report_view.ReportWindow(self, self.ref_history, self.user_history) # CALL NEW WINDOW
            return

        if self.is_recording:
            self.ax.clear()
            self.ax.plot(self.ref_history[-50:], color="#00ff00", linewidth=3)
            self.ax.plot(self.user_history[-50:], color="#ff3333", linewidth=3)
            self.ax.set_ylim(50, 600)
            self.canvas.draw()
            self.after(100, self.update_graph_loop)

if __name__ == "__main__":
    app = PitchApp()
    app.mainloop()