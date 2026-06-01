from abc import ABC, abstractmethod


class BaseTool(ABC):

    name = ""
    description = ""
    parameters = {}

    @abstractmethod
    def run(self, **kwargs):
        pass