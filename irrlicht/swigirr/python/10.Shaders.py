import os
import sys
import irr

MEDIA_PATH=os.path.join(
        os.path.dirname(__file__), 
        "../../../irrlicht/media")

device = None
UseHighLevelShaders = False


class MyShaderCallBack(irr.video.IShaderConstantSetCallBack):
    def __init__(self):
        irr.video.IShaderConstantSetCallBack.__init__(self)

    def OnSetConstants(self, services, userData):
        driver = services.getVideoDriver();
        invWorld = driver.getTransform(irr.video.ETS_WORLD);
        invWorld.makeInverse();

        if (UseHighLevelShaders):
            services.setVertexShaderConstant("mInvWorld", invWorld.pointer(), 16);
        else:
            services.setVertexShaderConstant(invWorld.pointer(), 0, 4);

        worldViewProj=irr.core.matrix4();
        worldViewProj = driver.getTransform(irr.video.ETS_PROJECTION);
        worldViewProj *= driver.getTransform(irr.video.ETS_VIEW);
        worldViewProj *= driver.getTransform(irr.video.ETS_WORLD);

        if (UseHighLevelShaders):
            services.setVertexShaderConstant("mWorldViewProj", worldViewProj.pointer(), 16);
        else:
            services.setVertexShaderConstant(worldViewProj.pointer(), 4, 4);

        pos = device.getSceneManager().getActiveCamera().getAbsolutePosition();

        if (UseHighLevelShaders):
            services.setVertexShaderConstant("mLightPos", irr.FloatPointer(pos), 3);
        else:
            services.setVertexShaderConstant(irr.FloatPointer(pos), 8, 1);

        col=irr.video.SColorf(0.0 ,1.0 ,1.0 ,0.0);
        if (UseHighLevelShaders):
            services.setVertexShaderConstant("mLightColor", irr.FloatPointer(col), 4);
        else:
            services.setVertexShaderConstant(irr.FloatPointer(col), 9, 1);

        world = driver.getTransform(irr.video.ETS_WORLD).getTransposed();

        if (UseHighLevelShaders):
            services.setVertexShaderConstant("mTransWorld", world.pointer(), 16);
        else:
            services.setVertexShaderConstant(world.pointer(), 10, 4);


if __name__=="__main__":
    UseHighLevelShaders = True;
    device = irr.createDevice(irr.video.EDT_OPENGL, irr.core.dimension2du(640, 480));

    if not device:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();
    gui = device.getGUIEnvironment();

    if (UseHighLevelShaders):
        psFileName = MEDIA_PATH+"/opengl.frag";
        vsFileName = MEDIA_PATH+"/opengl.vert";
    else:
        psFileName = MEDIA_PATH+"/opengl.psh";
        vsFileName = MEDIA_PATH+"/opengl.vsh";

    if (not driver.queryFeature(irr.video.EVDF_PIXEL_SHADER_1_1) and
            not driver.queryFeature(irr.video.EVDF_ARB_FRAGMENT_PROGRAM_1)):
        device.getLogger().log("WARNING: Pixel shaders disabled "
            "because of missing driver/hardware support.");
        psFileName = "";

    if (not driver.queryFeature(irr.video.EVDF_VERTEX_SHADER_1_1) and 
            not driver.queryFeature(irr.video.EVDF_ARB_VERTEX_PROGRAM_1)):
        device.getLogger().log("WARNING: Vertex shaders disabled "\
            "because of missing driver/hardware support.");
        vsFileName = "";

    gpu = driver.getGPUProgrammingServices();
    newMaterialType1 = 0;
    newMaterialType2 = 0;

    if (gpu):
        mc = MyShaderCallBack();

        if (UseHighLevelShaders):
            newMaterialType1 = gpu.addHighLevelShaderMaterialFromFiles(
                vsFileName, "vertexMain", irr.video.EVST_VS_1_1,
                psFileName, "pixelMain", irr.video.EPST_PS_1_1,
                mc, irr.video.EMT_SOLID);

            newMaterialType2 = gpu.addHighLevelShaderMaterialFromFiles(
                vsFileName, "vertexMain", irr.video.EVST_VS_1_1,
                psFileName, "pixelMain", irr.video.EPST_PS_1_1,
                mc, irr.video.EMT_TRANSPARENT_ADD_COLOR);
        else:
            newMaterialType1 = gpu.addShaderMaterialFromFiles(vsFileName,
                psFileName, mc, irr.video.EMT_SOLID);

            newMaterialType2 = gpu.addShaderMaterialFromFiles(vsFileName,
                psFileName, mc, irr.video.EMT_TRANSPARENT_ADD_COLOR);


    node = smgr.addCubeSceneNode(50);
    node.setPosition(irr.core.vector3df(0,0,0));
    node.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/wall.bmp"));
    node.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    node.setMaterialType(newMaterialType1);

    smgr.addTextSceneNode(gui.getBuiltInFont(),
            u"PS & VS & EMT_SOLID",
            irr.video.SColor(255,255,255,255), node);

    anim = smgr.createRotationAnimator(irr.core.vector3df(0, 0.3, 0));
    node.addAnimator(anim);

    node = smgr.addCubeSceneNode(50);
    node.setPosition(irr.core.vector3df(0,-10,50));
    node.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/wall.bmp"));
    node.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    node.setMaterialType(newMaterialType2);

    smgr.addTextSceneNode(gui.getBuiltInFont(),
            u"PS & VS & EMT_TRANSPARENT",
            irr.video.SColor(255,255,255,255), node);

    anim = smgr.createRotationAnimator(irr.core.vector3df(0, 0.3 ,0));
    node.addAnimator(anim);

    node = smgr.addCubeSceneNode(50);
    node.setPosition(irr.core.vector3df(0,50,25));
    node.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/wall.bmp"));
    node.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    smgr.addTextSceneNode(gui.getBuiltInFont(), u"NO SHADER",
        irr.video.SColor(255,255,255,255), node);

    driver.setTextureCreationFlag(irr.video.ETCF_CREATE_MIP_MAPS, False);

    smgr.addSkyBoxSceneNode(
        driver.getTexture(MEDIA_PATH+"/irrlicht2_up.jpg"),
        driver.getTexture(MEDIA_PATH+"/irrlicht2_dn.jpg"),
        driver.getTexture(MEDIA_PATH+"/irrlicht2_lf.jpg"),
        driver.getTexture(MEDIA_PATH+"/irrlicht2_rt.jpg"),
        driver.getTexture(MEDIA_PATH+"/irrlicht2_ft.jpg"),
        driver.getTexture(MEDIA_PATH+"/irrlicht2_bk.jpg"));

    driver.setTextureCreationFlag(irr.video.ETCF_CREATE_MIP_MAPS, True);

    cam = smgr.addCameraSceneNodeFPS();
    cam.setPosition(irr.core.vector3df(-100,50,100));
    cam.setTarget(irr.core.vector3df(0,0,0));
    device.getCursorControl().setVisible(False);

    lastFPS = -1;

    while device.run():
        if (device.isWindowActive()):
            driver.beginScene(True, True, irr.video.SColor(255,0,0,0));
            smgr.drawAll();
            driver.endScene();

            fps = driver.getFPS();
            if (lastFPS != fps):
                device.setWindowCaption(
                        u"Irrlicht Engine - Vertex and pixel shader example [%s] FPS: %d" % (
                            driver.getName(),
                            fps
                            ));
                lastFPS = fps;

