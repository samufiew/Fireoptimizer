import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def clean_temp():
    messagebox.showinfo("Pulizia", 
        "Qui verrà eseguita la pulizia dei file temporanei.\n(Sicuro: non fa ancora modifiche reali)"
    )

def boost_ram():
    messagebox.showinfo("RAM", 
        "Qui verrà eseguita l’ottimizzazione RAM.\n(Sicuro: funzione demo)"
    )

def flush_dns():
    messagebox.showinfo("Rete", 
        "Qui verrà eseguita la pulizia DNS.\n(Sicuro: funzione demo)"
    )

def performance_mode():
    messagebox.showinfo("Performance", 
        "Qui verrà attivata la modalità alte prestazioni.\n(Sicuro: funzione demo)"
    )

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
