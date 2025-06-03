import tkinter as tk
from PIL import Image, ImageTk
from utils import resource_path  

class SliderCustom(tk.Canvas):
    def __init__(self, master, length=100, **kwargs):
        super().__init__(master, width=length, height=30, bg="#000000", highlightthickness=0, **kwargs)
        self.length = length

        chemin_barre = resource_path("Images/slider.png")
        chemin_knob = resource_path("Images/point.png")

        self.bar_img = ImageTk.PhotoImage(Image.open(chemin_barre).resize((length, 10)))
        self.knob_img = ImageTk.PhotoImage(Image.open(chemin_knob).resize((20, 20)))

        self.create_image(0, 10, anchor='nw', image=self.bar_img, tags="barre")
        self.knob = self.create_image(0, 5, anchor='nw', image=self.knob_img, tags="curseur")

        self.value = 0  # valeur 0-100
        self.command = None  # callback par défaut

        self.bind("<Button-1>", self.clic)
        self.bind("<B1-Motion>", self.drag)

    def clic(self, event):
        self.deplacer_knob(event.x)

    def drag(self, event):
        self.deplacer_knob(event.x)

    def deplacer_knob(self, x):
        x = max(0, min(x, self.length))
        self.coords(self.knob, x - 10, 5)  # centrer curseur
        self.value = int((x / self.length) * 100)
        if self.command:
            self.command(self.value)

    def set(self, valeur):
        valeur = max(0, min(int(valeur), 100))
        x = (valeur / 100) * self.length
        self.coords(self.knob, x - 10, 5)
        self.value = valeur

    def set_command(self, func):
        self.command = func

    def set_callback(self, callback):
        self.callback = callback