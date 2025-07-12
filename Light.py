import pygame
from GameObject import GameObject
from pygame.math import Vector3 as Vec3

class Light(GameObject):
    def __init__(self, position: Vec3 | list[float] | tuple[float, float, float], dir: Vec3 | list[float] | tuple[float, float, float], color: pygame.Color | tuple[int, int, int]) -> None:
        position = Vec3(position)
        self.dir: Vec3 = Vec3(dir)
        self.color: pygame.Color = pygame.Color(color)
        super().__init__([], [], 'Light', (position))
    
    def Render(self, surface: pygame.Surface, light: GameObject) -> None:
        pass