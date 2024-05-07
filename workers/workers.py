import tkinter as tk
from PIL import Image, ImageTk
import time
import random
from threading import *         
import threading

lunch_semaphore = Semaphore(4)         
load_mutex = Lock()
unload_mutex = Lock()

totalCartoons = 0
current_time_min, current_time_sec = 0, 0
current_time_str = "-"
first_lunch_min, first_lunch_sec = 2, 0
second_lunch_min, second_lunch_sec = 3, 0
end_time = 5
workers_status = [0] * 8

class WarehouseApp:
    def __init__(self, master, margin_left, margin_top, worker_id):
        self.master = master
        self.master.title("Warehouse Simulation")
        self.total_cartoons = 0
        self.margin_top = margin_top
        self.margin_left = margin_left
        self.lunch = False
        self.worker_id = worker_id
        self.time = random.uniform(0.01, 0.1)

        self.warehouse_img = Image.open("workers/warehouse.jpg").resize((100, 100))
        self.lunch_img = Image.open("workers/lunch.png").resize((80, 80))
        self.worker_img = Image.open("workers/worker.png").resize((50, 50))
        self.sheep_img = Image.open("workers/sheep.png").resize((100, 100))
        self.carton_img = Image.open("workers/carton.png").resize((20, 20))

        self.warehouse_tk = ImageTk.PhotoImage(self.warehouse_img)
        self.worker_tk = ImageTk.PhotoImage(self.worker_img)
        self.sheep_tk = ImageTk.PhotoImage(self.sheep_img)
        self.carton_tk = ImageTk.PhotoImage(self.carton_img)
        self.lunch_tk = ImageTk.PhotoImage(self.lunch_img)

        self.warehouse_label = tk.Label(master, image=self.warehouse_tk)
        self.worker_label = tk.Label(master, image=self.worker_tk)
        self.sheep_label = tk.Label(master, image=self.sheep_tk)
        self.carton_label = tk.Label(master, image=self.carton_tk)
        self.lunch_label = tk.Label(master, image=self.lunch_tk)

        self.total_cartoons_label = tk.Label(master, text="Cartoons: 0 | Last unload: -", font=("Arial", 10), bg="white")

        self.canvas_vertical = tk.Canvas(master, width=1, height=150, bg="black")
        self.canvas_vertical.place(x=self.margin_left + 680, y=self.margin_top)

        self.canvas = tk.Canvas(master, width=680, height=1, bg="black")
        self.canvas.place(x=self.margin_left, y=130 + self.margin_top, width=685)

        self.warehouse_label.place(x=350 + self.margin_left, y=0 + self.margin_top)
        self.worker_label.place(x=100 + self.margin_left, y=25 + self.margin_top)
        self.sheep_label.place(x=0 + self.margin_left, y=0 + self.margin_top)
        self.carton_label.place(x=115 + self.margin_left, y=77 + self.margin_top)
        self.total_cartoons_label.place(x=300 + self.margin_left, y=110 + self.margin_top)
        self.lunch_label.place(x=600 + self.margin_left, y=10 + self.margin_top)

        load_mutex.acquire()
        self.worker_thread = threading.Thread(target=self.work)
        self.worker_thread.start()

    def work(self):
        global totalCartoons, current_time_str, workers_status, end_time
        load_mutex.release()

        for x in range(100 + self.margin_left, 290 + self.margin_left, 1):
            self.worker_label.place(x=x, y=25 + self.margin_top)
            self.carton_label.place(x=x + 15, y=77 + self.margin_top)
            self.master.update()
            time.sleep(self.time)

        with unload_mutex:
            workers_status[self.worker_id] = 0
            self.carton_label.place(x=-100, y=-100)
            self.total_cartoons += 3
            totalCartoons += 3
            self.total_cartoons_label.config(text=f"Cartoons: {self.total_cartoons} | Last unload: {current_time_str}")

        if (first_lunch_min <= current_time_min <= first_lunch_min + 1) and (first_lunch_sec <= current_time_sec <= first_lunch_sec + 30) \
        or (second_lunch_min <= current_time_min <= second_lunch_min + 1) and (second_lunch_sec <= current_time_sec <= second_lunch_sec + 30):
            if not self.lunch and lunch_semaphore._value > 0:
                lunch_semaphore.acquire()
                self.lunch = True
                workers_status[self.worker_id] = 1
                self.take_lunch()
                time.sleep(30)
                lunch_semaphore.release()

        for x in range(295 + self.margin_left, 100 + self.margin_left , -1):
            self.worker_label.place(x=x, y=25 + self.margin_top)
            self.master.update()
            time.sleep(self.time)

        if current_time_min < end_time:
            load_mutex.acquire()
            self.work()
        else:
            # Terminate gracefully if termination condition is met
            return


    def take_lunch(self):
        self.carton_label.place(x=-100, y=-100)
        self.worker_label.place(x=550 + self.margin_left, y=25 + self.margin_top)
        self.master.update()

class InfoPanel:
    def __init__(self, master):
        global end_time
        self.master = master
        self.timer_label = tk.Label(master, text="Timer: 00:00", font=("Arial", 20), bg="white")
        self.timer_label.place(x=930, y=450)
        self.total_cartoons_label = tk.Label(master, text="Total Cartoons: 0", font=("Arial", 16), bg="white")
        self.total_cartoons_label.place(x=930, y=490)
        self.lunch_time = tk.Label(master, text="First lunch Time: 02:00 - 02:30        Second lunch Time: 03:00 - 03:30", font=("Arial", 16), bg="white")
        self.lunch_time.place(x=700, y=520)
        self.end_time = tk.Label(master, text=f"End time: 0{end_time}:00", font=("Arial", 16), bg="white")
        self.end_time.place(x=930, y=550)
        self.start_time = time.time()
        self.update_timer()

    def update_timer(self):
        global totalCartoons, current_time_str, current_time_min, current_time_sec, end_time
        if current_time_min != end_time:
            current_time = time.time()
            elapsed_time = current_time - self.start_time
            minutes = int((elapsed_time % 3600) // 60)
            seconds = int(elapsed_time % 60)
            milliseconds = int((elapsed_time % 1) * 1000)
            timer_str = f"Timer: {minutes:02d}:{seconds:02d}"
            current_time_str = f"{minutes:02d}:{seconds:02d}:{milliseconds:03d}"
            current_time_min, current_time_sec = minutes, seconds
            self.timer_label.config(text=timer_str)
            self.total_cartoons_label.config(text=f'Total Cartoons: {totalCartoons}')
            self.master.after(5, self.update_timer)

def main():
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='white')
    worker1 = WarehouseApp(root, margin_left=0, margin_top=0, worker_id=0)
    worker2 = WarehouseApp(root, margin_left=0, margin_top=150, worker_id=1)
    worker3 = WarehouseApp(root, margin_left=0, margin_top=300, worker_id=2)
    worker4 = WarehouseApp(root, margin_left=0, margin_top=450, worker_id=3)
    worker5 = WarehouseApp(root, margin_left=0, margin_top=600, worker_id=4)
    worker6 = WarehouseApp(root, margin_left=685, margin_top=0, worker_id=5)
    worker7 = WarehouseApp(root, margin_left=685, margin_top=150, worker_id=6)
    worker8 = WarehouseApp(root, margin_left=685, margin_top=300, worker_id=7)
    info_panel = InfoPanel(root)

    root.mainloop()

if __name__ == "__main__":
    main()
