import pygame
from RenderScene import RenderScene
from GameObject import GameObject

class Renderer():
    def __init__(self) -> None:
        self.scenes: list[RenderScene] = []
        self.sceneNames: list[str] = []
        self.currScene: RenderScene

    def addScene(self, name: str) -> None:
        self.scenes.append(RenderScene(name))
        self.sceneNames.append(name)

    def getScene(self, sceneName: str) -> RenderScene:
        return self.scenes[self.sceneNames.index(sceneName)]

    def getCurrentScene(self):
        return self.currScene
    
    def setScene(self, sceneName: str) -> None:
        self.currScene = self.getScene(sceneName)
    
    def Render(self, surface: pygame.Surface, dt: float) -> None:
        self.currScene.Render(surface, dt)