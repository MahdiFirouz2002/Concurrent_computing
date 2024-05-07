import tkinter as tk
from PIL import Image, ImageTk
import random

class Bicycle:
    def __init__(self, canvas, vertical_margin, country, pathPoints, status):
        self.canvas = canvas
        self.status = status
        self.vertical_margin = vertical_margin
        self.delay = random.randint(1, 50)
        self.pathPoints = pathPoints
        self.country = country
        self.img = Image.open("tour_de_france/bikes/" + country + "_bike.png")
        self.img = self.img.resize((50, 50)) 
        self.img = ImageTk.PhotoImage(self.img) 
        self.image_obj = self.canvas.create_image(pathPoints[0][0][0], pathPoints[0][0][1] + vertical_margin, image=self.img, anchor=tk.NW)
    
    def setPathPoints(self, pathPoints):
        self.pathPoints = pathPoints

    def animate_image(self):
        for round, stage in enumerate(self.pathPoints):
            for i in range(len(stage) - 1):
                x1, y1 = stage[i]
                x2, y2 = stage[i + 1]
                dx, dy = x2 - x1, y2 - y1
                distance = (dx ** 2 + dy ** 2) ** 0.5
                steps = int(distance)
                for _ in range(steps):
                    self.canvas.move(self.image_obj, dx / steps, dy / steps)
                    self.canvas.update()
                    self.canvas.after(self.delay)
                self.status[self.country] = round