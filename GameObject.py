import pygame
import objParser
import time

from pygame.math import Vector3 as Vec3
from math import tan, radians
from Face import Face

class GameObject():
    def __init__(self, vertices: list[Vec3], faces: list[Face], name: str, position: Vec3 = Vec3(0, 0, 0), expiration: float = 0) -> None:
        self.vertices: list[pygame.math.Vector3] = vertices
        self.faces: list[Face] = []
        for face in faces:
            face.calculateDirection(self.vertices)
            self.faces.append(face)
        self.origColors: list[pygame.Color | tuple[int, int, int]] = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        self.name: str = name
        self.up: Vec3 = Vec3(0, 1, 0)
        self.right: Vec3 = Vec3(1, 0, 0)
        self.back: Vec3 = Vec3(0, 0, 1)
        self.position: Vec3 = position
        self.expiration: float = expiration

    def Render(self, surface: pygame.Surface, light: 'GameObject') -> None:
        #print(len(self.vertices), max(self.faces, key=lambda face: max(face.vertexIndices)).vertexIndices)
        #t2 = time.time()
        self.faces.sort(key=lambda face: max([self.vertices[vert].z for vert in face.vertexIndices]), reverse=True)
        
        lightIntensity = []
        for face in self.faces:
            if face.normal is not None:
                lightDir = (face.center - light.position).normalize() # type: ignore
                lightIntensity.append((-min(0, lightDir.dot(face.normal))+1)/2) # type: ignore
            else:
                lightIntensity.append(1)
        #t3 = time.time()
        #print(f'Light Calc: {round(t3-t2, 3)}')
        center = (surface.width/2, surface.height/2)
        fov = 60
        pixPerWorldUnit = surface.height / (tan(radians(fov/2))*2)
        offset = 0
        for i in range(len(self.faces)):
            i -= offset
            #print([(self.vertices[vert].xy / self.vertices[vert].z) + (surface.width/2, surface.height/2) for vert in self.faces[i]])
            #print(*[int(self.faces[i].color[j] * lightIntensity[i]) for j in range(3)])
            #print(lightIntensity[i])
            pygame.draw.polygon(surface, [*[int(self.faces[i].color[j] * lightIntensity[i]) for j in range(3)]], [(self.vertices[vert].xy * pixPerWorldUnit / self.vertices[vert].z) + center for vert in self.faces[i].vertexIndices], width=0)
        #print(f'Render {self.name}: {round(time.time()-t3, 3)}')

    def rotatePoint(self, angles: tuple[float, float, float], point: Vec3) -> None:
        for i in range(len(self.vertices)):
            vertex = self.vertices[i] - point
            vertex.rotate_rad_ip(angles[0], self.up)
            vertex.rotate_rad_ip(angles[1], self.right)
            vertex.rotate_rad_ip(angles[2], self.back)
            self.vertices[i] = vertex + point
        for i in range(len(self.faces)):
            if self.faces[i].normal is not None:
                normal: Vec3 = self.faces[i].normal.copy() # type: ignore
                normal.rotate_rad_ip(angles[0], self.up)
                normal.rotate_rad_ip(angles[1], self.right)
                normal.rotate_rad_ip(angles[2], self.back)
                self.faces[i].normal = normal.normalize()
            if self.faces[i].center is not None:
                center: Vec3 = self.faces[i].center - point # type: ignore
                center.rotate_rad_ip(angles[0], self.up)
                center.rotate_rad_ip(angles[1], self.right)
                center.rotate_rad_ip(angles[2], self.back)
                self.faces[i].center = center + point
        self.up.rotate_rad_ip(angles[1], self.right)
        self.up.rotate_rad_ip(angles[2], self.back)
        self.right.rotate_rad_ip(angles[0], self.up)
        self.right.rotate_rad_ip(angles[2], self.back)
        self.back.rotate_rad_ip(angles[0], self.up)
        self.back.rotate_rad_ip(angles[1], self.right)
        self.up.normalize_ip()
        self.right.normalize_ip()
        self.back.normalize_ip()
        #print(self.up, self.right, self.back)
    
    def rotateWorld(self, angles: tuple[float, float, float]) -> None:
        self.rotatePoint(angles, Vec3(0, 0, 0))
    
    def rotate(self, angles: tuple[float, float, float]) -> None:
        self.rotatePoint(angles, self.position)

    def translate(self, translation: Vec3) -> None:
        self.position += translation
        for vertex in self.vertices:
            vertex += translation
        for face in self.faces:
            if face.center:
                face.center += translation

    def scale(self, scaleFactor: float) -> None:
        for vertex in self.vertices:
            vertex -= self.position
            vertex *= scaleFactor
            vertex += self.position

    @staticmethod
    def fromOBJ(filename: str, name: str | None = None) -> 'GameObject':
        obj = objParser.parseObj(filename)
        if name is None:
            name = filename.split('\\')[-1].split('.')[0]
        go =  GameObject(obj.vertices, obj.faces, name, Vec3(0, 0, 0))
        return go