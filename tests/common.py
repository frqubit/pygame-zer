import numpy as np
import pygame
import os

dirname, filename = os.path.split(os.path.abspath(__file__))

def surface_equals_snapshot(surface: pygame.Surface, name: str) -> bool:
    filename = f"{dirname}/snapshots/{name}.png"
    if os.path.exists(filename):
        snapshot = pygame.image.load(filename)

        surf0 = np.array(pygame.surfarray.array3d(snapshot))
        surf1 = np.array(pygame.surfarray.array3d(surface))

        return (surf0 == surf1).all()
    else:
        pygame.image.save(surface, filename)
        return True
