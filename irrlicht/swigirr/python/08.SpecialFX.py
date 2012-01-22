import sys
import irr

MEDIA_PATH="../../../irrlicht/media"

if __name__=="__main__":

    #i=raw_input("Please press 'y' if you want to use realtime shadows.\n");
    i='y'

    shadows = (i == 'y');

    device = irr.createDevice(irr.video.EDT_OPENGL, 
            irr.core.dimension2du(640, 480), 16, False, shadows);

    if not device:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    mesh = smgr.getMesh(MEDIA_PATH+"/room.3ds");

    smgr.getMeshManipulator().makePlanarTextureMapping(mesh.getMesh(0), 0.004);

    node = smgr.addAnimatedMeshSceneNode(mesh);
    node.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/wall.jpg"));
    node.getMaterial(0).SpecularColor.set(0,0,0,0);

    mesh = smgr.addHillPlaneMesh( "myHill",
            irr.core.dimension2df(20,20),
            irr.core.dimension2du(40,40), None, 0,
            irr.core.dimension2df(0,0),
            irr.core.dimension2df(10,10));

    node = smgr.addWaterSurfaceSceneNode(mesh.getMesh(0), 3.0, 300.0, 30.0);
    node.setPosition(irr.core.vector3df(0,7,0));

    node.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/stones.jpg"));
    node.setMaterialTexture(1, driver.getTexture(MEDIA_PATH+"/water.jpg"));

    node.setMaterialType(irr.video.EMT_REFLECTION_2_LAYER);

    node = smgr.addLightSceneNode(None, irr.core.vector3df(0,0,0),
            irr.video.SColorf(1.0, 0.6, 0.7, 1.0), 800.0);
    anim = smgr.createFlyCircleAnimator (irr.core.vector3df(0,150,0),250.0);
    node.addAnimator(anim);

    node = smgr.addBillboardSceneNode(node, irr.core.dimension2df(50, 50));
    node.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    node.setMaterialType(irr.video.EMT_TRANSPARENT_ADD_COLOR);
    node.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/particlewhite.bmp"));

    ps = smgr.addParticleSystemSceneNode(False);

    em = ps.createBoxEmitter(
            irr.core.aabbox3df(-7,0,-7,7,1,7),
            irr.core.vector3df(0.0,0.06,0.0),
            80,100,
            irr.video.SColor(0,255,255,255),
            irr.video.SColor(0,255,255,255),
            800,2000,0,
            irr.core.dimension2df(10.0,10.0),
            irr.core.dimension2df(20.0,20.0));

    ps.setEmitter(em)

    paf = ps.createFadeOutParticleAffector();

    ps.addAffector(paf);

    ps.setPosition(irr.core.vector3df(-70,60,40));
    ps.setScale(irr.core.vector3df(2,2,2));
    ps.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    ps.setMaterialFlag(irr.video.EMF_ZWRITE_ENABLE, False);
    ps.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/fire.bmp"));
    ps.setMaterialType(irr.video.EMT_TRANSPARENT_VERTEX_ALPHA);

    n = smgr.addVolumeLightSceneNode(None, -1,
            32,
            32,
            irr.video.SColor(0, 255, 255, 255),
            irr.video.SColor(0, 0, 0, 0));

    if n:
        n.setScale(irr.core.vector3df(56.0, 56.0, 56.0));
        n.setPosition(irr.core.vector3df(-120,50,40));
        textures=[driver.getTexture("%s/portal%d.bmp" % (MEDIA_PATH, g))
                for g in range(7, 0, -1)]
        glow = smgr.createTextureAnimator(textures, 150);
        n.addAnimator(glow);

    mesh = smgr.getMesh(MEDIA_PATH+"/dwarf.x");

    anode = smgr.addAnimatedMeshSceneNode(mesh);
    anode.setPosition(irr.core.vector3df(-50,20,-60));
    anode.setAnimationSpeed(15);

    anode.addShadowVolumeSceneNode();
    smgr.setShadowColor(irr.video.SColor(150,0,0,0));

    anode.setScale(irr.core.vector3df(2,2,2));
    anode.setMaterialFlag(irr.video.EMF_NORMALIZE_NORMALS, True);

    camera = smgr.addCameraSceneNodeFPS();
    camera.setPosition(irr.core.vector3df(-50,50,-150));

    device.getCursorControl().setVisible(False);

    lastFPS = -1;
    while device.run():
        if device.isWindowActive():
            driver.beginScene(True, True);
            smgr.drawAll();
            driver.endScene();
            fps = driver.getFPS();

            if lastFPS != fps:
                device.setWindowCaption(u"Irrlicht Engine - SpecialFX example [%s] FPS: %d" % (
                    driver.getName(), fps));
                lastFPS = fps;

