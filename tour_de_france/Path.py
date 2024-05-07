import random

class Path:
    def __init__(self, canvas, x0, y0, x1, y1, pathColor, number):
        self.canvas = canvas
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1
        self.pathColor = pathColor
        self.number = number
        self.path_points = []
        self.draw_random_path()

    def draw_random_path(self):
        x1, y1 = self.x0, self.y0 
        x2, y2 = self.x1, self.y1 
        reverse = False

        threshold = 10
        if x2 < x1:
            x1, x2 = x2, x1 
            y1, y2 = y2, y1
            reverse = True

        num_control_points = random.randint(2, 10) 
        control_points = [(random.randint(x1, x2), abs(random.randint(min(y1, y2) - threshold, max(y1, y2) + threshold))) for _ in range(num_control_points)]
        control_points.sort(key=lambda point: point[0])
        self.path_points = [(x1, y1)] + control_points + [(x2, y2)]
        if reverse:
            self.path_points.reverse()
        self.canvas.create_line(x1, y1, *control_points, x2, y2, smooth=True, width=2, fill=self.pathColor)
        self.draw_end_circle(self.number)


    def getPathPoints(self):
        return self.path_points
    
    def draw_end_circle(self, txt):
        last_point = self.path_points[-1]
        radius = 20  
        circle_color = 'red'

        self.canvas.create_oval(
            last_point[0] - radius, last_point[1] - radius,
            last_point[0] + radius, last_point[1] + radius,
            fill=circle_color
        )

        self.canvas.create_text(
            last_point[0], last_point[1],
            text=txt,
            font=('Helvetica', '16'),
            fill='black'
        )

    def draw_start_circle(self, txt):
        last_point = self.path_points[0]
        radius = 20  
        circle_color = 'red'

        self.canvas.create_oval(
            last_point[0] - radius, last_point[1] - radius,
            last_point[0] + radius, last_point[1] + radius,
            fill=circle_color
        )

        self.canvas.create_text(
            last_point[0], last_point[1],
            text=txt,
            font=('Helvetica', '10'),
            fill='black'
        )
