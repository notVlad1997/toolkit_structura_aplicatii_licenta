from observers.observer import Observer


class Subject:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        if isinstance(observer, Observer):
            self.observers.append(observer)
        else:
            print("Observer is not a instance of " + str(Observer.__class__))

    def notify_observers(self, child):
        for observer in self.observers:
            observer.update(child)