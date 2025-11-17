import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def clean_temp():
    os.system("del /q/f/s %TEMP%\\*")
    messagebox.showinfo("Pulizia", "File temporanei rimossi!")

def boost_ram():
    os.system("wmic process where name!='explorer.exe' call setpriority 128")
    messagebox.showinfo("RAM", "RAM ottimizzata!")

def flush_dns():
    os.system("ipconfig /flushdns")
    messagebox.showinfo("Rete", "DNS pulito!")

def performance_mode():
    os.system("powercfg -setactive SCHEME_MIN")
    messagebox.showinfo("Performance", "Modalità prestazioni massime attivata!")

app = ctk.CTk()
app.title("Fireoptimizer")
app.geometry("420x450")

title = ctk.CTkLabel(app, text="🔥 Fireoptimizer", font=("Arial", 25))
title.pack(pady=20)

btn1 = ctk.CTkButton(app, text="🧹 Pulizia File Temporanei", width=260, command=clean_temp)
btn1.pack(pady=10)

btn2 = ctk.CTkButton(app, text="🚀 Boost RAM", width=260, command=boost_ram)
btn2.pack(pady=10)

btn3 = ctk.CTkButton(app, text="🌐 Flush DNS (Rete)", width=260, command=flush_dns)
btn3.pack(pady=10)

btn4 = ctk.CTkButton(app, text="⚡ Modalità Massime Prestazioni", width=260, command=performance_mode)
btn4.pack(pady=10)

app.mainloop()

