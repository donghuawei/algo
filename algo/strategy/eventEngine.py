# encoding: UTF-8

from queue import Queue, Empty
from threading import Thread


class EventEngine:
    """
    Event Drive Engine

    Variables:
    __queue: private, event queue
    __active: private, event switch
    __thread: private, event handle thread
    __timer: private, timer
    __handlers: private, event handle function collection
    
    
    Methods:
    __run: private method, main method to event working thread
    __process: private method, listener method used to response the corresponding event
    start: public method, start event engine
    stop: public method, stop event engine
    register: public method, register the event listner function for any specific event
    unregister: public method, unregister the event listner function for any specific event
    put: public method, put event into the event queue

    """

    # ----------------------------------------------------------------------
    def __init__(self):

        self.__queue = Queue()
        self.__active = False
        self.__thread = Thread(target=self.__run)
        self.__handlers = {}

    # ----------------------------------------------------------------------
    def __run(self):
        while self.__active == True:
            try:
                event = self.__queue.get(block=True, timeout=1)
                self.__process(event)
            except Empty:
                pass

    # ----------------------------------------------------------------------
    def __process(self, event):
        if event.type_ in self.__handlers:
            [handler(event) for handler in self.__handlers[event.type_]]
            # for handler in self.__handlers[event.type_]:
            # handler(event)

    # ----------------------------------------------------------------------
    def start(self):
        self.__active = True
        self.__thread.start()

    # ----------------------------------------------------------------------
    def stop(self):
        self.__active = False
        self.__thread.join()

    # ----------------------------------------------------------------------
    def register(self, type_, handler):
        try:
            handler_list_ = self.__handlers[type_]
        except KeyError:
            handler_list_ = []
            self.__handlers[type_] = handler_list_

        if handler not in handler_list_:
            handler_list_.append(handler)

    # ----------------------------------------------------------------------
    def unregister(self, type_, handler):

        try:
            handler_list_ = self.__handlers[type_]
            if handler in handler_list_:
                handler_list_.remove(handler)
            if not handler_list_:
                del self.__handlers[type_]
        except KeyError:
            pass

    # ----------------------------------------------------------------------
    def put(self, event):
        self.__queue.put(event)


########################################################################
class Event:
    def __init__(self, type_=None, even_param_=None):
        """Constructor"""
        self.type_ = type_
        self.even_param_ = even_param_
