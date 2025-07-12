import pygame
import time

from pygame.math import Vector3 as Vec3
from GameObject import GameObject
from Light import Light
from Face import Face

class RenderScene():
    def __init__(self, name: str) -> None:
        self.objects: list[GameObject] = []
        self.objectNames: list[str] = []
        self.name: str = name
        self.addObject(Light((0, 0, 0), (0, 0, 1), (255, 255, 255)))

    def addObject(self, gameObject: GameObject) -> None:
        self.objects.append(gameObject)
        self.objectNames.append(self.objects[-1].name)
        #self.calculateObjects()
    
    def addObjectFromObj(self, filename: str, name: str | None = None) -> None:
        self.objects.append(GameObject.fromOBJ(filename, name))
        self.objectNames.append(self.objects[-1].name)
        #self.calculateObjects()

    def getObject(self, name: str) -> GameObject:
        for gameObject in self.objects:
            if gameObject.name == name:
                return gameObject
        raise NameError()
    
    def calculateObjects(self):
        #t1 = time.time()
        allVerts = []
        allFaces = []
        #print(self.objectNames)
        for gameObject in self.objects:
            for face in gameObject.faces:
                vertInds = face.vertexIndices.copy()
                for i in range(len(vertInds)):
                    vertInds[i] += len(allVerts)
                newFace = Face(vertInds, face.color)
                newFace.center = face.center
                if face.normal is not None:
                    newFace.addNormal(face.normal)
                allFaces.append(newFace)
            #print(len(gameObject.vertices), len(allVerts), sum([len(gobj.vertices) for gobj in self.objects]))
            for vert in gameObject.vertices:
                allVerts.append(vert)
        self.allObjects = GameObject(allVerts, allFaces, 'all-Objects', Vec3(0,0,0))
        #print(f'calculateObjects: {round(time.time()-t1, 3)}')

    def delObject(self, objName: str) -> None:
        index = self.objectNames.index(objName)
        self.objects.pop(index)
        self.objectNames.pop(index)

    def Render(self, surface: pygame.Surface, dt: float) -> None:
        #t1r = time.time()
        self.calculateObjects()
        #self.allObjects = self.objects[1]
        self.allObjects.Render(surface, self.getObject('Light'))
        toBeRemoved = []
        for obj in self.objects:
            if obj.expiration > 0:
                obj.expiration -= dt
            if obj.expiration < 0:
                toBeRemoved.append(obj.name)
        for name in toBeRemoved:
            self.delObject(name)
        #print(f'Render: {round(time.time()-t1r, 3)}\n\n')