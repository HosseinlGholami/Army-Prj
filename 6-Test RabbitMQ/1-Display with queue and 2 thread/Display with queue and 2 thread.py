import concurrent.futures
import logging
import queue
import threading
import time
import cv2 as cv


def producer(queue, event,cap):
    """Pretend we're getting a number from the network."""
    while not event.is_set():
        ret, message = cap.read()
        if not ret:
            logging.info("Can't receive frame (stream end?). Exiting ...")
            break
        else:
            logging.info("Producer got message: %s", message)
            queue.put(message)
    cap.release()
    logging.info("Producer received event. Exiting")

def consumer(queue, event):
    """Pretend we're saving a number in the database."""
    while not event.is_set() or not queue.empty():
        message = queue.get()
        cv.imshow("mamad",message)
        cv.waitKey(1)
        logging.info(
            "queue size:%d", queue.qsize()
        )
    cv.destroyWindow('mamad')
    logging.info("Consumer received event. Exiting")

if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")
    cap = cv.VideoCapture(0)
    pipeline = queue.Queue(maxsize=10)
    event = threading.Event()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        executor.submit(producer, pipeline, event,cap)
        executor.submit(consumer, pipeline, event)

        time.sleep(10)
        logging.info("Main: about to set event")
        event.set()