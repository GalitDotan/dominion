from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def activate(self, *args, **kwargs):
        pass
