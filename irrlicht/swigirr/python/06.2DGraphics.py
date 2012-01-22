import sys
import irr

MEDIA_PATH='../../../irrlicht/media'

if __name__=="__main__":
    device = irr.createDevice(irr.video.EDT_OPENGL, irr.core.dimension2du(512, 384));

    if not device:
        sys.exit(1)

    device.setWindowCaption(u"Irrlicht Engine - 2D Graphics Demo");

    driver = device.getVideoDriver();

    images = driver.getTexture(MEDIA_PATH+"/2ddemo.png");
    driver.makeColorKeyTexture(images, irr.core.position2di(0,0));

    font = device.getGUIEnvironment().getBuiltInFont();
    font2 = device.getGUIEnvironment().getFont(MEDIA_PATH+"/fonthaettenschweiler.bmp");

    imp1=irr.core.recti(349,15,385,78);
    imp2=irr.core.recti(387,15,423,78);

    driver.getMaterial2D().getTextureLayer(0).BilinearFilter=True;
    driver.getMaterial2D().AntiAliasing=irr.video.EAAM_FULL_BASIC;

    while device.run():
        if device.isWindowActive():
            time = device.getTimer().getTime();

            driver.beginScene(True, True, irr.video.SColor(255,120,102,136));

            driver.draw2DImage(images, irr.core.position2di(50,50),
                    irr.core.recti(0,0,342,224), None,
                    irr.video.SColor(255,255,255,255), True);

            driver.draw2DImage(images, irr.core.position2di(164,125),
                    (time/500 % 2) and imp1 or imp2, None,
                    irr.video.SColor(255,255,255,255), True);

            driver.draw2DImage(images, irr.core.position2di(270,105),
                    (time/500 % 2) and imp1 or imp2, None,
                    irr.video.SColor(255,(time) % 255,255,255), True);

            if font:
                font.draw(
                        u"This demo shows that Irrlicht is also capable of drawing 2D graphics.",
                        irr.core.recti(130,10,300,50),
                        irr.video.SColor(255,255,255,255));

            if font2:
                font2.draw(u"Also mixing with 3d graphics is possible.",
                    irr.core.recti(130,20,300,60),
                    irr.video.SColor(255,time % 255,time % 255,255));

            driver.enableMaterial2D();
            driver.draw2DImage(images, irr.core.recti(10,10,108,48),
                    irr.core.recti(354,87,442,118));
            driver.enableMaterial2D(False);

            m = device.getCursorControl().getPosition();
            driver.draw2DRectangle(irr.video.SColor(100,255,255,255),
                    irr.core.recti(m.X-20, m.Y-20, m.X+20, m.Y+20));

            driver.endScene();

    sys.exit(0);

