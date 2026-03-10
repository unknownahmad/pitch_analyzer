# Real-Time Vocal Pitch Analyzer

A professional-grade Digital Signal Processing (DSP) application that tracks vocal pitch in real-time against a reference track. This project demonstrates high-level Python engineering, from mathematical signal analysis to multi-threaded GUI development.

##  Engineering Highlights

* **Autocorrelation Engine**: Replaced basic FFT peak detection with a robust autocorrelation algorithm to accurately find fundamental frequencies ($f_0$) while successfully ignoring loud harmonics that typically cause "octave jumps".
* **Multi-Threaded Architecture**: Implemented a decoupled threading system using the `threading` library to handle high-frequency audio I/O via `sounddevice` without blocking the GUI's main execution loop.
* **Hanning Window Integration**: Applied mathematical windowing to audio buffers to prevent spectral leakage, ensuring cleaner frequency transitions.
* **Signal Smoothing**: Engineered a Moving Average filter to iron out micro-jitters in human vocal input, providing a professional, readable pitch curve.
* **Dynamic Data Reporting**: Built a post-session analytics suite using `matplotlib.gridspec` for complex layout management and time-series data inspection.



##  Modular Architecture

The project is organized into a clean, hybrid structure for maintainability:
* **`analyzer.py`**: The "Math Engine" containing autocorrelation, scoring logic, and audio loading.
* **`gui.py`**: The "Live Dashboard" handling the real-time threading and scrolling visualization.
* **`report_view.py`**: The "Analytics View" which generates the final comparative graphs and time-series table.

##  Features

* **Live Pitch Monitoring**: Real-time visual feedback comparing user input (Red) to reference audio (Green).
* **Custom File Support**: Integrated file dialog for loading any `.wav` reference track.
* **Accuracy Scoring**: A mathematical percentage score based on frequency variance over the duration of the session.
* **Time-Series Inspection**: A detailed breakdown of performance sampled at 0.5s intervals for deep data analysis.
