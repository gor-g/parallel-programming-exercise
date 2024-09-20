from time import sleep
from Exemple import Process

def launch(nbProcess, runningTime=5):
    processes = []

    for i in range(nbProcess):
        processes.append(Process(f"P{i}", nbProcess))

    sleep(runningTime)

    for p in processes:
        p.stop()


if __name__ == '__main__':
    launch(nbProcess=5, runningTime=10)
