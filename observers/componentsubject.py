class ComponentSubject:
    def __init__(self):
        self.observers = []

    def register_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, child):
        for observer in self.observers:
            observer.update(child)