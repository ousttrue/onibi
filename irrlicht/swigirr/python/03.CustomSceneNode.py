import sys
import irr

class CSampleSceneNode(irr.scene.ISceneNode):

    def __init__(self, parent, mgr, id):
        irr.scene.ISceneNode.__init__(self, parent, mgr, id)
        self.Material=irr.video.SMaterial()
        self.Material.Wireframe = False;
        self.Material.Lighting = False;

        self.Vertices=[
                irr.video.S3DVertex(0,0,10, 1,1,0,
                    irr.video.SColor(255,0,255,255), 0, 1),
                irr.video.S3DVertex(10,0,-10, 1,0,0,
                    irr.video.SColor(255,255,0,255), 1, 1),
                irr.video.S3DVertex(0,20,0, 0,1,1,
                    irr.video.SColor(255,255,255,0), 1, 0),
                irr.video.S3DVertex(-10,0,-10, 0,0,1,
                    irr.video.SColor(255,0,255,0), 0, 0),
                ]
        self.indices = [ 0,2,3, 2,1,3, 1,0,3, 2,0,1 ];

        self.Box=irr.core.aabbox3df()
        self.Box.reset(self.Vertices[0].Pos);
        for v in self.Vertices:
            self.Box.addInternalPoint(v.Pos);

    def OnRegisterSceneNode(self):
        if self.isVisible():
            self.getSceneManager().registerNodeForRendering(self);
        irr.scene.ISceneNode.OnRegisterSceneNode(self);

    def render(self):
        driver = self.getSceneManager().getVideoDriver();
        driver.setMaterial(self.Material);
        driver.setTransform(irr.video.ETS_WORLD, self.getAbsoluteTransformation());
        driver.drawVertexPrimitiveList(self.Vertices, self.indices,
                irr.video.EVT_STANDARD, irr.scene.EPT_TRIANGLES, irr.video.EIT_16BIT)

    def getBoundingBox(self):
        return self.Box;

    def getMaterialCount(self):
        return 1;

    def getMaterial(self, i):
        return self.Material;


if __name__=="__main__":

    device = irr.createDevice(irr.video.EDT_OPENGL,
            irr.core.dimension2du(640, 480), 16, False);
    if not device:
        sys.exit(1);

    device.setWindowCaption(u"Custom Scene Node - Irrlicht Engine Demo");

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    smgr.addCameraSceneNode(None, irr.core.vector3df(0,-40,0), irr.core.vector3df(0,0,0));

    myNode = CSampleSceneNode(smgr.getRootSceneNode(), smgr, 666);

    anim = smgr.createRotationAnimator(irr.core.vector3df(0.8, 0, 0.8));
    if anim:
        myNode.addAnimator(anim);

    frames=0;
    while device.run():
        driver.beginScene(True, True, irr.video.SColor(0,100,100,100));

        smgr.drawAll();

        driver.endScene();
        frames+=1
        if frames==100:
            msg = u"Irrlicht Engine [%s] FPS: %d" % (
                    driver.getName(),
                    driver.getFPS())
            device.setWindowCaption(msg);
            frames=0;

    sys.exit(0);

