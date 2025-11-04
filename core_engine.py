import os
import hashlib
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from typing import Set, Callable

DEFAULT_SIGNATURES: Set[str] = {
    "44d88612fea8a8f36de82e1278abb02f",  # sample EICAR-like hash
    "5d41402abc4b2a76b9719d911017c592",
}

MAX_THREADS = 10

def calculate_hash(file_path: str, algorithm: str = "md5") -> str:
    try:
        hasher = hashlib.new(algorithm)
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    except Exception:
        return ""

def is_infected(hash_value: str, signatures: Set[str]) -> bool:
    return hash_value in signatures

def scan_file(file_path: str, signatures: Set[str]) -> bool:
    md5 = calculate_hash(file_path, "md5")
    return md5 and is_infected(md5, signatures)

def scan_directory(directory: str, signatures: Set[str], progress_callback: Callable[[int, int], None]):
    files = []
    for root, _, fs in os.walk(directory):
        for f in fs:
            files.append(os.path.join(root, f))

    total = len(files)
    infected = []
    scanned = 0
    lock = threading.Lock()

    def worker(file_queue: queue.Queue):
        nonlocal scanned
        while True:
            try:
                fp = file_queue.get_nowait()
            except queue.Empty:
                break
            if scan_file(fp, signatures):
                infected.append(fp)
            with lock:
                scanned += 1
                progress_callback(scanned, total)
            file_queue.task_done()

    q = queue.Queue()
    for f in files:
        q.put(f)

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as ex:
        for _ in range(MAX_THREADS):
            ex.submit(worker, q)
    q.join()
    return infected
