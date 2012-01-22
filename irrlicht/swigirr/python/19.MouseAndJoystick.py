import os
import sys
import irr


class SMouseState(object):
    def __init__(self):
        self.Position=irr.core.position2di();
        self.LeftButtonDown=False;


class MyEventReceiver(irr.IEventReceiver):
    def __init__(self):
        irr.IEventReceiver.__init__(self)
        self.MouseState=SMouseState()
        self.JoystickState=None

    def OnEvent(self, event):
        if (event.EventType == irr.EET_MOUSE_INPUT_EVENT):
            mouseEvent=event.Info.MouseInput.Event
            if mouseEvent== irr.EMIE_LMOUSE_PRESSED_DOWN:
                self.MouseState.LeftButtonDown = True;

            elif mouseEvent== irr.EMIE_LMOUSE_LEFT_UP:
                self.MouseState.LeftButtonDown = False;

            elif mouseEvent== irr.EMIE_MOUSE_MOVED:
                self.MouseState.Position.X = event.Info.MouseInput.X;
                self.MouseState.Position.Y = event.Info.MouseInput.Y;

        if (event.EventType == irr.EET_JOYSTICK_INPUT_EVENT
                and event.Info.JoystickEvent.Joystick == 0):
            self.JoystickState = event.Info.JoystickEvent;

        return False;

    def GetJoystickState(self):
        return self.JoystickState;

    def GetMouseState(self):
        return self.MouseState;


if __name__=="__main__":
    receiver=MyEventReceiver()

    device = irr.createDevice(irr.video.EDT_OPENGL,
            irr.core.dimension2du(640, 480), 16, False, False, False, receiver);

    if not device:
        sys.exit(1)

    joystickInfo=device.activateJoysticks()
    if len(joystickInfo)>0:
        print "Joystick support is enabled and %d joystick(s) are present." % len(joystickInfo);

        for i, joystick in enumerate(joystickInfo):
            print ("Joystick %d:"
                    "\tName: '%s'"
                    "\tAxes: %d"
                    "\tButtons: %d"
                    "\tHat is: " % (i, joystick.Name, joystick.Axes, joystick.Buttons))

            povHat=joystick.PovHat
            if povHat== irr.POV_HAT_PRESENT:
                print "present"

            elif povHat== irr.POV_HAT_ABSENT:
                print "absent"

            else:
                print "unknown"
    else:
        print "Joystick support is not enabled."

    device.setWindowCaption(
            u"Irrlicht Joystick Example (%d) joysticks)" % len(joystickInfo));

    driver = device.getVideoDriver();
    smgr = device.getSceneManager();

    node = smgr.addMeshSceneNode(
            smgr.addArrowMesh( "Arrow",
                irr.video.SColor(255, 255, 0, 0),
                irr.video.SColor(255, 0, 255, 0),
                16,16,
                2.0, 1.3,
                0.1, 0.6
                )
            );
    node.setMaterialFlag(irr.video.EMF_LIGHTING, False);

    camera = smgr.addCameraSceneNode();
    camera.setPosition(irr.core.vector3df(0, 0, -10));

    then = device.getTimer().getTime();
    MOVEMENT_SPEED = 5.0;

    while(device.run()):
        now = device.getTimer().getTime();
        frameDeltaTime = (now - then) / 1000.0;
        then = now;

        movedWithJoystick = False;
        nodePosition = node.getPosition();

        if(len(joystickInfo) > 0):
            moveHorizontal = 0.0;
            moveVertical = 0.0;

            joystickData = receiver.GetJoystickState();

            DEAD_ZONE = 0.05;

            moveHorizontal = joystickData.getAxis(irr.SJoystickEvent.AXIS_X) / 32767.0;
            if(abs(moveHorizontal) < DEAD_ZONE):
                moveHorizontal = 0.0;

            moveVertical = joystickData.getAxis(irr.SJoystickEvent.AXIS_Y) / -32767.0;
            if(abs(moveVertical) < DEAD_ZONE):
                moveVertical = 0.0;

            povDegrees = joystickData.POV / 100;
            if(povDegrees < 360):
                if(povDegrees > 0 and povDegrees < 180):
                    moveHorizontal = 1.0;
                elif(povDegrees > 180):
                    moveHorizontal = -1.0;

                if(povDegrees > 90 and povDegrees < 270):
                    moveVertical = -1.0;
                elif(povDegrees > 270 or povDegrees < 90):
                    moveVertical = +1.0;
                    
            if(not irr.core.equals(moveHorizontal, 0.0) 
                    or not irr.core.equals(moveVertical, 0.0)):
                nodePosition.X += MOVEMENT_SPEED * frameDeltaTime * moveHorizontal;
                nodePosition.Y += MOVEMENT_SPEED * frameDeltaTime * moveVertical;
                movedWithJoystick = True;

        if(not movedWithJoystick):
            ray = smgr.getSceneCollisionManager().getRayFromScreenCoordinates(
                receiver.GetMouseState().Position, camera);

            plane=irr.core.plane3df(nodePosition, irr.core.vector3df(0, 0, -1));
            mousePosition=irr.core.vector3df();
            if(plane.getIntersectionWithLine(ray.start, ray.getVector(), mousePosition)):
                toMousePosition=mousePosition - nodePosition;
                availableMovement = MOVEMENT_SPEED * frameDeltaTime;

                if(toMousePosition.getLength() <= availableMovement):
                    nodePosition = mousePosition;
                else:
                    nodePosition += toMousePosition.normalize() * availableMovement;

        node.setPosition(nodePosition);

        node.setMaterialFlag(irr.video.EMF_LIGHTING, receiver.GetMouseState().LeftButtonDown);

        driver.beginScene(True, True, irr.video.SColor(255,113,113,133));
        smgr.drawAll();
        driver.endScene();

