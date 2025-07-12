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
        faces = [Face([0,1,5,3], colors[0]), Face([0,1,4,2], colors[1]), Face([0,2,6,3], colors[2]), Face([1,4,7,5], colors[3]), Face([2,4,7,6], colors[4]), Face([3,5,7,6], colors[5])]
        super().__init__(vertices, faces, name, position)
        print(vertices)

    def rotate(self, angles: tuple[float, float, float]) -> None:
        for i in range(len(self.vertices)):
            vertex = self.vertices[i] - self.position
            vertex.rotate_rad_ip(angles[0], self.up)
            vertex.rotate_rad_ip(angles[1], self.right)
            vertex.rotate_rad_ip(angles[2], self.back)
            self.vertices[i] = vertex + self.position
        self.up.rotate_rad_ip(angles[1], self.right)
        self.up.rotate_rad_ip(angles[2], self.back)
        self.right.rotate_rad_ip(angles[0], self.up)
        self.right.rotate_rad_ip(angles[2], self.back)
        self.back.rotate_rad_ip(angles[0], self.up)
        self.back.rotate_rad_ip(angles[1], self.right)
        self.up.normalize_ip()
        self.right.normalize_ip()
        self.back.normalize_ip()
        print(self.up, self.right, self.back)
    def rotateWorld(self, angles: tuple[float, float, float]) -> None:
        for i in range(len(self.vertices)):
            vertex = self.vertices[i] - self.position
            vertex.rotate_rad_ip(angles[0], (0, 1, 0))
            vertex.rotate_rad_ip(angles[1], (1, 0, 0))
            vertex.rotate_rad_ip(angles[2], (0, 0, 1))
            self.vertices[i] = vertex + self.position
        self.up.rotate_rad_ip(angles[1], self.right)
        self.up.rotate_rad_ip(angles[2], self.back)
        self.right.rotate_rad_ip(angles[0], self.up)
        self.right.rotate_rad_ip(angles[2], self.back)
        self.back.rotate_rad_ip(angles[0], self.up)
        self.back.rotate_rad_ip(angles[1], self.right)