import pygame
import warnings
from pygame.math import Vector3 as Vec3

class Face():
    def __init__(self, vertices: list[Vec3], color: pygame.Color | tuple[int, int, int]) -> None:
        self.color: pygame.Color = pygame.Color(color)
        self.vertices: list[Vec3] = vertices
        self.normal = self.calculateNormal()
        self.texture = None
        self.texCoords = None
        self.center: Vec3 = self.calculateCenter()
        self.direction: int = self.calculateDirection()
    
    def calculateNormal(self) -> Vec3:
        self.normal = (self.vertices[1]-self.vertices[0]).cross(self.vertices[2]-self.vertices[0]).normalize()
        return self.normal

    def addTexture(self, texture, texCoords: list[pygame.math.Vector2]):
        warnings.warn('Textures Not Yet Implemented')
    
    def calculateCenter(self) -> Vec3:
        self.center = Vec3(*[sum([self.vertices[i][j] for i in range(len(self.vertices))])/len(self.vertices) for j in range(3)])
        return self.center

    def calculateDirection(self) -> int:
        p1 = self.vertices[0]
        p2 = self.vertices[1]
        p3 = self.vertices[2]
        z = (p2.x - p1.x)*(p3.y - p1.y) - (p2.y - p1.y)*(p3.x - p1.x)
        self.direction = int(1.1*z/abs(z+.01))
        return self.direction
    
    @staticmethod
    def fromIndices(indices: list[int], color: pygame.Color | tuple[int, int, int], vertices: list[Vec3]) -> 'Face':
        return Face([vertices[i] for i in indices], color)
    
    def __str__(self) -> str:
        return f'Vertices: {self.vertices}, Normal: {self.normal}, Center: {self.center}'
    def __repr__(self) -> str:
        return str(self)