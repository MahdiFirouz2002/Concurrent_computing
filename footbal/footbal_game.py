from mpi4py import MPI
import random

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

goalkeeper = size - 1

def play_game():
    if rank == 0:
        current_player = random.randint(0, size - 1)
        comm.send(None, dest=current_player, tag=0)
        print(f"Game starts with player {current_player}")
    while True:
        comm.recv(source=MPI.ANY_SOURCE, tag=0)
        if rank == goalkeeper:
            print(f"Player {rank} (goalkeeper) received the ball. Game over.")
            for i in range(size):
                if i != rank:
                    comm.send("Game Over", dest=i, tag=1)
            break
        else:
            next_player = rank
            while next_player == rank:
                next_player = random.randint(0, size - 1)
            print(f"Player {rank} passes the ball to player {next_player}")
            comm.send(None, dest=next_player, tag=0)
            flag = comm.iprobe(source=MPI.ANY_SOURCE, tag=1)
            if flag:
                comm.recv(source=MPI.ANY_SOURCE, tag=1)
                break

if __name__ == "__main__":
    play_game()
