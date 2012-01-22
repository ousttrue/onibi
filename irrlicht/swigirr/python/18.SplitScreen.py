import os
import sys
import irr


MEDIA_PATH=os.path.join(
        os.path.dirname(__file__),
        "../../../irrlicht/media")
ResX=800;
ResY=600;
fullScreen=False;
SplitScreen=True;

camera=[None, None, None, None];

class MyEventReceiver(irr.IEventReceiver):
    def __init__(self):
        irr.IEventReceiver.__init__(self)

    def OnEvent(self, event):
        global SplitScreen
        if (event.EventType == irr.EET_KEY_INPUT_EVENT 
                and event.Info.KeyInput.Key == irr.KEY_KEY_S 
                and event.Info.KeyInput.PressedDown):
            SplitScreen = not SplitScreen;
            return True;

        #if (camera[3]):
        #    return camera[3].OnEvent(event);

        return False;


if __name__=="__main__":
    receiver=MyEventReceiver();

    device = irr.createDevice(irr.video.EDT_OPENGL,
            irr.core.dimension2du(ResX,ResY), 32, fullScreen,
            False, False, receiver);
    if not device:
        sys.exit(1)

    smgr = device.getSceneManager();
    driver = device.getVideoDriver();

    model = smgr.getMesh(MEDIA_PATH+"/sydney.md2");
    if not model:
        sys.exit(1);
    model_node = smgr.addAnimatedMeshSceneNode(model);
    if (model_node):
        texture = driver.getTexture(MEDIA_PATH+"/sydney.bmp");
        model_node.setMaterialTexture(0,texture);
        model_node.setMD2Animation(irr.scene.EMAT_RUN);
        model_node.setMaterialFlag(irr.video.EMF_LIGHTING,False);

    device.getFileSystem().addZipFileArchive(MEDIA_PATH+"/map-20kdm2.pk3");
    map = smgr.getMesh("20kdm2.bsp");
    if (map):
        map_node = smgr.addOctreeSceneNode(map.getMesh(0));
        map_node.setPosition(irr.core.vector3df(-850,-220,-850));

    camera[0] = smgr.addCameraSceneNode(None, 
            irr.core.vector3df(50,0,0), irr.core.vector3df(0,0,0));
    camera[1] = smgr.addCameraSceneNode(None, 
            irr.core.vector3df(0,50,0), irr.core.vector3df(0,0,0));
    camera[2] = smgr.addCameraSceneNode(None, 
            irr.core.vector3df(0,0,50), irr.core.vector3df(0,0,0));
    camera[3] = smgr.addCameraSceneNodeFPS();

    if (camera[3]):
        camera[3].setPosition(irr.core.vector3df(-50,0,-50));

    device.getCursorControl().setVisible(False);
    lastFPS = -1;

    while(device.run()):
        driver.setViewPort(irr.core.recti(0,0,ResX,ResY));
        driver.beginScene(True,True,irr.video.SColor(255,100,100,100));
        if (SplitScreen):
            smgr.setActiveCamera(camera[0]);
            driver.setViewPort(irr.core.recti(0,0,ResX/2,ResY/2));
            smgr.drawAll();
            smgr.setActiveCamera(camera[1]);
            driver.setViewPort(irr.core.recti(ResX/2,0,ResX,ResY/2));
            smgr.drawAll();
            smgr.setActiveCamera(camera[2]);
            driver.setViewPort(irr.core.recti(0,ResY/2,ResX/2,ResY));
            smgr.drawAll();
            driver.setViewPort(irr.core.recti(ResX/2,ResY/2,ResX,ResY));

        smgr.setActiveCamera(camera[3]);
        smgr.drawAll();
        driver.endScene();

        if (driver.getFPS() != lastFPS):
            lastFPS = driver.getFPS();
            device.setWindowCaption(u"Irrlicht SplitScreen-Example (FPS: %d)" % lastFPS);

