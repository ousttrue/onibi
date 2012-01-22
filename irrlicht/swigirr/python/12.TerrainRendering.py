import os
import sys
import irr


MEDIA_PATH=os.path.join(
        os.path.dirname(__file__),
        "../../../irrlicht/media"
        )

class MyEventReceiver(irr.IEventReceiver):
    def __init__(self, terrain, skybox, skydome) :
        irr.IEventReceiver.__init__(self)
        self.Terrain=terrain
        self.Skybox=skybox
        self.Skybox.setVisible(True);
        self.Skydome=skydome
        self.Skydome.setVisible(False);
        self.showBox=True

    def OnEvent(self, event):
        if (event.EventType == irr.irr.EET_KEY_INPUT_EVENT 
                and not event.Info.KeyInput.PressedDown):

            key=event.Info.KeyInput.Key
            if key==irr.irr.KEY_KEY_W:
                self.Terrain.setMaterialFlag(irr.video.EMF_WIREFRAME,
                        not self.Terrain.getMaterial(0).Wireframe);
                self.Terrain.setMaterialFlag(irr.video.EMF_POINTCLOUD, False);
                return True;
            elif key== irr.irr.KEY_KEY_P:
                self.Terrain.setMaterialFlag(irr.video.EMF_POINTCLOUD,
                        not self.Terrain.getMaterial(0).PointCloud);
                self.Terrain.setMaterialFlag(irr.video.EMF_WIREFRAME, False);
                return True;
            elif key== irr.irr.KEY_KEY_D:
                self.Terrain.setMaterialType(
                        (self.Terrain.getMaterial(0).MaterialType == irr.video.EMT_SOLID) 
                        and irr.video.EMT_DETAIL_MAP 
                        or irr.video.EMT_SOLID);
                return True;
            elif key== irr.irr.KEY_KEY_S:
                self.showBox=not self.showBox;
                self.Skybox.setVisible(self.showBox);
                self.Skydome.setVisible(not self.showBox);
                return True;
        return False;


if __name__=="__main__":
    params=irr.SIrrlichtCreationParameters();
    params.DriverType=irr.video.EDT_OPENGL;
    params.WindowSize=irr.core.dimension2du(640, 480);
    device = irr.createDeviceEx(params);
    if not device:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();
    env = device.getGUIEnvironment();

    driver.setTextureCreationFlag(irr.video.ETCF_ALWAYS_32_BIT, True);

    env.addImage(driver.getTexture(MEDIA_PATH+"/irrlichtlogo2.png"),
            irr.core.position2di(10,10));

    env.getSkin().setFont(env.getFont(MEDIA_PATH+"/fontlucida.png"));

    env.addStaticText(
            u"Press 'W' to change wireframe mode\n"
            u"Press 'D' to toggle detail map\n"
            u"Press 'S' to toggle skybox/skydome",
            irr.core.recti(10,421,250,475), True, True, None, -1, True);

    camera = smgr.addCameraSceneNodeFPS(None,100.0,1.2);

    camera.setPosition(irr.core.vector3df(2700*2,255*2,2600*2));
    camera.setTarget(irr.core.vector3df(2397*2,343*2,2700*2));
    camera.setFarValue(42000.0);

    device.getCursorControl().setVisible(False);

    terrain = smgr.addTerrainSceneNode(
            MEDIA_PATH+"/terrain-heightmap.bmp",
            None,
            -1,
            irr.core.vector3df(0.0, 0.0, 0.0),
            irr.core.vector3df(0.0, 0.0, 0.0),
            irr.core.vector3df(40.0, 4.40, 40.0),
            irr.video.SColor ( 255, 255, 255, 255 ),
            5,
            irr.scene.ETPS_17,
            4
            );

    terrain.setMaterialFlag(irr.video.EMF_LIGHTING, False);

    terrain.setMaterialTexture(0,
            driver.getTexture(MEDIA_PATH+"/terrain-texture.jpg"));
    terrain.setMaterialTexture(1,
            driver.getTexture(MEDIA_PATH+"/detailmap3.jpg"));

    terrain.setMaterialType(irr.video.EMT_DETAIL_MAP);

    terrain.scaleTexture(1.0, 20.0);
    #terrain.setDebugDataVisible ( True );

    selector = smgr.createTerrainTriangleSelector(terrain, 0);
    terrain.setTriangleSelector(selector);

    anim = smgr.createCollisionResponseAnimator(
            selector, camera, irr.core.vector3df(60,100,60),
            irr.core.vector3df(0,0,0),
            irr.core.vector3df(0,50,0));
    camera.addAnimator(anim);

    buffer = irr.scene.CDynamicMeshBuffer(irr.video.EVT_2TCOORDS, irr.video.EIT_16BIT);
    terrain.getMeshBufferForLOD(buffer, 0);
    data = irr.video.S3DVertex2TCoords.cast(buffer.getVertexBuffer().getData());

    driver.setTextureCreationFlag(irr.video.ETCF_CREATE_MIP_MAPS, False);

    skybox=smgr.addSkyBoxSceneNode(
            driver.getTexture(MEDIA_PATH+"/irrlicht2_up.jpg"),
            driver.getTexture(MEDIA_PATH+"/irrlicht2_dn.jpg"),
            driver.getTexture(MEDIA_PATH+"/irrlicht2_lf.jpg"),
            driver.getTexture(MEDIA_PATH+"/irrlicht2_rt.jpg"),
            driver.getTexture(MEDIA_PATH+"/irrlicht2_ft.jpg"),
            driver.getTexture(MEDIA_PATH+"/irrlicht2_bk.jpg"));
    skydome=smgr.addSkyDomeSceneNode(
            driver.getTexture(MEDIA_PATH+"/skydome.jpg"),16,8,0.95,2.0);

    driver.setTextureCreationFlag(irr.video.ETCF_CREATE_MIP_MAPS, True);

    receiver=MyEventReceiver(terrain, skybox, skydome);
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
                caption=u"Terrain Renderer - Irrlicht Engine [%s] FPS: %d Height: %f" % (
                        driver.getName(),
                        fps,
                        terrain.getHeight(
                            camera.getAbsolutePosition().X,
                            camera.getAbsolutePosition().Z)
                        )
                device.setWindowCaption(caption);
                lastFPS = fps;

