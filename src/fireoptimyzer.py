import customtkinter as ctk
from tkinter import messagebox

# Tema moderno
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# -------------------------------
# FUNZIONI (per ora sicure e demo)
# -------------------------------

def clean_temp():
    messagebox.showinfo("Pulizia", "Pulizia file temporanei completata (modalità sicura).")

def optimize_ram():
    messagebox.showinfo("RAM", "Ottimizzazione RAM completata (modalità sicura).")

def optimize_network():
    messagebox.showinfo("Rete", "Ottimizzazione rete completata (modalità sicura).")

def performance_mode():
    messagebox.showinfo("Performance", "Modalità prestazioni attiva (modalità sicura).")

# -------------------------------
# INTERFACCIA GRAFICA MIGLIORATA
# -------------------------------

app = ctk.CTk()
app.title("🔥 Fireoptimizer")
app.geometry("420x480")

title = ctk.CTkLabel(app, text="🔥 Fireoptimizer", font=("Arial", 25))
title.pack(pady=20)

btn1 = ctk.CTkButton(app, text="🧹 Pulizia File Temporanei", width=280, command=clean_temp)
btn1.pack(pady=12)

btn2 = ctk.CTkButton(app, text="🚀 Ottimizza RAM", width=280, command=optimize_ram)
btn2.pack(pady=12)

btn3 = ctk.CTkButton(app, text="🌐 Ottimizza Rete", width=280, command=optimize_network)
btn3.pack(pady=12)

btn4 = ctk.CTkButton(app, text="⚡ Modalità Prestazioni", width=280, command=performance_mode)
btn4.pack(pady=12)

footer = ctk.CTkLabel(app, text="Versione sicura — priva di rischi", font=("Arial", 12))
footer.pack(pady=30)

app.mainloop()

