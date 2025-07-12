import pygame
import objParser
import time

from pygame.math import Vector3 as Vec3
from math import tan, radians
from Face import Face

class GameObject():
    def __init__(self, faces: list[Face], name: str, position: Vec3 = Vec3(0, 0, 0), expiration: float = 0) -> None:
        #self.vertices: list[pygame.math.Vector3] = vertices
        self.faces: list[Face] = []
        for face in faces:
            for vertex in face.vertices:
                vertex += position
            face.center += position
            self.faces.append(face)
        #print(self.faces, '\n\n\n')
        self.name: str = name
        self.up: Vec3 = Vec3(0, 1, 0)
        self.right: Vec3 = Vec3(1, 0, 0)
        self.back: Vec3 = Vec3(0, 0, 1)
        self.position: Vec3 = position
        self.expiration: float = expiration

    def Render(self, surface: pygame.Surface, light: 'GameObject') -> None:
        #print(len(self.vertices), max(self.faces, key=lambda face: max(face.vertexIndices)).vertexIndices)
        #t2 = time.time()
        self.faces.sort(key=lambda face: max([vert.z for vert in face.vertices]), reverse=True)
        
        lightIntensity = []
        for face in self.faces:
            lightDir = (face.center - light.position).normalize()
            lightIntensity.append((-min(0, lightDir.dot(face.normal))+1)/2)
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
            pygame.draw.polygon(surface, [*[int(self.faces[i].color[j] * lightIntensity[i]) for j in range(3)]], [(vert.xy * pixPerWorldUnit / vert.z) + center for vert in self.faces[i].vertices], width=0)
        #print(f'Render {self.name}: {round(time.time()-t3, 3)}')

    def rotatePoint(self, angles: tuple[float, float, float], point: Vec3) -> None:
        #print(point)
        for face in self.faces:
            for i in range(len(face.vertices)):
                vertex = face.vertices[i] - point
                vertex.rotate_rad_ip(angles[0], self.up)
                vertex.rotate_rad_ip(angles[1], self.right)
                vertex.rotate_rad_ip(angles[2], self.back)
                face.vertices[i] = vertex + point
            normal: Vec3 = face.normal.copy()
            normal.rotate_rad_ip(angles[0], self.up)
            normal.rotate_rad_ip(angles[1], self.right)
            normal.rotate_rad_ip(angles[2], self.back)
            face.normal = normal.normalize()
            center: Vec3 = face.center - point
            center.rotate_rad_ip(angles[0], self.up)
            center.rotate_rad_ip(angles[1], self.right)
            center.rotate_rad_ip(angles[2], self.back)
            face.center = center + point
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
        for face in self.faces:
            for vertex in face.vertices:
                vertex += translation/4
            face.center += translation

    def scale(self, scaleFactor: float) -> None:
        for face in self.faces:
            for vertex in face.vertices:
                vertex -= self.position
                vertex *= scaleFactor
                vertex += self.position

    @staticmethod
    def fromOBJ(filename: str, name: str | None = None) -> 'GameObject':
        obj = objParser.parseObj(filename)
        if name is None:
            name = filename.split('\\')[-1].split('.')[0]
        go =  GameObject(obj.faces, name, Vec3(0, 0, 0))
        return go