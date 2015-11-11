class Observable:
    def __init__(self):
        self.__observers = []

    def register_observer(self, observer):
        self.__observers.append(observer)
		  
	 def unregister_observers(self):
        self.__observers.clear()
    
    def notify_observers(self, *args, **kwargs):
        for observer in self.__observers:
            observer.notify(self, *args, **kwargs)
