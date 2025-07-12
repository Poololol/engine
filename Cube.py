import pygame
from pygame.math import Vector3 as Vec3
from GameObject import GameObject
from Face import Face

class Cube(GameObject):
    def __init__(self, sideLength: float, position: Vec3 | list[float] | tuple[float, float, float], name: str) -> None:
        position = Vec3(position)
        self.sideLength: float = sideLength
        self.up: Vec3 = Vec3(0, 1, 0)
        self.right: Vec3 = Vec3(1, 0, 0)
        self.back: Vec3 = Vec3(0, 0, 1)
        colors: list[pygame.Color | tuple[int, int, int]] = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        vertices = [position + (-self.sideLength/2, -self.sideLength/2, -self.sideLength/2), 
                    position + (-self.sideLength/2, -self.sideLength/2, self.sideLength/2), 
                    position + (-self.sideLength/2, self.sideLength/2, -self.sideLength/2), 
                    position + (self.sideLength/2, -self.sideLength/2, -self.sideLength/2), 
                    position + (-self.sideLength/2, self.sideLength/2, self.sideLength/2), 
                    position + (self.sideLength/2, -self.sideLength/2, self.sideLength/2), 
                    position + (self.sideLength/2, self.sideLength/2, -self.sideLength/2), 
                    position + (self.sideLength/2, self.sideLength/2, self.sideLength/2)]
        faces = [Face.fromIndices([0,1,5,3], colors[0], vertices), Face.fromIndices([0,1,4,2], colors[1], vertices), Face.fromIndices([0,2,6,3], colors[2], vertices), Face.fromIndices([1,4,7,5], colors[3], vertices), Face.fromIndices([2,4,7,6], colors[4], vertices), Face.fromIndices([3,5,7,6], colors[5], vertices)]
        super().__init__(faces, name, position)
        #print(vertices)

    