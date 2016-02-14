from threading import Thread

def async(original_func):
    def wrapper(*args, **kwargs):
        thr = Thread(target=original_func, args=args, kwargs=kwargs)
        thr.start()
    return wrapper
