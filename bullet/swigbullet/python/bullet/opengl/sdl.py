import sys
import pygame
from pygame.locals import *
import bullet
import bullet.opengl.gldebugdrawer
from . import glapplication


class DemoApplication(glapplication.GLApplication):

    def specialKeyboard(self, key, x, y):
        pass

    def swapBuffers(self):
        pass

    def	updateModifierKeys(self):
        pass


def main(argv, width, height, title, demoApp):
    demoApp.initPhysics();
    #debugDrawer=bullet.opengl.gldebugdrawer.GLDebugDrawer()
    #demoApp.getDynamicsWorld().setDebugDrawer(debugDrawer);

    pygame.init()
    size=(width, height)
    screen = pygame.display.set_mode(size, 
            HWSURFACE | OPENGL | DOUBLEBUF)

    demoApp.reshape(width, height)

    #clock = pygame.time.Clock()    
    is_running=True
    while is_running:
        # event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                is_running=False
            if event.type == KEYUP and event.key == K_ESCAPE:
                is_running=False
        # keyboard
        pressed = pygame.key.get_pressed()
            
        #time_passed = clock.tick()
        
        # Show the screen
        demoApp.moveAndDisplay()
        pygame.display.flip()

    pygame.quit()

