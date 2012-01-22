import os
import sys
import irr


MEDIA_PATH=os.path.join(
        os.path.dirname(__file__),
        "../../../irrlicht/media"
        )

if __name__=="__main__":
    device = irr.createDevice(irr.video.EDT_OPENGL, irr.core.dimension2du(640, 480));
    if not device:
        sys.exit(1)

    device.setWindowCaption(u"Load .irr file example");

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    if (len(sys.argv)>1):
        smgr.loadScene(sys.argv[1]);
    else:
        smgr.loadScene(MEDIA_PATH+"/example.irr");

    camera = smgr.addCameraSceneNodeFPS(None, 50.0, 0.1);

    meta = smgr.createMetaTriangleSelector();

    nodes=smgr.getSceneNodesFromType(irr.scene.ESNT_ANY);

    for node in nodes:
        selector = None;
        nodeType=node.getType()
        if (nodeType==irr.scene.ESNT_CUBE
                or node.getType()== irr.scene.ESNT_ANIMATED_MESH):
            selector = smgr.createTriangleSelectorFromBoundingBox(node);

        elif (nodeType==irr.scene.ESNT_MESH
                or nodeType== irr.scene.ESNT_SPHERE):
            selector = smgr.createTriangleSelector(irr.scene.IMeshSceneNode.cast(node).getMesh(), node);

        elif nodeType==irr.scene.ESNT_TERRAIN:
            selector = smgr.createTerrainTriangleSelector(irr.scene.ITerrainSceneNode.cast(node));

        elif nodeType==irr.scene.ESNT_OCTREE:
            selector = smgr.createOctreeTriangleSelector(irr.scene.IMeshSceneNode.cast(node).getMesh(), node);

        if(selector):
            meta.addTriangleSelector(selector);

    anim = smgr.createCollisionResponseAnimator(
            meta, camera, irr.core.vector3df(5,5,5),
            irr.core.vector3df(0,0,0));

    camera.addAnimator(anim);

    camera.setPosition(irr.core.vector3df(0.0, 20.0, 0.0));

    cube = smgr.getSceneNodeFromType(irr.scene.ESNT_CUBE);
    if(cube):
        camera.setTarget(cube.getAbsolutePosition());

    lastFPS = -1;
    while(device.run()):
        if (device.isWindowActive()):
            driver.beginScene(True, True, irr.video.SColor(0,200,200,200));
            smgr.drawAll();
            driver.endScene();

            fps = driver.getFPS();

            if (lastFPS != fps):
                device.setWindowCaption(u"Load Irrlicht File example - Irrlicht Engine [%s] FPS:%d" % (
                    driver.getName(), fps));
                lastFPS = fps;

