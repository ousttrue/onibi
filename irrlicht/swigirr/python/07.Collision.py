import sys
import irr

ID_IsNotPickable = 0
IDFlag_IsPickable = 1 << 0
IDFlag_IsHighlightable = 1 << 1

MEDIA_PATH="../../../../media"

if __name__=="__main__":
    device = irr.createDevice(irr.video.EDT_OPENGL, 
            irr.core.dimension2du(640, 480), 16, False);

    if not device:
        sys.exit(1)

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    device.getFileSystem().addZipFileArchive(MEDIA_PATH+"/map-20kdm2.pk3");

    q3levelmesh = smgr.getMesh("20kdm2.bsp");
    q3node = None;

    if q3levelmesh:
        q3node = smgr.addOctreeSceneNode(q3levelmesh.getMesh(0), None, IDFlag_IsPickable);

    selector = None;
    if q3node:
        q3node.setPosition(irr.core.vector3df(-1350,-130,-1400));
        selector = smgr.createOctreeTriangleSelector(
                q3node.getMesh(), q3node, 128);
        q3node.setTriangleSelector(selector);

    camera = smgr.addCameraSceneNodeFPS(None, 100.0, 0.3, ID_IsNotPickable, None, 0, True, 3.0);
    camera.setPosition(irr.core.vector3df(50,50,-60));
    camera.setTarget(irr.core.vector3df(-70,30,-60));

    if selector:
        anim = smgr.createCollisionResponseAnimator(
                selector, camera, irr.core.vector3df(30,50,30),
                irr.core.vector3df(0,-10,0), irr.core.vector3df(0,30,0));
        camera.addAnimator(anim);

    device.getCursorControl().setVisible(False);

    bill = smgr.addBillboardSceneNode();
    bill.setMaterialType(irr.video.EMT_TRANSPARENT_ADD_COLOR );
    bill.setMaterialTexture(0, driver.getTexture(MEDIA_PATH+"/particle.bmp"));
    bill.setMaterialFlag(irr.video.EMF_LIGHTING, False);
    bill.setMaterialFlag(irr.video.EMF_ZBUFFER, False);
    bill.setSize(irr.core.dimension2df(20.0, 20.0));
    bill.setID(ID_IsNotPickable); 

    node = None;
    node = smgr.addAnimatedMeshSceneNode(smgr.getMesh(MEDIA_PATH+"/faerie.md2"),
            None, IDFlag_IsPickable | IDFlag_IsHighlightable);
    print(node)
    node.setPosition(irr.core.vector3df(-70,-15,-120));
    node.setScale(irr.core.vector3df(2, 2, 2));
    node.setMD2Animation(irr.scene.EMAT_POINT);
    node.setAnimationSpeed(20.0);
    material=irr.video.SMaterial();
    material.setTexture(0, driver.getTexture(MEDIA_PATH+"/faerie2.bmp"));
    material.Lighting = True;
    material.NormalizeNormals = True;
    node.setMaterial(0, material);

    selector = smgr.createTriangleSelector(node);
    node.setTriangleSelector(selector);

    node = smgr.addAnimatedMeshSceneNode(smgr.getMesh(MEDIA_PATH+"/dwarf.x"),
            None, IDFlag_IsPickable | IDFlag_IsHighlightable);
    node.setPosition(irr.core.vector3df(-70,-66,0));
    node.setRotation(irr.core.vector3df(0,-90,0));
    node.setAnimationSpeed(20.0);
    selector = smgr.createTriangleSelector(node);
    node.setTriangleSelector(selector);

    node = smgr.addAnimatedMeshSceneNode(smgr.getMesh(MEDIA_PATH+"/ninja.b3d"),
            None, IDFlag_IsPickable | IDFlag_IsHighlightable);
    node.setScale(irr.core.vector3df(10, 10, 10));
    node.setPosition(irr.core.vector3df(-70,-66,-60));
    node.setRotation(irr.core.vector3df(0,90,0));
    node.setAnimationSpeed(10.0);
    node.getMaterial(0).NormalizeNormals = True;
    selector = smgr.createTriangleSelector(node);
    node.setTriangleSelector(selector);

    material.setTexture(0, None);
    material.Lighting = False;

    light = smgr.addLightSceneNode(None, irr.core.vector3df(-60,100,400),
            irr.video.SColorf(1.0,1.0,1.0,1.0), 600.0);
    print(light)
    light.setID(ID_IsNotPickable);

    highlightedSceneNode = None;
    collMan = smgr.getSceneCollisionManager();
    lastFPS = -1;

    material.Wireframe=True;

    while device.run():
        if device.isWindowActive():
            driver.beginScene(True, True);
            smgr.drawAll();

            if highlightedSceneNode:
                highlightedSceneNode.setMaterialFlag(irr.video.EMF_LIGHTING, True);
                highlightedSceneNode = 0;

            ray=irr.core.line3df()
            ray.start = camera.getPosition();
            ray.end = ray.start + (camera.getTarget() - ray.start).normalize() * 1000.0;

            intersection=irr.core.vector3df();
            hitTriangle=irr.core.triangle3df();

            selectedSceneNode = collMan.getSceneNodeAndCollisionPointFromRay(
                    ray,
                    intersection,
                    hitTriangle,
                    IDFlag_IsPickable,
                    None);

            if selectedSceneNode:
                bill.setPosition(intersection);

                driver.setTransform(irr.video.ETS_WORLD, irr.core.matrix4());
                driver.setMaterial(material);
                driver.draw3DTriangle(hitTriangle, irr.video.SColor(0,255,0,0));

                if (selectedSceneNode.getID() & IDFlag_IsHighlightable) == IDFlag_IsHighlightable:
                    highlightedSceneNode = selectedSceneNode;
                    highlightedSceneNode.setMaterialFlag(irr.video.EMF_LIGHTING, False);

            driver.endScene();

            fps = driver.getFPS();

            if lastFPS != fps:
                msg = u"Collision detection example - Irrlicht Engine [%s] FPS:%d" % (
                        driver.getName(), fps)
                device.setWindowCaption(msg);
                lastFPS = fps;

