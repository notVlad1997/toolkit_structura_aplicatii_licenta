import tkinter as tk


class FrameWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        #self.master.title("Fereastra Cu Bare Titlu")

        # Configurare pentru a face frame-ul să arate ca o fereastră
        #self.master.geometry("600x300")  # Setează dimensiunea inițială a ferestrei
        self.master.configure(borderwidth=5, relief="ridge")  # Adaugă bordură la fereastra principală

        # Crează un frame în interiorul ferestrei principale
        self.frame_interior = tk.Frame(self.master, width=300, height=200, borderwidth=5, relief="ridge")
        self.frame_interior.pack_propagate(
            False)  # Nu permite frame-ului să-și ajusteze dimensiunile în funcție de conținut

        # Plasează frame-ul în mijlocul spațiului disponibil între bara laterală și marginea dreaptă a ferestrei
        self.frame_interior.place(relx=0.5, rely=0.5, anchor="center")

        # Adaugă bara de titlu fictivă peste frame-ul interior
        self.bara_titlu = tk.Frame(self.frame_interior, height=15, relief="raised")
        self.bara_titlu.pack(fill="x")
        self.bara_titlu.pack_propagate(
            False)  # Nu permite barei de titlu să-și ajusteze dimensiunile în funcție de conținut

        # Adaugă butoanele de minimizare, maximizare și închidere în bara de titlu
        self.buton_minimizare = tk.Button(self.bara_titlu, text="-")
        self.buton_maximizare = tk.Button(self.bara_titlu, text="□")
        self.buton_inchidere = tk.Button(self.bara_titlu, text="x")

        # Aranjează butoanele pe partea dreaptă fără spații între ele
        self.buton_inchidere.pack(side="right")
        self.buton_maximizare.pack(side="right")
        self.buton_minimizare.pack(side="right")

        # Adaugă o linie de separare între bara de titlu și conținutul frame-ului
        self.separator = tk.Frame(self.frame_interior, height=2, relief="sunken",
                                   background="gray")  # Ajustează înălțimea și culoarea la nevoie
        self.separator.pack(side="top", fill="x", pady=2)  # pady adaugă un spațiu între bara de titlu și separator

