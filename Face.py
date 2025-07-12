import pygame
import warnings
from pygame.math import Vector3 as Vec3

class Face():
    def __init__(self, vertexIndices: list[int], color: pygame.Color | tuple[int, int, int]) -> None:
        self.color: pygame.Color = pygame.Color(color)
        self.vertexIndices: list[int] = vertexIndices
        self.normal = None
        self.texture = None
        self.texCoords = None
        self.center: None | Vec3 = None
        self.direction: None | int = None
    
    def addNormal(self, normal: Vec3) -> None:
        self.normal = normal

    def addTexture(self, texture, texCoords: list[pygame.math.Vector2]):
        warnings.warn('Textures Not Yet Implemented')
    
    def calculateCenter(self, vertices: list[Vec3]) -> Vec3:
        self.center = Vec3(*[sum([vertices[i][j] for i in self.vertexIndices])/len(self.vertexIndices) for j in range(3)])
        return self.center

    def calculateDirection(self, vertices: list[Vec3]) -> int:
        p1 = vertices[self.vertexIndices[0]]
        p2 = vertices[self.vertexIndices[1]]
        p3 = vertices[self.vertexIndices[2]]
        z = (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)
        self.direction = int(1.1*z/abs(z+.01))
        return self.direction