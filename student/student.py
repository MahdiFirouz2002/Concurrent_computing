import multiprocessing
import random
import time

def student_process(student_id, delay_range):
    receive_delay = random.randint(*delay_range)
    time.sleep(receive_delay)
    start_time = time.time()

    answer_time = 90 * 60  # 90 minutes in seconds

    return_delay = random.randint(*delay_range)
    time.sleep(return_delay)
    end_time = time.time()

    total_time = end_time - start_time
    print(f"Student {student_id}: Total time for answering: {total_time:.2f} seconds")

    return total_time

if __name__ == "__main__":
    num_students = 16
    delay_range = (2, 5)  # Delay range for receiving and returning the exam paper

    processes = []
    for student_id in range(num_students):
        p = multiprocessing.Process(target=student_process, args=(student_id + 1, delay_range))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    total_time = sum([p.exitcode for p in processes])
    average_time_per_student = total_time / num_students
    print(f"\nAverage time per student: {average_time_per_student:.2f} seconds")
