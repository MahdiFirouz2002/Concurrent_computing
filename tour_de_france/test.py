import multiprocessing

def modify_dict(shared_dict):
    shared_dict["key"] = "value from child process"

if __name__ == "__main__":
    manager = multiprocessing.Manager()
    shared_dict = manager.dict()

    shared_dict["key"] = "value from main process"

    print("Initial value in shared_dict:", shared_dict["key"])

    p = multiprocessing.Process(target=modify_dict, args=(shared_dict,))
    p.start()
    p.join()

    print("Modified value in shared_dict:", shared_dict["key"])
