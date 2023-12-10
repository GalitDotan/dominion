from abc import abstractmethod


class Screen:
    @abstractmethod
    def __repr__(self):
        pass

    def display(self):
        print(self)
