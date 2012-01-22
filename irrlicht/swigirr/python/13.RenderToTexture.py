import os
import sys
import irr

MEDIA_PATH=os.path.join(
        os.path.dirname(__file__),
        "../../../irrlicht/media"
        )

if __name__=="__main__":
    device = irr.createDevice(irr.video.EDT_OPENGL, irr.core.dimension2du(640, 480),
            16, False, False);

    if not device:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();
    env = device.getGUIEnvironment();

    fairy = smgr.addAnimatedMeshSceneNode(
            smgr.getMesh(MEDIA_PATH+"/faerie.md2"));

    if (fairy):
        fairy.setMaterialTexture(0,
                driver.getTexture(MEDIA_PATH+"/faerie2.bmp"));
        fairy.setMaterialFlag(irr.video.EMF_LIGHTING, True);
        fairy.getMaterial(0).Shininess = 20.0;
        fairy.setPosition(irr.core.vector3df(-10,0,-100));
        fairy.setMD2Animation ( irr.scene.EMAT_STAND );

    smgr.addLightSceneNode(None, irr.core.vector3df(-15,5,-105),
            irr.video.SColorf(1.0, 1.0, 1.0));

    smgr.setAmbientLight(irr.video.SColor(0,60,60,60));

    fpsCamera = smgr.addCameraSceneNodeFPS();
    fpsCamera.setPosition(irr.core.vector3df(-50,50,-150));

    device.getCursorControl().setVisible(False);

    test = smgr.addCubeSceneNode(60);

    anim = smgr.createRotationAnimator(
            irr.core.vector3df(0.3, 0.3 ,0));

    test.setPosition(irr.core.vector3df(-100,0,-100));
    test.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    test.addAnimator(anim);

    device.setWindowCaption(u"Irrlicht Engine - Render to Texture and Specular Highlights example");

    rt = None;
    fixedCam = None;

    if (driver.queryFeature(irr.video.EVDF_RENDER_TO_TARGET)):
        rt = driver.addRenderTargetTexture(irr.core.dimension2dui(256,256), "RTT1");
        test.setMaterialTexture(0, rt);
        fixedCam = smgr.addCameraSceneNode(None, irr.core.vector3df(10,10,-80),
                irr.core.vector3df(-10,10,-100));
    else:
        skin = env.getSkin();
        font = env.getFont(MEDIA_PATH+"/fonthaettenschweiler.bmp");
        if (font):
            skin.setFont(font);

        text = env.addStaticText(
                u"Your hardware or this renderer is not able to use the "
                u"render to texture feature. RTT Disabled.",
                irr.core.recti(150,20,470,60));

        text.setOverrideColor(irr.video.SColor(100,255,255,255));

    lastFPS = -1;
    while(device.run()):
        if (device.isWindowActive()):
            driver.beginScene(True, True);

            if (rt):
                driver.setRenderTarget(rt, True, True, irr.video.SColor(0,0,0,255));

                test.setVisible(False);
                smgr.setActiveCamera(fixedCam);

                smgr.drawAll();

                driver.setRenderTarget(0, True, True);

                test.setVisible(True);
                smgr.setActiveCamera(fpsCamera);

            smgr.drawAll();
            env.drawAll();

            driver.endScene();

            fps = driver.getFPS();
            if (lastFPS != fps):
                device.setWindowCaption(
                        u"Irrlicht Engine - Render to Texture and Specular Highlights example FPS: %d" % fps
                        )
                lastFPS = fps;

