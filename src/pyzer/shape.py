from .camera import Camera
from abc import abstractmethod

class Shape:
    @abstractmethod
    def draw(self, camera: Camera):
        raise NotImplementedError("Shape is an abstract class")

    @abstractmethod
    def translate(self, x: float, y: float):
        raise NotImplementedError("Shape is an abstract class")
