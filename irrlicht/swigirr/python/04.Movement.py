#!/usr/bin/env python
import irr


MEDIA_PATH='../../../irrlicht/media'


class MyEventReceiver(irr.IEventReceiver):

    def __init__(self):
        irr.IEventReceiver.__init__(self)
        self.KeyIsDown=[False 
                for _ in range(255)]
                #for _ in range(irr.KEY_KEY_CODES_COUNT)]

    def OnEvent(self, event):
        if event.EventType == irr.EET_KEY_INPUT_EVENT:
            self.KeyIsDown[irr.getKeyAsInt(event.Info.KeyInput)] = event.Info.KeyInput.PressedDown;
        return False;

    def IsKeyDown(self, keyCode):
        return self.KeyIsDown[irr.keyToInt(keyCode)];


if __name__=="__main__":
    receiver=MyEventReceiver();
    print(receiver)

    device = irr.createDevice(irr.video.EDT_OPENGL,
            irr.core.dimension2dui(640, 480), 16, False, False, False, receiver);

    if device == 0:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    node = smgr.addSphereSceneNode();
    if node:
        node.setPosition(irr.core.vector3df(0,0,30));
        node.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/wall.bmp"));
        node.setMaterialFlag(irr.video.EMF_LIGHTING, False);

    n = smgr.addCubeSceneNode();
    if n:
        n.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/t351sml.jpg"));
        n.setMaterialFlag(irr.video.EMF_LIGHTING, False);
        anim = smgr.createFlyCircleAnimator(irr.core.vector3df(0,0,30), 20.0);
        if anim:
            n.addAnimator(anim);
            #anim.drop();

    anms = smgr.addAnimatedMeshSceneNode(smgr.getMesh(MEDIA_PATH+"/ninja.b3d"));
    if anms:
        anim = smgr.createFlyStraightAnimator(irr.core.vector3df(100,0,60),
                irr.core.vector3df(-100,0,60), 3500, True);
        if anim:
            anms.addAnimator(anim);
            #anim.drop();

        anms.setMaterialFlag(irr.video.EMF_LIGHTING, False);

        anms.setFrameLoop(0, 13);
        anms.setAnimationSpeed(15);

        anms.setScale(irr.core.vector3df(2.0,2.0,2.0));
        anms.setRotation(irr.core.vector3df(0,-90,0));


    smgr.addCameraSceneNodeFPS();
    device.getCursorControl().setVisible(False);

    device.getGUIEnvironment().addImage(
            driver.getTexture(MEDIA_PATH+"/irrlichtlogoalpha2.tga"),
            irr.core.position2di(10,20));

    diagnostics = device.getGUIEnvironment().addStaticText(
            u"", irr.core.recti(10, 10, 400, 20));
    diagnostics.setOverrideColor(irr.video.SColor(255, 255, 255, 0));

    lastFPS = -1;

    then = device.getTimer().getTime();

    MOVEMENT_SPEED = 5.0;

    while device.run():
        now = device.getTimer().getTime();
        frameDeltaTime = (now - then) / 1000.0
        then = now;

        nodePosition = node.getPosition();

        if receiver.IsKeyDown(irr.KEY_KEY_W):
            nodePosition.Y += MOVEMENT_SPEED * frameDeltaTime;
        elif receiver.IsKeyDown(irr.KEY_KEY_S):
            nodePosition.Y -= MOVEMENT_SPEED * frameDeltaTime;

        if receiver.IsKeyDown(irr.KEY_KEY_A):
            nodePosition.X -= MOVEMENT_SPEED * frameDeltaTime;
        elif receiver.IsKeyDown(irr.KEY_KEY_D):
            nodePosition.X = nodePosition.X + MOVEMENT_SPEED * frameDeltaTime;
        node.setPosition(nodePosition);

        driver.beginScene(True, True, irr.video.SColor(255,113,113,133));

        smgr.drawAll();
        device.getGUIEnvironment().drawAll();

        driver.endScene();

        fps = driver.getFPS();

        if lastFPS != fps:
            tmp=u"Movement Example - Irrlicht Engine [%s] fps: %d" % (
                    driver.getName(), fps)

            device.setWindowCaption(tmp);
            lastFPS = fps;

    sys.exit(0);

