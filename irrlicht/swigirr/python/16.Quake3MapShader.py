import os
import sys
import irr

MEDIA_PATH=os.path.join(
        os.path.dirname(__file__),
        "../../media"
        )

#QUAKE3_STORAGE_FORMAT=addFolderFileArchive
#QUAKE3_STORAGE_1="/baseq3/"
#QUAKE3_STORAGE_1="../../media/"
QUAKE3_STORAGE_1="../../media/map-20kdm2.pk3"
QUAKE3_STORAGE_2="/cf/"
#QUAKE3_MAP_NAME="maps/cf.bsp"
QUAKE3_MAP_NAME="maps/20kdm2.bsp"


class CScreenShotFactory(irr.IEventReceiver):
    def __init__(self, device, templateName, node):
        irr.IEventReceiver.__init__(self)
        self.Device=device
        self.Number=0
        self.FilenameTemplate=templateName.replace('/', '_').replace("\\", "_")
        self.Node=node

    def OnEvent(self, event):
        if ((event.EventType == irr.EET_KEY_INPUT_EVENT) and
                event.Info.KeyInput.PressedDown):
            if (event.Info.KeyInput.Key == irr.KEY_F9):
                image = Device.getVideoDriver().createScreenShot();
                if (image):
                    self.Number+=1
                    buf="%s_shot%04d.jpg" % (
                            self.FilenameTemplate,
                            self.Number);
                    Device.getVideoDriver().writeImageToFile(image, buf, 85);
            else:
                if (event.Info.KeyInput.Key == irr.KEY_F8):
                    if (Node.isDebugDataVisible()):
                        Node.setDebugDataVisible(irr.scene.EDS_OFF);
                    else:
                        Node.setDebugDataVisible(irr.scene.EDS_BBOX_ALL);
        return False;


if __name__=="__main__":
    videoDim=irr.core.dimension2du(800,600);

    device = irr.createDevice(irr.video.EDT_OPENGL, videoDim, 32, False );

    if not device:
        sys.exit(1)

    mapname=None;
    if len(sys.argv)>2:
        mapname = sys.argv[2];
    else:
        mapname = QUAKE3_MAP_NAME;

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();
    gui = device.getGUIEnvironment();

    #device.getFileSystem().addFolderFileArchive(MEDIA_PATH);
    #device.getFileSystem().addFolderFileArchive("../../media/");

    if len(sys.argv)>2:
        device.getFileSystem().addZipFileArchive(sys.argv[1]);
    else:
        device.getFileSystem().addZipFileArchive(QUAKE3_STORAGE_1);

    smgr.getParameters().setAttribute(irr.scene.ALLOW_ZWRITE_ON_TRANSPARENT, True);

    mesh = irr.scene.IQ3LevelMesh.cast(smgr.getMesh(mapname));

    node = None;
    if (mesh):
        geometry = mesh.getMesh(irr.scene.E_Q3_MESH_GEOMETRY);
        node = smgr.addOctreeSceneNode(geometry, None, -1, 4096);

    screenshotFactory=CScreenShotFactory(device, mapname, node);
    device.setEventReceiver(screenshotFactory);

    if ( mesh ):
        additional_mesh = mesh.getMesh(irr.scene.E_Q3_MESH_ITEMS);
        font = device.getGUIEnvironment().getFont(MEDIA_PATH+"/fontlucida.png");
        count = 0;

        for i in range(additional_mesh.getMeshBufferCount()):
            meshBuffer = additional_mesh.getMeshBuffer(i);
            material = meshBuffer.getMaterial();

            shaderIndex = int(material.MaterialTypeParam2);
            shader = mesh.getShader(int(shaderIndex));
            if not shader:
                continue;

            """
            count += 1;
            name=smgr.addQuake3SceneNode(meshBuffer, shader).getName()
            node = smgr.addBillboardTextSceneNode(
                    font, name, node,
                    irr.core.dimension2df(80.0, 8.0),
                    irr.core.vector3df(0, 10, 0));
            """

    camera = smgr.addCameraSceneNodeFPS();

    if ( mesh ):
        entityList = mesh.getEntityList();

        search=irr.scene.IShader();
        search.name = "info_player_deathmatch";

        index = entityList.binary_search(search);
        if (index >= 0):
            notEndList=None;
            while True:
                    print(index)
                    group = entityList.get(index).getGroup(1);

                    parsepos = irr.new_u32(0);
                    pos = irr.scene.getAsVector3df(group.get("origin"), parsepos);
                    irr.delete_u32(parsepos)

                    parsepos = irr.new_u32(0);
                    angle = irr.scene.getAsFloat(group.get("angle"), parsepos);
                    irr.delete_u32(parsepos)

                    target=irr.core.vector3df(0.0, 0.0, 1.0);
                    target.rotateXZBy(angle);

                    camera.setPosition(pos);
                    camera.setTarget(pos + target);

                    index+=1;
                    notEndList = index == 2;
                    if not notEndList:
                        break

            device.getCursorControl().setVisible(False);

    gui.addImage(driver.getTexture("irrlichtlogo2.png"),
            irr.core.position2di(10, 10));

    pos=irr.core.position2di(videoDim.Width - 128, videoDim.Height - 64);

    gui.addImage(driver.getTexture("opengllogo.png"), pos);

    lastFPS = -1;
    while(device.run()):
        if (device.isWindowActive()):
            driver.beginScene(True, True, irr.video.SColor(255,20,20,40));
            smgr.drawAll();
            gui.drawAll();
            driver.endScene();

            fps = driver.getFPS();

            attr = smgr.getParameters();
            caption=u"Q3 [%s] FPS:%d Cull:%d/%d Draw:%d/%d/%d" % (
                    driver.getName(),
                    fps,
                    attr.getAttributeAsInt("calls"),
                    attr.getAttributeAsInt("culled"),
                    attr.getAttributeAsInt("drawn_solid"),
                    attr.getAttributeAsInt("drawn_transparent"),
                    attr.getAttributeAsInt("drawn_transparent_effect"))
            device.setWindowCaption(caption);
            lastFPS = fps;

