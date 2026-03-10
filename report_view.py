import customtkinter as ctk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

class ReportWindow(ctk.CTkToplevel):
    def __init__(self, parent, ref_history, user_history):
        super().__init__(parent)
        self.title("Post-Session Analysis Report")
        self.geometry("1100x800")
        self.attributes('-topmost', True)
        
        self.ref_history = ref_history
        self.user_history = user_history

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", pady=(20, 0), padx=20)
        
        btn_table = ctk.CTkButton(btn_frame, text="Open Time-Series Data Table", command=self.open_data_table)
        btn_table.pack(side="right")
        
        self.setup_graphs()

    def setup_graphs(self):
        fig = plt.figure(figsize=(10, 6))
        fig.patch.set_facecolor('#2b2b2b')
        gs = gridspec.GridSpec(2, 2, figure=fig)
        
        ax1 = fig.add_subplot(gs[0, :])
        ax2 = fig.add_subplot(gs[1, 0])
        ax3 = fig.add_subplot(gs[1, 1])
        
        ax1.set_facecolor('#2b2b2b')
        ax1.plot(self.ref_history, label="Target", color="#00ff00")
        ax1.plot(self.user_history, label="User", color="#ff3333")
        ax1.set_title("Combined Pitch Comparison", color="white")
        ax1.tick_params(colors='white')
        ax1.legend(facecolor='#2b2b2b', labelcolor='white')
        
        ax2.set_facecolor('#2b2b2b')
        ax2.plot(self.ref_history, color="#00ff00")
        ax2.set_title("Target Reference Pitch", color="white")
        ax2.tick_params(colors='white')
        
        ax3.set_facecolor('#2b2b2b')
        ax3.plot(self.user_history, color="#ff3333")
        ax3.set_title("User Recorded Pitch", color="white")
        ax3.tick_params(colors='white')
        
        plt.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self)
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=10, padx=20)

    def open_data_table(self):
        table_window = ctk.CTkToplevel(self)
        table_window.title("Time-Series Data (0.5s Intervals)")
        table_window.geometry("700x600")
        table_window.attributes('-topmost', True)
        
        frame = ctk.CTkScrollableFrame(table_window)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        headers = ["Time (s)", "Target (Hz)", "User (Hz)", "Difference"]
        for i, h in enumerate(headers):
            ctk.CTkLabel(frame, text=h, font=("Helvetica", 12, "bold"), width=140).grid(row=0, column=i, padx=5, pady=5)
        
        for i in range(0, len(self.ref_history), 5):
            t, r, u = i * 0.1, self.ref_history[i], self.user_history[i]
            d = u - r
            
            ctk.CTkLabel(frame, text=f"{t:.1f}", width=140).grid(row=i+1, column=0, pady=2)
            ctk.CTkLabel(frame, text=f"{r:.1f}", width=140).grid(row=i+1, column=1, pady=2)
            ctk.CTkLabel(frame, text=f"{u:.1f}", width=140).grid(row=i+1, column=2, pady=2)
            ctk.CTkLabel(frame, text=f"{d:.1f}", width=140).grid(row=i+1, column=3, pady=2)