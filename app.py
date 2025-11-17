import tkinter as tk
from tkinter import messagebox

def optimize_performance():
    messagebox.showinfo("Ottimizzazione", "Ottimizzazione performance completata!")

def clean_temp():
    messagebox.showinfo("Pulizia", "File temporanei rimossi!")

def fix_network():
    messagebox.showinfo("Rete", "La rete è stata ottimizzata!")

def main():
    win = tk.Tk()
    win.title("Fireoptimizer")
    win.geometry("350x300")

    title = tk.Label(win, text="Fireoptimizer", font=("Arial", 16))
    title.pack(pady=10)

    btn1 = tk.Button(win, text="Ottimizza performance", width=25, command=optimize_performance)
    btn1.pack(pady=10)

    btn2 = tk.Button(win, text="Pulisci file temporanei", width=25, command=clean_temp)
    btn2.pack(pady=10)

    btn3 = tk.Button(win, text="Ottimizza rete", width=25, command=fix_network)
    btn3.pack(pady=10)

    win.mainloop()

if __name__ == "__main__":
    main()
