from abc import ABC, abstractmethod


class OnImageListener(ABC):

    @abstractmethod
    def on_detect(self, images):
        pass
