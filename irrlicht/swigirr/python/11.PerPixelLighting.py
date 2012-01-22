import os
import sys
import irr


MEDIA_PATH=os.path.join(
        os.path.dirname(__file__),
        "../../../irrlicht/media"
        )


class MyEventReceiver(irr.IEventReceiver):

    def __init__(self, room, env, driver):
        irr.IEventReceiver.__init__(self)
        self.Room = room;
        self.Driver = driver;
        skin = env.getSkin();
        font = env.getFont(MEDIA_PATH+"/fonthaettenschweiler.bmp");
        if (font):
            skin.setFont(font);

        window = env.addWindow(
                irr.core.recti(460,375,630,470), False, u"Use 'E' + 'R' to change");

        self.ListBox = env.addListBox(
                irr.core.recti(2,22,165,88), window);

        self.ListBox.addItem(u"Diffuse");
        self.ListBox.addItem(u"Bump mapping");
        self.ListBox.addItem(u"Parallax mapping");
        self.ListBox.setSelected(1);

        self.ProblemText = env.addStaticText(
                u"Your hardware or this renderer is not able to use the "
                u"needed shaders for this material. Using fall back materials.",
                irr.core.recti(150,20,470,80));

        self.ProblemText.setOverrideColor(irr.video.SColor(100,255,255,255));

        renderer = self.Driver.getMaterialRenderer(irr.video.EMT_PARALLAX_MAP_SOLID);
        if (renderer and renderer.getRenderCapability() == 0):
            self.ListBox.setSelected(2);

        self.setMaterial();

    def OnEvent(self, event):
        if (event.EventType == irr.irr.EET_KEY_INPUT_EVENT and
                not event.Info.KeyInput.PressedDown and self.Room and self.ListBox):
            sel = self.ListBox.getSelected();
            if (event.Info.KeyInput.Key == irr.irr.KEY_KEY_R):
                sel+=1;
            else:
                if (event.Info.KeyInput.Key == irr.irr.KEY_KEY_E):
                    sel-=1;
                else:
                    return False;

            if (sel > 2):
                sel = 0;
            if (sel < 0):
                sel = 2;
            self.ListBox.setSelected(sel);

            self.setMaterial();

        return False;

    def setMaterial(self):
        materialType = irr.video.EMT_SOLID;
        selected=self.ListBox.getSelected()
        if selected== 0: 
            materialType = irr.video.EMT_SOLID;
        elif selected== 1: 
            materialType = irr.video.EMT_NORMAL_MAP_SOLID;
        elif selected== 2: 
            materialType = irr.video.EMT_PARALLAX_MAP_SOLID;

        self.Room.setMaterialType(materialType);

        renderer = self.Driver.getMaterialRenderer(materialType);
        if (not renderer or renderer.getRenderCapability() != 0):
            self.ProblemText.setVisible(True);
        else:
            self.ProblemText.setVisible(False);


if __name__=="__main__":
    device = irr.createDevice(irr.video.EDT_OPENGL,
            irr.core.dimension2du(640, 480));

    if not device:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();
    env = device.getGUIEnvironment();

    driver.setTextureCreationFlag(irr.video.ETCF_ALWAYS_32_BIT, True);

    env.addImage(driver.getTexture(MEDIA_PATH+"/irrlichtlogo2.png"),
            irr.core.position2di(10,10));

    camera = smgr.addCameraSceneNodeFPS();
    camera.setPosition(irr.core.vector3df(-200,200,-200));

    device.getCursorControl().setVisible(False);

    driver.setFog(irr.video.SColor(0,138,125,81), 
            irr.video.EFT_FOG_LINEAR, 250, 1000, 0.003, True, False);

    roomMesh = smgr.getMesh(MEDIA_PATH+"/room.3ds");
    room = None;
    if (roomMesh):
        smgr.getMeshManipulator().makePlanarTextureMapping(
                roomMesh.getMesh(0), 0.003);

        normalMap = driver.getTexture(MEDIA_PATH+"/rockwall_height.bmp");

        if (normalMap):
            driver.makeNormalMapTexture(normalMap, 9.0);

        tangentMesh = smgr.getMeshManipulator().createMeshWithTangents(roomMesh.getMesh(0));

        room = smgr.addMeshSceneNode(tangentMesh);
        room.setMaterialTexture(0,
                driver.getTexture(MEDIA_PATH+"/rockwall.jpg"));
        room.setMaterialTexture(1, normalMap);

        room.getMaterial(0).SpecularColor.set(0,0,0,0);

        room.setMaterialFlag(irr.video.EMF_FOG_ENABLE, True);
        room.setMaterialType(irr.video.EMT_PARALLAX_MAP_SOLID);
        room.getMaterial(0).MaterialTypeParam = 0.035;

    earthMesh = smgr.getMesh(MEDIA_PATH+"/earth.x");
    if (earthMesh):
        manipulator = smgr.getMeshManipulator();

        tangentSphereMesh = manipulator.createMeshWithTangents(earthMesh.getMesh(0));

        manipulator.setVertexColorAlpha(tangentSphereMesh, 200);

        m=irr.core.matrix4();
        m.setScale ( irr.core.vector3df(50,50,50) );
        manipulator.transformMesh( tangentSphereMesh, m );
        sphere = smgr.addMeshSceneNode(tangentSphereMesh);
        sphere.setPosition(irr.core.vector3df(-70,130,45));
        earthNormalMap = driver.getTexture(MEDIA_PATH+"/earthbump.jpg");
        if (earthNormalMap):
            driver.makeNormalMapTexture(earthNormalMap, 20.0);
            sphere.setMaterialTexture(1, earthNormalMap);
            sphere.setMaterialType(irr.video.EMT_NORMAL_MAP_TRANSPARENT_VERTEX_ALPHA);

        sphere.setMaterialFlag(irr.video.EMF_FOG_ENABLE, True);

        anim = smgr.createRotationAnimator(irr.core.vector3df(0,0.1,0));
        sphere.addAnimator(anim);

    light1 = smgr.addLightSceneNode(None, irr.core.vector3df(0,0,0),
            irr.video.SColorf(0.5, 1.0, 0.5, 0.0), 800.0);
    light1.setDebugDataVisible ( irr.scene.EDS_BBOX );
    anim = smgr.createFlyCircleAnimator (irr.core.vector3df(50,300,0),190.0, -0.003);
    light1.addAnimator(anim);

    bill = smgr.addBillboardSceneNode(light1, irr.core.dimension2df(60, 60));
    bill.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    bill.setMaterialFlag(irr.video.EMF_ZWRITE_ENABLE, False);
    bill.setMaterialType(irr.video.EMT_TRANSPARENT_ADD_COLOR);
    bill.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/particlered.bmp"));

    light2 = smgr.addLightSceneNode(None, irr.core.vector3df(0,0,0),
            irr.video.SColorf(1.0, 0.2, 0.2, 0.0), 800.0);

    anim = smgr.createFlyCircleAnimator(irr.core.vector3df(0,150,0), 200.0,
            0.001, irr.core.vector3df(0.2, 0.9, 0.0));
    light2.addAnimator(anim);

    bill = smgr.addBillboardSceneNode(light2, irr.core.dimension2df(120, 120));
    bill.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    bill.setMaterialFlag(irr.video.EMF_ZWRITE_ENABLE, False);
    bill.setMaterialType(irr.video.EMT_TRANSPARENT_ADD_COLOR);
    bill.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/particlewhite.bmp"));

    ps = smgr.addParticleSystemSceneNode(False, light2);
    em = ps.createBoxEmitter(
            irr.core.aabbox3df(-3,0,-3,3,1,3),
            irr.core.vector3df(0.0,0.03,0.0),
            80,100,
            irr.video.SColor(0,255,255,255), irr.video.SColor(0,255,255,255),
            400,1100);
    em.setMinStartSize(irr.core.dimension2df(30.0, 40.0));
    em.setMaxStartSize(irr.core.dimension2df(30.0, 40.0));

    ps.setEmitter(em);

    paf = ps.createFadeOutParticleAffector();
    ps.addAffector(paf);

    ps.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    ps.setMaterialFlag(irr.video.EMF_ZWRITE_ENABLE, False);
    ps.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/fireball.bmp"));
    ps.setMaterialType(irr.video.EMT_TRANSPARENT_VERTEX_ALPHA);

    receiver=MyEventReceiver(room, env, driver);
    device.setEventReceiver(receiver);

    lastFPS = -1;

    while (device.run()):
        if (device.isWindowActive()):
            driver.beginScene(True, True);

            smgr.drawAll();
            env.drawAll();

            driver.endScene();

            fps = driver.getFPS();

            if (lastFPS != fps):
                device.setWindowCaption(u"Per pixel lighting example - Irrlicht Engine [%s] FPS: %d" % (
                    driver.getName(), fps))
                lastFPS = fps;

