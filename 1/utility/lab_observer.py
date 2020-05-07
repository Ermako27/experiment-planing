from abc import abstractmethod, ABCMeta


class LabObserver(metaclass=ABCMeta):
    @abstractmethod
    def model_is_changed(self):
        pass
