#!/usr/bin/python3

import queue
import threading
import sys
import socket
import time

THREADS_LIMIT = 1


class Worker(threading.Thread):
    daemon = True

    def run(self) -> None:
        while True:
            try:
                domain = q.get(False)
                socket.gethostbyname(domain)

                try:
                    socket.gethostbyname("wegwegweg" + domain)
                except socket.gaierror:
                    valid.add(domain)

            except queue.Empty:
                break
            except socket.gaierror:
                invalid.add(domain)
            except BaseException as e:
                print("Exception: {0} => {1}".format(e, domain))



valid = set()
invalid = set()

q = queue.Queue()

for line in open(sys.argv[1]):
    line = line.strip()
    if not len(line):
        continue
    q.put(line)

start_q_size = q.qsize()
pool = []
for _ in range(THREADS_LIMIT):
    w = Worker()
    w.start()
    pool.append(w)

print("Start working with {0} targets".format(start_q_size))
is_alive = True
while is_alive:
    is_alive = False

    for w in pool:
        if w.is_alive():
            is_alive = True
            break

    time.sleep(10)
    print("Done {0} from {1}, working.".format(start_q_size - q.qsize(), start_q_size))

with open("domains-valid.txt", "w") as fh:
    fh.write("\n".join(valid))
with open("domains-invalid.txt", "w") as fh:
    fh.write("\n".join(invalid))

print("Done. Check domains-valid.txt / domains-invalid.txt")