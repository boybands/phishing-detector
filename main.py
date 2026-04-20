import tkinter as tk
from tkinter import ttk, messagebox
from detector_typo import cek_typo_phishing
import pyttsx3

engine = pyttsx3.init()

def speak_status(status):
    if status == "legit":
        engine.say("Link ini adalah link asli")
    elif status == "phishing":
        engine.say("Link ini adalah link palsu")
    else:
        engine.say("Link ini adalah link tidak diketahui")
    engine.runAndWait()

def deteksi():
    url = entry.get().strip()

    if not url:
        messagebox.showwarning("Peringatan", "Masukkan URL terlebih dahulu!")
        return

    hasil, status = cek_typo_phishing(url)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, hasil)

    if status == "phishing":
        output_text.configure(bg="#ffebee", fg="#b71c1c")
    elif status == "legit":
        output_text.configure(bg="#e8f5e9", fg="#1b5e20")
    else:
        output_text.configure(bg="#fff8e1", fg="#e65100")

    # 🔊 Tambahkan suara
    speak_status(status)


root = tk.Tk()
root.title("Deteksi Phishing Typosquatting - Layanan Akun Digital")
root.geometry("850x600")
root.configure(bg="#f4f6f9")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

title = ttk.Label(main_frame,
                  text="Deteksi Phishing Berbasis Typosquatting\nLayanan Akun Digital Populer Indonesia",
                  font=("Segoe UI", 16, "bold"))
title.pack(pady=(0, 20))

entry = ttk.Entry(main_frame, font=("Segoe UI", 12))
entry.pack(fill="x", ipady=5)
entry.focus()

btn = ttk.Button(main_frame, text="Analisis Domain", command=deteksi)
btn.pack(pady=10)

output_text = tk.Text(main_frame,
                      wrap="word",
                      font=("Consolas", 11),
                      relief="solid",
                      padx=10,
                      pady=10)
output_text.pack(fill="both", expand=True)

root.mainloop()
