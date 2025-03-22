from .camera import Camera

class Shape:
    def draw(self, camera: Camera):
        raise NotImplementedError("Shape is an abstract class")

    def translate(self, x: int, y: int):
        raise NotImplementedError("Shape is an abstract class")
