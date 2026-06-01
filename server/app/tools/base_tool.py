from abc import ABC, abstractmethod


class BaseTool(ABC):

    name = ""
    description = ""

    @abstractmethod
    def run(self, **kwargs):
        pass