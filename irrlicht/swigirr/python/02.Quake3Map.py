import sys
import irr

MEDIA_PATH='../../../irrlicht/media'

if __name__=="__main__":

   
    i=raw_input("Please select the driver you want for this example:\n"
            " (a) OpenGL 1.5\n (b) Direct3D 9.0c\n (c) Direct3D 8.1\n"
            " (d) Burning's Software Renderer\n (e) Software Renderer\n"
            " (f) NullDevice\n (otherKey) exit\n\n")
    driverMap={
        'a': irr.video.EDT_OPENGL,
        'b': irr.video.EDT_DIRECT3D9,
        'c': irr.video.EDT_DIRECT3D8,
        'd': irr.video.EDT_BURNINGSVIDEO,
        'e': irr.video.EDT_SOFTWARE,
        'f': irr.video.EDT_NULL,
         }
    driverType=driverMap[i]
    device = irr.createDevice(driverType, irr.core.dimension2du(640, 480));

    if not device:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    device.getFileSystem().addZipFileArchive(MEDIA_PATH+"/map-20kdm2.pk3");

    mesh = smgr.getMesh("20kdm2.bsp");
    if mesh:
        node = smgr.addOctreeSceneNode(mesh.getMesh(0), None, -1, 1024);

    if node:
        node.setPosition(irr.core.vector3df(-1300,-144,-1249));

    smgr.addCameraSceneNodeFPS();

    device.getCursorControl().setVisible(False);

    lastFPS = -1;
    while device.run():

        if device.isWindowActive():

            driver.beginScene(True, True, irr.video.SColor(255,200,200,200));
            smgr.drawAll();
            driver.endScene();

            fps = driver.getFPS();

            if lastFPS != fps:
                msg = u"Irrlicht Engine - Quake 3 Map example [%s] FPS: %d" % (
                        driver.getName(), fps)

                device.setWindowCaption(msg);
                lastFPS = fps;
        else:
            # python keyword renamed
            device._yield();

    sys.exit(0)

