#!/usr/bin/env python

import sys
import irr

MEDIA_PATH="../../../irrlicht/media"

if __name__=="__main__":

    print irr.core.dimension2du(640, 480)
    device = irr.createDevice( 
            irr.video.EDT_SOFTWARE, irr.core.dimension2du(640, 480), 16,
            False, False, False, None);

    if not device:
        sys.exit(1)

    device.setWindowCaption(u"Hello World! - Irrlicht Engine Demo");

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    guienv = device.getGUIEnvironment();
    guienv.addStaticText(
            u"Hello World! This is the Irrlicht Software renderer!",
            irr.core.recti(10, 10, 260, 40),
            True
            );

    mesh = smgr.getMesh(MEDIA_PATH+"/sydney.md2");
    if not mesh:
        sys.exit(1)

    node = smgr.addAnimatedMeshSceneNode( mesh );
    if not node:
        sys.exit(1)

    if node:
        node.setMaterialFlag(irr.video.EMF_LIGHTING, False);
        node.setMD2Animation(irr.scene.EMAT_STAND);
        node.setMaterialTexture( 0, driver.getTexture(MEDIA_PATH+"/sydney.bmp"));

    smgr.addCameraSceneNode(None, irr.core.vector3df(0,30,-40), irr.core.vector3df(0,5,0));

    while device.run():
        driver.beginScene(True, True, irr.video.SColor(255,100,101,140));
        smgr.drawAll();
        guienv.drawAll();
        driver.endScene();

