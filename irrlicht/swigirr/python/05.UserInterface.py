import sys
import irr

MEDIA_PATH='../../media'


GUI_ID_QUIT_BUTTON=101
GUI_ID_NEW_WINDOW_BUTTON=102
GUI_ID_FILE_OPEN_BUTTON=103
GUI_ID_TRANSPARENCY_SCROLL_BAR=104


class Context(object):
    def __init__(self, device, counter, listbox):
        self.device=device
        self.counter=counter
        self.listbox=listbox


class MyEventReceiver(irr.IEventReceiver):

    def __init__(self, context):
        irr.IEventReceiver.__init__(self)
        self.Context=context

    def OnEvent(self, _event):
        if _event.EventType == irr.EET_GUI_EVENT:
            event=_event.Info.GUIEvent
            id = event.Caller.getID();
            env = self.Context.device.getGUIEnvironment();
            
            if event.EventType==irr.EGET_SCROLL_BAR_CHANGED:
                if id == GUI_ID_TRANSPARENCY_SCROLL_BAR:
                    pos = irr.gui.IGUIScrollBar.cast(event.Caller).getPos();
                    for i in range(irr.gui.EGDC_COUNT):
                        col = env.getSkin().getColor(i);
                        col.setAlpha(pos);
                        env.getSkin().setColor(i, col);

            elif event.EventType==irr.EGET_BUTTON_CLICKED:
                if id==GUI_ID_QUIT_BUTTON:
                    self.Context.device.closeDevice();
                    return True;
                elif id==GUI_ID_NEW_WINDOW_BUTTON:
                    self.Context.listbox.addItem(u"Window created");
                    self.Context.counter += 30;
                    if self.Context.counter > 200:
                        self.Context.counter = 0;

                    window = env.addWindow(
                        irr.core.recti(
                            100 + self.Context.counter, 
                            100 + self.Context.counter, 
                            300 + self.Context.counter, 
                            200 + self.Context.counter),
                        False, # modal?
                        u"Test window");

                    env.addStaticText(u"Please close me",
                        irr.core.recti(35,35,140,50),
                        True, # border?
                        False, # wordwrap?
                        window);
                    return True;

                elif id== GUI_ID_FILE_OPEN_BUTTON:
                    self.Context.listbox.addItem(u"File open");
                    env.addFileOpenDialog(u"Please choose a file.");
                    return True;

                else:
                    return False;

        return False;


if __name__=="__main__":
    device = irr.createDevice(irr.video.EDT_OPENGL, irr.core.dimension2du(640, 480));
    if not device:
        sys.exit(1)

    device.setWindowCaption(u"Irrlicht Engine - User Interface Demo");
    device.setResizable(True);

    driver = device.getVideoDriver();
    env = device.getGUIEnvironment();

    skin = env.getSkin();
    font = env.getFont(MEDIA_PATH+"/fonthaettenschweiler.bmp");
    if font:
        skin.setFont(font);

    skin.setFont(env.getBuiltInFont(), irr.gui.EGDF_TOOLTIP);

    env.addButton(irr.core.recti(10,240,110,240 + 32), None, GUI_ID_QUIT_BUTTON,
            u"Quit", u"Exits Program");
    env.addButton(irr.core.recti(10,280,110,280 + 32), None, GUI_ID_NEW_WINDOW_BUTTON,
            u"New Window", u"Launches a new Window");
    env.addButton(irr.core.recti(10,320,110,320 + 32), None, GUI_ID_FILE_OPEN_BUTTON,
            u"File Open", u"Opens a file");

    env.addStaticText(u"Transparent Control:", irr.core.recti(150,20,350,40), True);
    scrollbar = env.addScrollBar(True,
            irr.core.recti(150, 45, 350, 60), None, GUI_ID_TRANSPARENCY_SCROLL_BAR);
    scrollbar.setMax(255);

    scrollbar.setPos(env.getSkin().getColor(irr.gui.EGDC_WINDOW).getAlpha());

    env.addStaticText(u"Logging ListBox:", irr.core.recti(50,110,250,130), True);
    listbox = env.addListBox(irr.core.recti(50, 140, 250, 210));
    env.addEditBox(u"Editable Text", irr.core.recti(350, 80, 550, 100));

    receiver=MyEventReceiver(Context(device, 0, listbox))

    device.setEventReceiver(receiver);

    env.addImage(driver.getTexture(MEDIA_PATH+"/irrlichtlogo2.png"),
            irr.core.position2di(10,10));

    while device.run():
        if device.isWindowActive():
            driver.beginScene(True, True, irr.video.SColor(0,200,200,200));
            env.drawAll();
            driver.endScene();

    sys.exit(0);

