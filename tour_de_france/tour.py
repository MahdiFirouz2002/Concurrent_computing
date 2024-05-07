import multiprocessing
import tkinter as tk
from Path import *
from Bicycle import *
import time
from threading import *         
import threading

stages_path_points = []
status_copy = {"france": -1, "german": -1, "usa": -1}
timers = {"france": time.time(), "german": time.time(), "usa": time.time()}
mainCanvas = None

def main(status):
    global mainCanvas
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    root.configure(background='white')
    canvas = tk.Canvas(root)
    canvas.pack(fill='both', expand=True)
    mainCanvas = canvas
    initPathes(canvas)
    bike_france_thread, bike_german_thread, bike_usa_thread = initBicycles(canvas, status)
    root.mainloop()
    bike_france_thread.join()
    bike_german_thread.join()
    bike_usa_thread.join()

def handleTimer(country, status, roundTimes):
    global status_copy, timers
    while True:
        if status[country] != status_copy[country]:
            timeDiff = time.time() - timers[country]
            roundTimes[country].append(timeDiff)
            timers[country] = time.time()
            status_copy[country] = status[country]
            print(country + " round " + str(status[country]) + "  roundTime: " + str(roundTimes[country][-1]))
        time.sleep(0.5)

def resize_image(image_path, width, height):
    original_image = Image.open(image_path)
    resized_image = original_image.resize((width, height))
    return ImageTk.PhotoImage(resized_image)

def oracle(roundTimes):
    global mainCanvas
    time.sleep(1)
    while True:
        sumTimes = {"france": [], "german": [], "usa": []}
        for country in ["german", "france", "usa"]:
            if len(roundTimes[country]) > 0: 
                sumTimes[country] = [sum(roundTimes[country]), len(roundTimes[country])]
        sumTimes = dict(sorted(sumTimes.items(), key=lambda item: (item[1][0], -item[1][1])))
        i = 1
        print("##################################")
        for (key, value) in sumTimes.items():
            print(str(i) + "th place: " + key + "   total time: " + str(value[0]))
            i = i + 1
        print("##################################")

        images = {
            "france": resize_image("tour_de_france/flags/france.png", 70, 70),
            "german": resize_image("tour_de_france/flags/german.png", 70, 70),
            "usa": resize_image("tour_de_france/flags/usa.png", 70, 70)
        }

        y_pos = 200
        i = 1
        for country, _ in sumTimes.items():
            image = images[country]
            mainCanvas.create_image(650, y_pos, anchor=tk.NW, image=image)
            mainCanvas.create_text(730, y_pos + 25, anchor=tk.NW, text=f"{i}th", font=("Arial", 16))
            y_pos += 100
            i = i + 1

        mainCanvas.update()
        time.sleep(1)


def initPathes(canvas):
    # start stage1
    start_1_path = Path(canvas, 100, 100, 300, 100, "red", "1")
    start_1_path.draw_start_circle("Start")
    start_s1_path_points = start_1_path.getPathPoints()
    stages_path_points.append(start_s1_path_points)

    # stage1 stage2
    s1_s2_path = Path(canvas, start_s1_path_points[-1][0] + 10, start_s1_path_points[-1][1], 500, 100, "yellow", "2")
    s1_s2_path_points = s1_s2_path.getPathPoints()
    stages_path_points.append(s1_s2_path_points)

    # stage2 stage3
    s2_s3_path = Path(canvas, s1_s2_path_points[-1][0] + 10, s1_s2_path_points[-1][1], 700, 100, "blue", "3")
    s2_s3_path_points = s2_s3_path.getPathPoints()
    stages_path_points.append(s2_s3_path_points)

    # stage3 stage4
    s3_s4_path = Path(canvas, s2_s3_path_points[-1][0] + 10, s2_s3_path_points[-1][1], 900, 100, "green", "4")
    s3_s4_path_points = s3_s4_path.getPathPoints()
    stages_path_points.append(s3_s4_path_points)

    # stage4 stage5
    s4_s5_path = Path(canvas, s3_s4_path_points[-1][0] + 10, s3_s4_path_points[-1][1], 1100, 100, "orange", "5")
    s4_s5_path_points = s4_s5_path.getPathPoints()
    stages_path_points.append(s4_s5_path_points)

    # stage5 stage6
    s5_s6_path = Path(canvas, s4_s5_path_points[-1][0] + 10, s4_s5_path_points[-1][1], 1200, 300, "purple", "6")
    s5_s6_path_points = s5_s6_path.getPathPoints()
    stages_path_points.append(s5_s6_path_points)

    # stage6 stage7
    s6_s7_path = Path(canvas, s5_s6_path_points[-1][0], s5_s6_path_points[-1][1] + 10, 1310, 500, "black", "7")
    s6_s7_path_points = s6_s7_path.getPathPoints()
    stages_path_points.append(s6_s7_path_points)

    # stage7 stage8
    s7_s8_path = Path(canvas, s6_s7_path_points[-1][0], s6_s7_path_points[-1][1] + 10, 1100, 700, "gray", "8")
    s7_s8_path_points = s7_s8_path.getPathPoints()
    stages_path_points.append(s7_s8_path_points)

    # stage8 stage9
    s8_s9_path = Path(canvas, s7_s8_path_points[-1][0] - 10, s7_s8_path_points[-1][1], 900, 700, "blue", "9")
    s8_s9_path_points = s8_s9_path.getPathPoints()
    stages_path_points.append(s8_s9_path_points)

    # stage9 stage10
    s9_s10_path = Path(canvas, s8_s9_path_points[-1][0] - 10, s8_s9_path_points[-1][1], 700, 700, "red", "10")
    s9_s10_path_points = s9_s10_path.getPathPoints()
    stages_path_points.append(s9_s10_path_points)

    # stage10 stage11
    s10_s11_path = Path(canvas, s9_s10_path_points[-1][0] - 10, s9_s10_path_points[-1][1], 500, 700, "green", "11")
    s10_s11_path_points = s10_s11_path.getPathPoints()
    stages_path_points.append(s10_s11_path_points)

    # stage11 stage12
    s11_s12_path = Path(canvas, s10_s11_path_points[-1][0] - 10, s10_s11_path_points[-1][1], 300, 700, "orange", "12")
    s11_s12_path_points = s11_s12_path.getPathPoints()
    stages_path_points.append(s11_s12_path_points)

    # stage12 end
    s12_end_path = Path(canvas, s11_s12_path_points[-1][0] - 10, s11_s12_path_points[-1][1], 100, 700, "yellow", "End")
    s12_end_path_points = s12_end_path.getPathPoints()
    stages_path_points.append(s12_end_path_points)

def initBicycles(canvas, status):
    bike_france = Bicycle(canvas, -50, "france", stages_path_points, status)
    bike_german = Bicycle(canvas, -30, "german", stages_path_points, status)
    bike_usa = Bicycle(canvas, -10, "usa", stages_path_points, status)

    bike_france_thread = threading.Thread(name="bike_france_thread", target=bike_france.animate_image)
    bike_german_thread = threading.Thread(name="bike_german_thread", target=bike_german.animate_image)
    bike_usa_thread = threading.Thread(name="bike_usa_thread", target=bike_usa.animate_image)

    bike_france_thread.start()
    bike_german_thread.start()
    bike_usa_thread.start()

    return bike_france_thread, bike_german_thread, bike_usa_thread

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    status = manager.dict({"france": 0, "german": 0, "usa": 0})
    roundTimes = {country: manager.list() for country in ["france", "german", "usa"]}

    # create process to handle each country time
    german_process = multiprocessing.Process(name="german_process", target=handleTimer, args=("german", status, roundTimes,))
    france_process = multiprocessing.Process(name="france_process", target=handleTimer, args=("france", status, roundTimes,))
    usa_process = multiprocessing.Process(name="usa_process", target=handleTimer, args=("usa", status, roundTimes,))
    oracle_process = threading.Thread(name="oracle_process", target=oracle, args=(roundTimes,))
    german_process.start()
    france_process.start()
    usa_process.start()
    oracle_process.start()
    main(status)
    german_process.join()
    france_process.join()
    usa_process.join()
    oracle_process.join()
