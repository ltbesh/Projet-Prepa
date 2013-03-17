#    Copyright 2009 Google Inc.
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

"""Simple web application load testing script.

This is a simple web application load
testing skeleton script. Modify the code between !!!!!
to make the requests you want load tested.
"""

import httplib2
import random
import socket
import time
from threading import Event
from threading import Thread
from threading import current_thread
from urllib import urlencode

# Modify these values to control how the testing is done

# How many threads should be running at peak load.
NUM_THREADS = 10

# How many minutes the test should run with all threads active.
TIME_AT_PEAK_QPS = 10 # secondes

# How many seconds to wait between starting threads.
# Shouldn't be set below 30 seconds.
DELAY_BETWEEN_THREAD_START = 15 # seconds

quitevent = Event()
all_thread = Event()

count = 0

def threadproc():
    """This function is executed by each thread."""

    print "Thread started: %s" % current_thread().getName()
    h = httplib2.Http(timeout = 30)
    global count
    while not quitevent.is_set():
        if all_thread.is_set():
            count +=1
            try:
                # HTTP requests to exercise the server go here
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                resp, content = h.request(
                    "http://127.0.0.1:8080/increment")
                if resp.status != 200:
                    pass
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            except socket.timeout:
                pass
        else:
            try:
                # HTTP requests to exercise the server go here
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                resp, content = h.request(
                    "http://127.0.0.1:8080/")
                if resp.status != 200:
                    pass
                # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            except socket.timeout:
                pass

    print "Thread finished: %s" % current_thread().getName()

if __name__ == "__main__":
    runtime = (TIME_AT_PEAK_QPS + DELAY_BETWEEN_THREAD_START * NUM_THREADS)
    print "Total runtime will be: " + str(runtime) + " seconds" 
    threads = []
    try:
        for i in range(NUM_THREADS):
            t = Thread(target = threadproc)
            t.start()
            threads.append(t)
            time.sleep(DELAY_BETWEEN_THREAD_START)
        all_thread.set()
        print "All threads running"
        time.sleep(TIME_AT_PEAK_QPS)
        print "Completed full time at peak qps, shutting down threads"
    except:
        print "Exception raised, shutting down threads"

    quitevent.set()
    time.sleep(3)
    for t in threads:
        t.join(1.0)
    print "Finished"
    print count