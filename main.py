import sys
import os

from time import time
from threading import Thread
from queue import Queue
from record import recognize_important, record_audio
#from important import most_important


# Create n empty .wav files named 'temp0.wav', 'temp1.wav', etc.
def create_temp(n):
    for i in range(n):
        open(f'temp{i}.wav', 'w').close()


# Remove temporary .wav files
def delete_temp(n):
    for i in range(n):
        tempfile = f'temp{i}.wav'
        if os.path.exists(tempfile):
            os.remove(tempfile)


# Worker function for spawned thread
def worker(q, lang):
    while True:
        filename = q.get()
        if filename == 'HALT':
            break
        print(recognize_important(filename, lang))
        q.task_done()


# Time elapsed since start of program execution
def elapsed_time(start):
    return int(time() - start)


# Main function
def main(lang, minutes):
    print('0s\tProgram start')
    start = time()

    q = Queue()
    thread = Thread(target=worker, args=(q, lang))

    # Version-safe initialization of daemon thread
    try:
        thread.setDaemon(True)
    except:
        thread.daemon = True

    thread.start()
    create_temp(minutes)

    try:
        for i in range(minutes):
            # Elapsed time
            t = elapsed_time(start)
            print(f'{t}s\tRecording minute {i}')

            # Record audio and put in queue
            filename = f'temp{i}.wav'
            record_audio(filename, 60)
            q.put(filename)
    except Exception as e:
        print(e)
        thread.join()

    t = elapsed_time(start)
    print(f'{t}s\tRecording complete.')
    q.put('HALT')
    thread.join()

    t = elapsed_time(start)
    print(f'{t}s\tProgram complete.')
    delete_temp(minutes)


# Sample usage:
# python main.py 'English' 5
# python main.py 'German' 5
if __name__ == '__main__':
    assert len(sys.argv) == 3
    assert sys.argv[1] == 'English' or sys.argv[1] == 'German'
    main(sys.argv[1], int(sys.argv[2]))

