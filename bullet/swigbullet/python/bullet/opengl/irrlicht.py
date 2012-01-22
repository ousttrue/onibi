import sys
import irr
import bullet
import bullet.opengl.gldebugdrawer
from . import demoapplication


class DemoApplication(demoapplication.DemoApplication):

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

    device = irr.createDevice(irr.video.EDT_OPENGL,
            irr.core.dimension2du(width, height), 16, False);
    device.setWindowCaption(title);

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    smgr.addCameraSceneNode(None, irr.core.vector3df(0,-40,0), irr.core.vector3df(0,0,0));

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


    if not device:
        sys.exit(1);


    myNode = CSampleSceneNode(smgr.getRootSceneNode(), smgr, 666);

    anim = smgr.createRotationAnimator(irr.core.vector3df(0.8, 0, 0.8));
    if anim:
        myNode.addAnimator(anim);

    frames=0;
    while device.run():
        driver.beginScene(True, True, irr.video.SColor(0,100,100,100));

        smgr.drawAll();

        driver.endScene();
        frames+=1
        if frames==100:
            msg = u"Irrlicht Engine [%s] FPS: %d" % (
                    driver.getName(),
                    driver.getFPS())
            device.setWindowCaption(msg);
            frames=0;

    sys.exit(0);

