import pygame
import utils
from pygame.math import Vector3 as Vec3
from GameObject import GameObject
from Renderer import Renderer
from math import pi, cos
from Cube import Cube
from Face import Face

screenSize = (500, 500)
screen = pygame.display.set_mode(screenSize, pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 20)

rend = Renderer()
rend.addScene('Tedst')
#rend.getScene('Tedst').addObject(Cube(100, (-50, -50, 1)))
rend.getScene('Tedst').addObject(Cube(200, (0, 0, 400), 'Test Cube 2'))
rend.getScene('Tedst').getObject('Test Cube 2').rotate((0, pi/4, 0))
rend.getScene('Tedst').getObject('Test Cube 2').rotate((0, 0, pi/4))
rend.setScene('Tedst')

rend.addScene('OBJ')
rend.setScene('OBJ')
rend.getScene('OBJ').addObjectFromObj(r"C:\Users\braed\OneDrive\Documents\beveledCube.obj", 'beveledCube')
rend.getScene('OBJ').addObjectFromObj(r"C:\Users\braed\OneDrive\Documents\beveledCube-3.obj", 'beveledCube2')
rend.getScene('OBJ').addObjectFromObj(r"C:\Users\braed\OneDrive\Documents\beveledCube-10.obj", 'beveledCube3')
rend.getScene('OBJ').addObjectFromObj(r"C:\Users\braed\OneDrive\Documents\beveledCube-20.obj", 'beveledCube4')
rend.getScene('OBJ').addObjectFromObj(r"C:\Users\braed\OneDrive\Documents\sphere-5.obj", 'sphere')
rend.getScene('OBJ').getObject('beveledCube').translate(Vec3(0, 2, 5))
rend.getScene('OBJ').getObject('beveledCube2').translate(Vec3(0, -2, 5))
rend.getScene('OBJ').getObject('beveledCube3').translate(Vec3(2, 0, 5))
rend.getScene('OBJ').getObject('beveledCube4').translate(Vec3(-2, 0, 5))
rend.getScene('OBJ').getObject('sphere').translate(Vec3(0, 0, 5))

rend.addScene('Sphere')
rend.setScene('Sphere')
rend.getScene('Sphere').addObjectFromObj(r"C:\Users\braed\OneDrive\Documents\sphere.obj", 'sphere')
rend.getScene('Sphere').getObject('sphere').translate(Vec3(0, 0, 3))
r'''rend.getScene('Sphere').addObjectFromObj(r"C:\Users\braed\OneDrive\Documents\sphere.obj", 'sphere2')
rend.getScene('Sphere').getObject('sphere2').translate(Vec3(0, 0, 1))
rend.getScene('Sphere').getObject('sphere2').scale(1/10)'''

'''face = rend.getScene('Sphere').getObject('sphere').faces[500]
face.color = (255,0,0)
o = (GameObject([Vec3(0, 0, 0), face.normal/1, face.normal/1 + Vec3(1,1,1)/100], [Face([0, 1, 2], (255,255,255))], 'Normal-1', Vec3(0,0,0)))
print(face.center)
print(rend.getScene('Sphere').getObject('sphere').position)
o.translate(face.center)
rend.getScene('Sphere').addObject(o)'''

rend.addScene('Teacup')
#rend.setScene('Teacup')
rend.getScene('Teacup').addObjectFromObj(r"C:\Users\braed\Downloads\newell_teaset\newell_teaset\teacup.obj")
rend.getScene('Teacup').getObject('teacup').translate(Vec3(0,1.5,2))
rend.getScene('Teacup').getObject('teacup').rotate((0,0,pi))
rend.getScene('Teacup').addObjectFromObj(r"C:\Users\braed\Downloads\newell_teaset\newell_teaset\spoon.obj")
rend.getScene('Teacup').getObject('spoon').translate(Vec3(0,0,1))
rend.getScene('Teacup').getObject('spoon').rotate((0, pi/2, 0))

if __name__ == '__main__':
    run = True
    frame = 0
    print(1/60)
    while run:
        screenSize = screen.get_size()
        dt = clock.get_time()/1000

        pygame.draw.rect(screen, 0, ((0, 0), screenSize))

        rend.Render(screen, dt)
        #rend.getScene('Tedst').getObject('Test Cube 2').rotateWorld((1 * dt, 0.0, 0.0))
        #rend.getScene('OBJ').getObject('beveledCube').rotate((1 * dt, 0.0, 0.0))
        #rend.getScene('OBJ').getObject('beveledCube2').rotate((-1 * dt, 0.0, 0.0))
        #rend.getScene('OBJ').getObject('beveledCube3').rotate((0.0, 1 * dt, 0.0))
        #rend.getScene('OBJ').getObject('beveledCube4').rotate((0.0, -1 * dt, 0.0))
        #rend.getScene('OBJ').getObject('sphere').translate(Vec3(0, cos(frame/10) * dt, 0))
        #rend.getScene('OBJ').getObject('sphere').rotate((1 * dt, 2 * dt, -1 * dt))
        rend.getScene('Sphere').getObject('sphere').rotate((1 * dt, 0.0, 0.0))
        #rend.getScene('Teacup').getObject('spoon').rotate((0.0, 0.0, 1 * dt))
        #rend.getScene('Sphere').getObject('sphere').faces[int(frame/20)].color = (255,255,255)
        '''if frame >= 0:
            for i in range(len(rend.getCurrentScene().getObject('sphere').faces)):
                face = rend.getCurrentScene().getObject('sphere').faces[i]
                o = (GameObject([Vec3(0, 0, 0), face.normal/10, face.normal/10 + Vec3(1,1,1)/1000], [Face([0, 1, 2], (255,255,255))], f'Normal-{i}', Vec3(0,0,0), dt))
                o.translate(face.center)
                rend.currScene.addObject(o)'''

        #print(rend.getCurrentScene().name)
        #quit()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                key = event.dict['key']
                if key == pygame.K_F2:
                    utils.TakeScreenshot(screen)

        pygame.display.set_caption(f'FPS: {round(clock.get_fps(), 2)}, Faces: {len(rend.currScene.allObjects.faces)}, Frame: {frame}')
        pygame.display.update()
        clock.tick(6)
        frame += 1
        #quit()