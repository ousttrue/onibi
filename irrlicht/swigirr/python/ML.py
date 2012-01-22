import os
import sys
import struct
import irr

SIZE_FONT_NORMAL=12
SIZE_FONT_BIG=24

if os.name=='nt':
    FONTPATH1="C:/Windows/Fonts/arial.ttf"
    FONTPATH2="C:/Windows/Fonts/times.ttf"
    FONTPATH3="C:/Windows/Fonts/msgothic.ttc"
else:
    FONTPATH1="/usr/share/fonts/Truetype/freefont/FreeSans.ttf"
    FONTPATH2="/usr/share/fonts/Truetype/freefont/FreeSerif.ttf"
    FONTPATH3="/usr/share/fonts/Truetype/ttf-japanese-gothic.ttf"


Device=None;
lang = 0;
listbox = 0;
lstLang = 0;
txtTrans = 0;
txtLog = 0;
btnQuit = 0;
btnNew = 0;
btnFile = 0;
edtName = 0;
edtMemo = 0;

fonts=[None]*6
font=None
font2=None
skin=None;

# Japanese Texts
jtxtTrans = u"\u900f\u660e\u5ea6\u8a2d\u5b9a\u003a"
jtxtQuit = u"\u7d42\u308f\u308b"
jtxtNew = u"\u65b0\u898f\u30a6\u30a3\u30f3\u30c9\u30a6"
jtxtFile = u"\u30d5\u30a1\u30a4\u30eb\u3092\u958b\u304f"
jtxtLog = u"\u64cd\u4f5c\u30ed\u30b0"
jtxtTfont = u"\u900f\u904e\u30d5\u30a9\u30f3\u30c8"
jtxtHello = u"\u3053\u3093\u306b\u3061\u306f\u30c8\u30a5\u30eb\u30fc\u30bf\u30a4\u30d7"


def ChangeCaption(newlang):
    lang = newlang;
    if lang==0:
        txtTrans.setText(u"Transparency:");
        btnQuit.setText(u"Quit");
        btnNew.setText(u"New Window");
        btnFile.setText(u"Open File");
        txtLog.setText(u"Logging ListBox:");
    elif lang==1:
        txtTrans.setText(jtxtTrans);
        btnQuit.setText(jtxtQuit);
        btnNew.setText(jtxtNew);
        btnFile.setText(jtxtFile);
        txtLog.setText(jtxtLog);
    else:
        print "unknown lang %d" % newlang


class MyEventReceiver(irr.IEventReceiver):
    def __init__(self):
        irr.IEventReceiver.__init__(self)
        self.cnt = 0;

    def OnEvent(self, event):
        if event.EventType == irr.EET_GUI_EVENT:
            id = event.Info.GUIEvent.Caller.getID();
            env = Device.getGUIEnvironment();
            eventType=event.Info.GUIEvent.EventType
            if eventType== irr.EGET_SCROLL_BAR_CHANGED:
                if (id == 104):
                    pos = irr.gui.IGUIScrollBar.cast(event.Info.GUIEvent.Caller).getPos();
                    
                    for i in range(irr.gui.EGDC_COUNT):
                        col = env.getSkin().getColor(i);
                        col.setAlpha(pos);
                        env.getSkin().setColor(i, col);

            elif eventType== irr.EGET_BUTTON_CLICKED:
                if (id == 101):
                    Device.closeDevice();
                    return True;

                if (id == 102):
                    listbox.addItem(u"Window created");
                    self.cnt += 30;
                    if (self.cnt > 200):
                        self.cnt = 0;
                    window = env.addWindow(
                            irr.core.recti(100 + self.cnt, 100 + self.cnt, 300 + self.cnt, 200 + self.cnt), 
                            False,
                            u"Test window");

                    env.addStaticText(u"Please close me",  
                            irr.core.recti(35,35,140,50),
                            True, # border?
                            False, # wordwrap?
                            window);

                    return True;

                if (id == 103):
                    listbox.addItem(u"File open");
                    env.addFileOpenDialog(u"Please choose a file.");
                    return True;

            elif (eventType== irr.EGET_LISTBOX_CHANGED 
                    or eventType== irr.EGET_LISTBOX_SELECTED_AGAIN):
                if (id == 120):
                    sel = lstLang.getSelected();
                    font = fonts[sel * 2];
                    font2 = fonts[sel * 2 + 1];
                    skin.setFont(font);
                    if (sel == 2):
                        ChangeCaption(1);
                    else:
                        ChangeCaption(0);

        return False;


if __name__=="__main__":

    Device = irr.createDevice(irr.video.EDT_OPENGL, irr.core.dimension2du(640, 480));
    if not Device:
        sys.exit(1);

    Driver = Device.getVideoDriver();
    env = Device.getGUIEnvironment();
    Scene = Device.getSceneManager();

    Scene.addCameraSceneNode(None, irr.core.vector3df(0,10,-40), irr.core.vector3df(0,0,0));

    receiver=MyEventReceiver();
    Device.setEventReceiver(receiver);

    fonts[0] = env.getFont(FONTPATH1, SIZE_FONT_NORMAL);
    fonts[1] = env.getFont(FONTPATH1, SIZE_FONT_BIG);
    fonts[2] = env.getFont(FONTPATH2, SIZE_FONT_NORMAL);
    fonts[3] = env.getFont(FONTPATH2, SIZE_FONT_BIG);
    fonts[4] = env.getFont(FONTPATH3, SIZE_FONT_NORMAL);
    fonts[5] = env.getFont(FONTPATH3, SIZE_FONT_BIG);

    font = fonts[0];
    font2 = fonts[1];

    skin = env.getSkin();
    skin.setFont(font);

    txtTrans = env.addStaticText(u"Transparency:", irr.core.recti(50,20,250,40), True);
    scrollbar = env.addScrollBar(True, irr.core.recti(50, 45, 250, 60), None, 104);
    scrollbar.setMax(255);
    col = env.getSkin().getColor(0);
    scrollbar.setPos(col.getAlpha());

    txtLog = env.addStaticText(u"Logging ListBox:", irr.core.recti(50,80,250,100), True);
    listbox = env.addListBox(irr.core.recti(50, 110, 250, 180));

    btnQuit = env.addButton(irr.core.recti(10,210,100,240), None, 101, u"Quit");
    btnNew = env.addButton(irr.core.recti(10,250,100,290), None, 102, u"New Window");
    btnFile = env.addButton(irr.core.recti(10,300,100,340), None, 103, u"Open File");

    edtName = env.addEditBox(u"",irr.core.recti(300,60,580,80));
    edtName.setMax(40);
    edtMemo = env.addEditBox(u"",irr.core.recti(300,100,580,450));
    edtMemo.setMultiLine(True);
    edtMemo.setTextAlignment(irr.gui.EGUIA_UPPERLEFT, irr.gui.EGUIA_UPPERLEFT);

    lstLang = env.addListBox(irr.core.recti(10, 400, 250, 470),None,120);
    lstLang.addItem(u"Arial");
    lstLang.addItem(u"Times Roman");
    lstLang.addItem(u"MS-Gothic(Japanese)");
    lstLang.setSelected(0);

    lastFPS = -1;

    while Device.run():
        Driver.beginScene(True, True, 
                irr.video.SColor(0,64,64,128));

        Scene.drawAll();

        if lang==1:
            font2.draw(u"Hello TrueType",
                    irr.core.recti(250,20,640,100),
                    irr.video.SColor(255,255,64,64),True);
        else:
            font2.draw(jtxtHello,
                    irr.core.recti(250,20,640,100),
                    irr.video.SColor(255,255,64,64),True);

        env.drawAll();
        Driver.endScene();

        fps = Driver.getFPS();
        if (lastFPS != fps):
            Device.setWindowCaption(u"Irrlicht TrueType Demo (fps:%d)" % fps);
            lastFPS = fps;

