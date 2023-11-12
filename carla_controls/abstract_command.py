from abc import ABC, abstractmethod

class CMD(ABC):
    @abstractmethod
    def execute(self):
        """Action to take as command"""
