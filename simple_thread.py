#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
import Queue
import threading


"""
Global Interpreter Lock (GIL) ensures only one thread get
executed at a time, less exploitation of multi-core computation
power
"""


def example_task(keyword):
    time.sleep(2)
    current_thread = threading.current_thread()
    print("current thread identifier {0}".format(current_thread.ident))
    print("thread argument {0}".format(keyword))


class Pool:
    """A simple thread pool manager

    Attributes:
        task_queue: A queue holds all tasks waiting to be executed
        thread_pool: A threading.Thread array of length num_of_threads
    """

    def __init__(self, num_of_threads):
        """Initialize Pool class

        Args:
            num_of_threads: Number of threads in the pool
        """
        self.task_queue = Queue.Queue()
        self.thread_pool = [threading.Thread(target=self.worker)
                            for i in range(num_of_threads)]
        for thread in self.thread_pool:
            thread.start()

    def add_task(self, task):
        """Enqueue a task to the task queue

        Args:
            task: A callable function to be excuted
        """
        self.task_queue.put(task)

    def worker(self):
        """Worker method executed by threading.Thread

        Fetch new task from the task queue, execute obtained task, and
        wait when tasks are not available
        """
        while True:
            new_task = self.task_queue.get()
            new_task['func'](**new_task['args'])
            self.task_queue.task_done()

    def join(self):
        """Wait all tasks to be executed

        """
        self.task_queue.join()


if __name__ == "__main__":
    pool = Pool(10)
    print("start 10 tasks")
    for x in range(5):
        # time.sleep(1)
        print('task has been added')
        pool.add_task({'func': example_task, 'args': {'keyword': 'hello'}})
    pool.join()
