import sys
import locale
import irr

MEDIA_PATH= "../../../irrlicht/media/"

Device = None;
StartUpModelFile=''
MessageText=u''
Caption=u'';
Model = None;
SkyBox = None;
Octree=False;
UseLight=False;

Camera = [None, None];

def set_global(base, *names):
    num=base
    thismodule = sys.modules[__name__]
    for n in names:
        setattr(thismodule, n, num)
        num+=1

set_global(0x10000, 
    'GUI_ID_DIALOG_ROOT_WINDOW',

    'GUI_ID_X_SCALE',
    'GUI_ID_Y_SCALE',
    'GUI_ID_Z_SCALE',

    'GUI_ID_OPEN_MODEL',
    'GUI_ID_SET_MODEL_ARCHIVE',
    'GUI_ID_LOAD_AS_OCTREE',

    'GUI_ID_SKY_BOX_VISIBLE',
    'GUI_ID_TOGGLE_DEBUG_INFO',

    'GUI_ID_DEBUG_OFF',
    'GUI_ID_DEBUG_BOUNDING_BOX',
    'GUI_ID_DEBUG_NORMALS',
    'GUI_ID_DEBUG_SKELETON',
    'GUI_ID_DEBUG_WIRE_OVERLAY',
    'GUI_ID_DEBUG_HALF_TRANSPARENT',
    'GUI_ID_DEBUG_BUFFERS_BOUNDING_BOXES',
    'GUI_ID_DEBUG_ALL',

    'GUI_ID_MODEL_MATERIAL_SOLID',
    'GUI_ID_MODEL_MATERIAL_TRANSPARENT',
    'GUI_ID_MODEL_MATERIAL_REFLECTION',

    'GUI_ID_CAMERA_MAYA',
    'GUI_ID_CAMERA_FIRST_PERSON',

    'GUI_ID_POSITION_TEXT',

    'GUI_ID_ABOUT',
    'GUI_ID_QUIT',

    'GUI_ID_TEXTUREFILTER',
    'GUI_ID_SKIN_TRANSPARENCY',
    'GUI_ID_SKIN_ANIMATION_FPS',

    'GUI_ID_BUTTON_SET_SCALE',
    'GUI_ID_BUTTON_SCALE_MUL10',
    'GUI_ID_BUTTON_SCALE_DIV10',
    'GUI_ID_BUTTON_OPEN_MODEL',
    'GUI_ID_BUTTON_SHOW_ABOUT',
    'GUI_ID_BUTTON_SHOW_TOOLBOX',
    'GUI_ID_BUTTON_SELECT_ARCHIVE',

    'GUI_ID_ANIMATION_INFO'
    )

MAX_FRAMERATE = 80
DEFAULT_FRAMERATE = 30


def setActiveCamera(newActive):
    if not Device:
        return;

    active = Device.getSceneManager().getActiveCamera();
    active.setInputReceiverEnabled(False);

    newActive.setInputReceiverEnabled(True);
    Device.getSceneManager().setActiveCamera(newActive);


def setSkinTransparency(alpha, skin):
    for i in range(irr.gui.EGDC_COUNT):
        col = skin.getColor(i);
        col.setAlpha(alpha);
        skin.setColor(i, col);


def updateScaleInfo(model):
    toolboxWnd = Device.getGUIEnvironment().getRootGUIElement().getElementFromId(
            GUI_ID_DIALOG_ROOT_WINDOW, True);
    if not toolboxWnd:
        return;
    if not model:
        toolboxWnd.getElementFromId(GUI_ID_X_SCALE, True).setText( u"-" );
        toolboxWnd.getElementFromId(GUI_ID_Y_SCALE, True).setText( u"-" );
        toolboxWnd.getElementFromId(GUI_ID_Z_SCALE, True).setText( u"-" );
    else:
        scale = model.getScale();
        toolboxWnd.getElementFromId(GUI_ID_X_SCALE, True).setText( "%f" % scale.X );
        toolboxWnd.getElementFromId(GUI_ID_Y_SCALE, True).setText( "%f" % scale.Y );
        toolboxWnd.getElementFromId(GUI_ID_Z_SCALE, True).setText( "%f" % scale.Z );

def showAboutText():
    Device.getGUIEnvironment().addMessageBox(Caption, MessageText);


def get_extension(fn):
    pos=fn.rfind('.')
    if pos!=-1:
        return fn[pos:].lower()


def loadModel(fn):
    global Model

    extension=get_extension(fn)
    print extension
    if (extension == ".jpg" or extension == ".pcx" or
        extension == ".png" or extension == ".ppm" or
        extension == ".pgm" or extension == ".pbm" or
        extension == ".psd" or extension == ".tga" or
        extension == ".bmp" or extension == ".wal" or
        extension == ".rgb" or extension == ".rgba"):
        texture = Device.getVideoDriver().getTexture( fn );
        if texture and Model:
            Device.getVideoDriver().removeTexture(texture);
            texture = Device.getVideoDriver().getTexture(fn);
            Model.setMaterialTexture(0, texture);
        return;

    elif (extension == ".pk3" or extension == ".zip" or extension == ".pak" or extension == ".npk"):
        Device.getFileSystem().addFileArchive(fn);
        return;

    if Model:
        Model.remove();

    Model = None;

    if (extension==".irr"):
        Device.getSceneManager().loadScene(fn);
        outNodes=Device.getSceneManager().getSceneNodesFromType(irr.scene.ESNT_ANIMATED_MESH);
        if outNodes.size()>0:
            Model = outNodes[0];
        return;

    m = Device.getSceneManager().getMesh(fn);

    if not m:
        if (StartUpModelFile != fn):
            Device.getGUIEnvironment().addMessageBox(
                    Caption, u"The model could not be loaded. "
                    u"Maybe it is not a supported file format.");
        return;

    if (Octree):
        Model = Device.getSceneManager().addOctreeSceneNode(m.getMesh(0));
    else:
        animModel = Device.getSceneManager().addAnimatedMeshSceneNode(m);
        animModel.setAnimationSpeed(30);
        Model = animModel;

    Model.setMaterialFlag(irr.video.EMF_LIGHTING, UseLight);
    Model.setMaterialFlag(irr.video.EMF_NORMALIZE_NORMALS, UseLight);
    Model.setDebugDataVisible(irr.scene.EDS_OFF);

    menu = irr.gui.IGUIContextMenu.cast(
            Device.getGUIEnvironment().getRootGUIElement().getElementFromId(GUI_ID_TOGGLE_DEBUG_INFO, True));
    if menu:
        for item in range(6):
            menu.setItemChecked(item, False);
    updateScaleInfo(Model);


def createToolBox():
    env = Device.getGUIEnvironment();
    root = env.getRootGUIElement();
    e = root.getElementFromId(GUI_ID_DIALOG_ROOT_WINDOW, True);
    if e:
        e.remove();

    wnd = env.addWindow(irr.core.recti(600,45,800,480),
        False, u"Toolset", None, GUI_ID_DIALOG_ROOT_WINDOW);

    tab = env.addTabControl(
        irr.core.recti(2,20,800-602,480-7), wnd, True, True);

    t1 = tab.addTab(u"Config");

    env.addStaticText(u"Scale:",
            irr.core.recti(10,20,60,45), False, False, t1);
    env.addStaticText(u"X:", irr.core.recti(22,48,40,66), False, False, t1);
    env.addEditBox(u"1.0", irr.core.recti(40,46,130,66), True, t1, GUI_ID_X_SCALE);
    env.addStaticText(u"Y:", irr.core.recti(22,82,40,96), False, False, t1);
    env.addEditBox(u"1.0", irr.core.recti(40,76,130,96), True, t1, GUI_ID_Y_SCALE);
    env.addStaticText(u"Z:", irr.core.recti(22,108,40,126), False, False, t1);
    env.addEditBox(u"1.0", irr.core.recti(40,106,130,126), True, t1, GUI_ID_Z_SCALE);

    env.addButton(irr.core.recti(10,134,85,165), t1, GUI_ID_BUTTON_SET_SCALE, u"Set");

    env.addButton(irr.core.recti(65,20,95,40), t1, GUI_ID_BUTTON_SCALE_MUL10, u"* 10");
    env.addButton(irr.core.recti(100,20,130,40), t1, GUI_ID_BUTTON_SCALE_DIV10, u"* 0.1");

    updateScaleInfo(Model);

    env.addStaticText(u"GUI Transparency Control:",
            irr.core.recti(10,200,150,225), True, False, t1);
    scrollbar = env.addScrollBar(True,
            irr.core.recti(10,225,150,240), t1, GUI_ID_SKIN_TRANSPARENCY);
    scrollbar.setMax(255);
    scrollbar.setPos(255);

    env.addStaticText(u":", irr.core.recti(10,240,150,265), True, False, t1);
    env.addStaticText(u"Framerate:",
            irr.core.recti(12,240,75,265), False, False, t1);
    env.addStaticText(u"", irr.core.recti(75,240,200,265), False, False, t1,
            GUI_ID_ANIMATION_INFO);
    scrollbar = env.addScrollBar(True,
            irr.core.recti(10,265,150,280), t1, GUI_ID_SKIN_ANIMATION_FPS);
    scrollbar.setMax(MAX_FRAMERATE);
    scrollbar.setMin(-MAX_FRAMERATE);
    scrollbar.setPos(DEFAULT_FRAMERATE);
    scrollbar.setSmallStep(1);


def updateToolBox():
    env = Device.getGUIEnvironment();
    root = env.getRootGUIElement();
    dlg = root.getElementFromId(GUI_ID_DIALOG_ROOT_WINDOW, True);
    if not dlg:
        return;

    aniInfo = irr.gui.IGUIStaticText.cast(dlg.getElementFromId(GUI_ID_ANIMATION_INFO, True));
    if aniInfo:
        if ( Model and irr.scene.ESNT_ANIMATED_MESH == Model.getType() ):
            animatedModel = irr.scene.IAnimatedMeshSceneNode.cast(Model);
            msg = u"%d Frame: %d" % (
                    irr.core.round_(animatedModel.getAnimationSpeed()),
                    animatedModel.getFrameNr()
                    )
            aniInfo.setText(msg);
        else:
            aniInfo.setText(u"");


class MyEventReceiver(irr.IEventReceiver):
    def OnEvent(self, event):
        return False
        pass
        if (event.EventType == EET_KEY_INPUT_EVENT and
                event.Info.KeyInput.PressedDown == False):
            if OnKeyUp(event.Info.KeyInput.Key):
                return True;

        if (event.EventType == EET_GUI_EVENT):
            id = event.Info.GUIEvent.Caller.getID();
            env = Device.getGUIEnvironment();

            eventType=event.Info.GUIEvent.EventType
            if eventType==EGET_MENU_ITEM_SELECTED:
                OnMenuItemSelected( IGUIContextMenu.cast(event.Info.GUIEvent.Caller) );

            elif eventType==EGET_FILE_SELECTED:
                dialog = IGUIFileOpenDialog.cast(event.Info.GUIEvent.Caller);
                loadModel(dialog.getFileName());

            elif eventType==EGET_SCROLL_BAR_CHANGED:
                if id == GUI_ID_SKIN_TRANSPARENCY:
                    pos = IGUIScrollBar.cast(event.Info.GUIEvent.Caller).getPos();
                    setSkinTransparency(pos, env.getSkin());
                elif id == GUI_ID_SKIN_ANIMATION_FPS:
                    pos = IGUIScrollBar.cast(event.Info.GUIEvent.Caller).getPos();
                    if irr.scene.ESNT_ANIMATED_MESH == Model.getType():
                        irr.scene.IAnimatedMeshSceneNode.cast(Model).setAnimationSpeed(pos);

            elif eventType==EGET_COMBO_BOX_CHANGED:
                if id == GUI_ID_TEXTUREFILTER:
                    OnTextureFilterSelected(IGUIComboBox.cast(event.Info.GUIEvent.Caller));

            elif eventType==EGET_BUTTON_CLICKED:

                if id==GUI_ID_BUTTON_SET_SCALE:
                    root = env.getRootGUIElement();
                    scale=irr.core.vector3df();

                    s = root.getElementFromId(GUI_ID_X_SCALE, True).getText();
                    scale.X = locale.atof(s);
                    s = root.getElementFromId(GUI_ID_Y_SCALE, True).getText();
                    scale.Y = locale.atof(s);
                    s = root.getElementFromId(GUI_ID_Z_SCALE, True).getText();
                    scale.Z = locale.atof(s);

                    if Model:
                        Model.setScale(scale);
                    updateScaleInfo(Model);

                elif id==GUI_ID_BUTTON_SCALE_MUL10:
                    if Model:
                        Model.setScale(Model.getScale()*10.0);
                    updateScaleInfo(Model);

                elif id==GUI_ID_BUTTON_SCALE_DIV10:
                    if Model:
                        Model.setScale(Model.getScale()*0.10);
                    updateScaleInfo(Model);

                elif id==GUI_ID_BUTTON_OPEN_MODEL:
                    env.addFileOpenDialog(u"Please select a model file to open");

                elif id==GUI_ID_BUTTON_SHOW_ABOUT:
                    showAboutText();

                elif GUI_ID_BUTTON_SHOW_TOOLBOX:
                    createToolBox();

                elif GUI_ID_BUTTON_SELECT_ARCHIVE:
                    env.addFileOpenDialog(u"Please select your game archive/directory");
        return False;

    def OnKeyUp(self, keyCode):
        pass
        if (keyCode == irr.irr.KEY_ESCAPE):
            if Device:
                camera = Device.getSceneManager().getActiveCamera();
                if camera:
                    camera.setInputReceiverEnabled( not camera.isInputReceiverEnabled() );
                return True;

        elif (keyCode == irr.irr.KEY_F1):
            if Device:
                elem = Device.getGUIEnvironment().getRootGUIElement().getElementFromId(GUI_ID_POSITION_TEXT);
                if elem:
                    elem.setVisible(not elem.isVisible());

        elif (keyCode == irr.irr.KEY_KEY_M):
            if Device:
                Device.minimizeWindow();

        elif (keyCode == irr.irr.KEY_KEY_L):
            UseLight= not UseLight;
            if Model:
                Model.setMaterialFlag(irr.video.EMF_LIGHTING, UseLight);
                Model.setMaterialFlag(irr.video.EMF_NORMALIZE_NORMALS, UseLight);

        return False;

    def OnMenuItemSelected(self, menu):
        pass
        id = menu.getItemCommandId(menu.getSelectedItem());
        env = Device.getGUIEnvironment();

        if id==GUI_ID_OPEN_MODEL:
            env.addFileOpenDialog(u"Please select a model file to open");

        elif id==GUI_ID_SET_MODEL_ARCHIVE:
            env.addFileOpenDialog(u"Please select your game archive/directory");

        elif id==GUI_ID_LOAD_AS_OCTREE:
            Octree = not Octree;
            menu.setItemChecked(menu.getSelectedItem(), Octree);

        elif id==GUI_ID_QUIT:
            Device.closeDevice();

        elif id==GUI_ID_SKY_BOX_VISIBLE:
            menu.setItemChecked(menu.getSelectedItem(), not menu.isItemChecked(menu.getSelectedItem()));
            SkyBox.setVisible(not SkyBox.isVisible());

        elif id==GUI_ID_DEBUG_OFF:
            menu.setItemChecked(menu.getSelectedItem()+1, False);
            menu.setItemChecked(menu.getSelectedItem()+2, False);
            menu.setItemChecked(menu.getSelectedItem()+3, False);
            menu.setItemChecked(menu.getSelectedItem()+4, False);
            menu.setItemChecked(menu.getSelectedItem()+5, False);
            menu.setItemChecked(menu.getSelectedItem()+6, False);
            if Model:
                Model.setDebugDataVisible(irr.scene.EDS_OFF);

        elif id==GUI_ID_DEBUG_BOUNDING_BOX:
            menu.setItemChecked(menu.getSelectedItem(), not menu.isItemChecked(menu.getSelectedItem()));
            if Model:
                Model.setDebugDataVisible(Model.isDebugDataVisible()^irr.scene.EDS_BBOX);

        elif id==GUI_ID_DEBUG_NORMALS:
            menu.setItemChecked(menu.getSelectedItem(), not menu.isItemChecked(menu.getSelectedItem()));
            if Model:
                Model.setDebugDataVisible(Model.isDebugDataVisible()^irr.scene.EDS_NORMALS);

        elif id==GUI_ID_DEBUG_SKELETON:
            menu.setItemChecked(menu.getSelectedItem(), not menu.isItemChecked(menu.getSelectedItem()));
            if Model:
                Model.setDebugDataVisible(Model.isDebugDataVisible()^irr.scene.EDS_SKELETON);

        elif id==GUI_ID_DEBUG_WIRE_OVERLAY:
            menu.setItemChecked(menu.getSelectedItem(), not menu.isItemChecked(menu.getSelectedItem()));
            if Model:
                Model.setDebugDataVisible(Model.isDebugDataVisible()^irr.scene.EDS_MESH_WIRE_OVERLAY);

        elif id==GUI_ID_DEBUG_HALF_TRANSPARENT:
            menu.setItemChecked(menu.getSelectedItem(), not menu.isItemChecked(menu.getSelectedItem()));
            if Model:
                Model.setDebugDataVisible(Model.isDebugDataVisible()^irr.scene.EDS_HALF_TRANSPARENCY);

        elif id==GUI_ID_DEBUG_BUFFERS_BOUNDING_BOXES:
            menu.setItemChecked(menu.getSelectedItem(), not menu.isItemChecked(menu.getSelectedItem()));
            if Model:
                Model.setDebugDataVisible(Model.isDebugDataVisible()^irr.scene.EDS_BBOX_BUFFERS);

        elif id==GUI_ID_DEBUG_ALL:
            menu.setItemChecked(menu.getSelectedItem()-1, True);
            menu.setItemChecked(menu.getSelectedItem()-2, True);
            menu.setItemChecked(menu.getSelectedItem()-3, True);
            menu.setItemChecked(menu.getSelectedItem()-4, True);
            menu.setItemChecked(menu.getSelectedItem()-5, True);
            menu.setItemChecked(menu.getSelectedItem()-6, True);
            if Model:
                Model.setDebugDataVisible(irr.scene.EDS_FULL);

        elif id==GUI_ID_ABOUT:
            showAboutText();

        elif id==GUI_ID_MODEL_MATERIAL_SOLID:
            if Model:
                Model.setMaterialType(irr.video.EMT_SOLID);

        elif id==GUI_ID_MODEL_MATERIAL_TRANSPARENT:
            if Model:
                Model.setMaterialType(irr.video.EMT_TRANSPARENT_ADD_COLOR);

        elif id==GUI_ID_MODEL_MATERIAL_REFLECTION:
            if Model:
                Model.setMaterialType(irr.video.EMT_SPHERE_MAP);

        elif id==GUI_ID_CAMERA_MAYA:
            setActiveCamera(Camera[0]);

        elif id==GUI_ID_CAMERA_FIRST_PERSON:
            setActiveCamera(Camera[1]);

    def OnTextureFilterSelected(self, combo):
        pass
        pos = combo.getSelected();
        if pos==0:
            if Model:
                Model.setMaterialFlag(irr.video.EMF_BILINEAR_FILTER, False);
                Model.setMaterialFlag(irr.video.EMF_TRILINEAR_FILTER, False);
                Model.setMaterialFlag(irr.video.EMF_ANISOTROPIC_FILTER, False);

        elif pos==1:
            if Model:
                Model.setMaterialFlag(irr.video.EMF_BILINEAR_FILTER, True);
                Model.setMaterialFlag(irr.video.EMF_TRILINEAR_FILTER, False);

        elif pos==2:
            if Model:
                Model.setMaterialFlag(irr.video.EMF_BILINEAR_FILTER, False);
                Model.setMaterialFlag(irr.video.EMF_TRILINEAR_FILTER, True);

        elif pos==3:
            if Model:
                Model.setMaterialFlag(irr.video.EMF_ANISOTROPIC_FILTER, True);

        elif pos==4:
            if Model:
                Model.setMaterialFlag(irr.video.EMF_ANISOTROPIC_FILTER, False);


if __name__=="__main__":
    receiver=MyEventReceiver()
    Device = irr.createDevice(irr.video.EDT_OPENGL, 
            irr.core.dimension2du(800, 600), 16, False, False, False, receiver);

    if not Device:
        sys.exit(1)

    Device.setResizable(True);
    Device.setWindowCaption(u"Irrlicht Engine - Loading...");

    driver = Device.getVideoDriver();
    env = Device.getGUIEnvironment();
    smgr = Device.getSceneManager();
    smgr.getParameters().setAttribute(irr.scene.COLLADA_CREATE_SCENE_INSTANCES, True);

    driver.setTextureCreationFlag(irr.video.ETCF_ALWAYS_32_BIT, True);

    smgr.addLightSceneNode(None, 
            irr.core.vector3df(200,200,200),
            irr.video.SColorf(1.0,1.0,1.0),2000);
    smgr.setAmbientLight(irr.video.SColorf(0.3,0.3,0.3));
    Device.getFileSystem().addFolderFileArchive(MEDIA_PATH);


    xml = Device.getFileSystem().createXMLReader(u"config.xml");

    while xml and xml.read():
        nodeType=xml.getNodeType()
        if nodeType==irr.io.EXN_TEXT:
            MessageText = xml.getNodeData();
        elif nodeType==irr.io.EXN_ELEMENT:
            if (irr.core.stringw("startUpModel") == xml.getNodeName()):
                StartUpModelFile = xml.getAttributeValue(u"file");
            else:
                if (irr.core.stringw("messageText") == xml.getNodeName()):
                    Caption = xml.getAttributeValue(u"caption");

    if len(sys.argv) > 1:
        StartUpModelFile = sys.argv[1];

    skin = env.getSkin();
    font = env.getFont("fonthaettenschweiler.bmp");
    if font:
        skin.setFont(font);

    menu = env.addMenu();
    menu.addItem(u"File", -1, True, True);
    menu.addItem(u"View", -1, True, True);
    menu.addItem(u"Camera", -1, True, True);
    menu.addItem(u"Help", -1, True, True);

    submenu = menu.getSubMenu(0);
    submenu.addItem(u"Open Model File & Texture...", GUI_ID_OPEN_MODEL);
    submenu.addItem(u"Set Model Archive...", GUI_ID_SET_MODEL_ARCHIVE);
    submenu.addItem(u"Load as Octree", GUI_ID_LOAD_AS_OCTREE);
    submenu.addSeparator();
    submenu.addItem(u"Quit", GUI_ID_QUIT);

    submenu = menu.getSubMenu(1);
    submenu.addItem(u"sky box visible", GUI_ID_SKY_BOX_VISIBLE, True, False, True);
    submenu.addItem(u"toggle model debug information", GUI_ID_TOGGLE_DEBUG_INFO, True, True);
    submenu.addItem(u"model material", -1, True, True );

    submenu = submenu.getSubMenu(1);
    submenu.addItem(u"Off", GUI_ID_DEBUG_OFF);
    submenu.addItem(u"Bounding Box", GUI_ID_DEBUG_BOUNDING_BOX);
    submenu.addItem(u"Normals", GUI_ID_DEBUG_NORMALS);
    submenu.addItem(u"Skeleton", GUI_ID_DEBUG_SKELETON);
    submenu.addItem(u"Wire overlay", GUI_ID_DEBUG_WIRE_OVERLAY);
    submenu.addItem(u"Half-Transparent", GUI_ID_DEBUG_HALF_TRANSPARENT);
    submenu.addItem(u"Buffers bounding boxes", GUI_ID_DEBUG_BUFFERS_BOUNDING_BOXES);
    submenu.addItem(u"All", GUI_ID_DEBUG_ALL);

    submenu = menu.getSubMenu(1).getSubMenu(2);
    submenu.addItem(u"Solid", GUI_ID_MODEL_MATERIAL_SOLID);
    submenu.addItem(u"Transparent", GUI_ID_MODEL_MATERIAL_TRANSPARENT);
    submenu.addItem(u"Reflection", GUI_ID_MODEL_MATERIAL_REFLECTION);

    submenu = menu.getSubMenu(2);
    submenu.addItem(u"Maya Style", GUI_ID_CAMERA_MAYA);
    submenu.addItem(u"First Person", GUI_ID_CAMERA_FIRST_PERSON);

    submenu = menu.getSubMenu(3);
    submenu.addItem(u"About", GUI_ID_ABOUT);

    bar = env.addToolBar();

    image = driver.getTexture("open.png");
    bar.addButton(GUI_ID_BUTTON_OPEN_MODEL, u"", u"Open a model",image, None, False, True);

    image = driver.getTexture("tools.png");
    bar.addButton(GUI_ID_BUTTON_SHOW_TOOLBOX, u"", u"Open Toolset",image, None, False, True);

    image = driver.getTexture("zip.png");
    bar.addButton(GUI_ID_BUTTON_SELECT_ARCHIVE, u"", u"Set Model Archive",image, None, False, True);

    image = driver.getTexture("help.png");
    bar.addButton(GUI_ID_BUTTON_SHOW_ABOUT, u"", u"Open Help", image, None, False, True);

    box = env.addComboBox(irr.core.recti(250,4,350,23), bar, GUI_ID_TEXTUREFILTER);
    box.addItem(u"No filtering");
    box.addItem(u"Bilinear");
    box.addItem(u"Trilinear");
    box.addItem(u"Anisotropic");
    box.addItem(u"Isotropic");

    for i in range(irr.gui.EGDC_COUNT):
        col = env.getSkin().getColor(i);
        col.setAlpha(255);
        env.getSkin().setColor(i, col);

    createToolBox();

    fpstext = env.addStaticText(u"",
            irr.core.recti(400,4,570,23), True, False, bar);

    postext = env.addStaticText(u"",
            irr.core.recti(10,50,470,80),False, False, None, GUI_ID_POSITION_TEXT);
    postext.setVisible(False);

    Caption = " - [%s]" % driver.getName();
    Device.setWindowCaption(Caption);

    if len(sys.argv)==1:
        showAboutText();
    loadModel(StartUpModelFile);

    SkyBox = smgr.addSkyBoxSceneNode(
        driver.getTexture("irrlicht2_up.jpg"),
        driver.getTexture("irrlicht2_dn.jpg"),
        driver.getTexture("irrlicht2_lf.jpg"),
        driver.getTexture("irrlicht2_rt.jpg"),
        driver.getTexture("irrlicht2_ft.jpg"),
        driver.getTexture("irrlicht2_bk.jpg"));

    Camera[0] = smgr.addCameraSceneNodeMaya();
    Camera[0].setFarValue(20000.0);
    Camera[0].setTarget(irr.core.vector3df(0,30,0));

    Camera[1] = smgr.addCameraSceneNodeFPS();
    Camera[1].setFarValue(20000.0);
    Camera[1].setPosition(irr.core.vector3df(0,0,-70));
    Camera[1].setTarget(irr.core.vector3df(0,30,0));

    setActiveCamera(Camera[0]);

    img = env.addImage(driver.getTexture("irrlichtlogo2.png"),
            irr.core.position2di(10, driver.getScreenSize().Height - 128));

    img.setAlignment(irr.gui.EGUIA_UPPERLEFT, irr.gui.EGUIA_UPPERLEFT,
            irr.gui.EGUIA_LOWERRIGHT, irr.gui.EGUIA_LOWERRIGHT);

    while Device.run() and driver:
        if Device.isWindowActive():
            driver.beginScene(True, True, irr.video.SColor(150,50,50,50));

            smgr.drawAll();
            env.drawAll();

            driver.endScene();

            fpstext.setText(u"FPS: %d Tris: %d" % (
                driver.getFPS(),
                driver.getPrimitiveCountDrawn(),
                ));

            cam = Device.getSceneManager().getActiveCamera();
            postext.setText(u"Pos: %f %f %f Tgt: %f %f %f" % (
                    cam.getPosition().X,
                    cam.getPosition().Y,
                    cam.getPosition().Z,
                    cam.getTarget().X,
                    cam.getTarget().Y,
                    cam.getTarget().Z,
                    ));

            updateToolBox();
        else:
            Device._yield()

