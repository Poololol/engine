import pygame
import warnings
import random
from Face import Face

class OBJ:
    def __init__(self, vertices: list[pygame.math.Vector3], faces: list[Face], texCoords: list[tuple[float, float]], normals: list[pygame.math.Vector3]) -> None:
        self.vertices: list[pygame.math.Vector3] = vertices
        self.faces: list[Face] = faces
        self.texCoords: list[tuple[float, float]] = texCoords
        self.normals: list[pygame.math.Vector3] = normals

def parseObj(filename: str) -> OBJ:
    with open(filename, 'r') as obj:
        lines: list[str] = obj.readlines()
       
    vertices: list[pygame.math.Vector3] = []
    facesInfo: list[tuple[list[int], list[int], list[int]]] = []
    texCoords: list[tuple[float, float]] = []
    normals: list[pygame.math.Vector3] = []
    for line in lines:
        if line.startswith('v '):
            coords = line.split(' ')[1:]
            try:
                scale: float = float(coords[3])
            except IndexError:
                scale: float = 1.0
            vertices.append(pygame.math.Vector3(float(coords[0])/scale, float(coords[1])/scale, float(coords[2])/scale))
        elif line.startswith('f '):
            info = line.split(' ')[1:]
            if info[-1] == '\n':
                info = info[:-1]
            #print(line, info)
            vs = [int(v.split('/')[0])-1 for v in info]
            if len(info[0].split('/')) == 2:
                vt = [int(v.split('/')[1])-1 for v in info]
                vn = [-1] * len(info)
            elif len(info[0].split('/')) == 3:
                vt = [int(v.split('/')[1])-1 for v in info]
                vn = [int(v.split('/')[2])-1 for v in info]
            else:
                vt = [-1] * len(info)
                vn = [-1] * len(info)
            facesInfo.append((vs, vt, vn))
        elif line.startswith('vt'):
            info = line.split(' ')[1:]
            if len(info) == 1:
                texCoords.append((float(info[0]), 0.))
            elif len(info) == 2:
                texCoords.append((float(info[0]), float(info[1])))
            elif len(info) == 3:
                warnings.warn('3D Textures Not Supported')
                texCoords.append((float(info[0]), float(info[1])))
        elif line.startswith('vn'):
            coords = line.split(' ')[1:]
            normals.append(pygame.math.Vector3(float(coords[0]), float(coords[1]), float(coords[2])).normalize())
    
    faces: list[Face] = []
    for faceInfo in facesInfo:
        color = pygame.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        #color = (255, 255, 255)
        face = Face([vertices[faceInfo[0][i]].copy() for i in range(len(faceInfo[0]))], color)
        if faceInfo[1][0] >= 0 and len(texCoords) > 0:
            face.addTexture(0, [pygame.math.Vector2(texCoords[i]) for i in faceInfo[1]])
        if faceInfo[2][0] >= 0 and len(normals) > 0:
            #print(faceInfo[2], len(normals))
            #face.addNormal(pygame.math.Vector3(*[sum([normals[i][j] for i in faceInfo[2]])/len(faceInfo[2]) for j in range(3)]))
            pass
        #face.calculateCenter(vertices)
        faces.append(face)
    #print(vertices, faces, texCoords, normals)
    #print(lines)
    obj = OBJ(vertices, faces, texCoords, normals)
    return obj

parseObj(r"C:\Users\braed\Downloads\Super Fyyran-Trug\tinker.obj")