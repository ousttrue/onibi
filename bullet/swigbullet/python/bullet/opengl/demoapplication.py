import sys
import math
import abc
import bullet
from . import vector3


class DemoApplication(object):
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self.m_profileIterator=bullet.CProfileManager.Get_Iterator()
        self.m_clock=bullet.btClock()
        # this is the most important class
        self.m_dynamicsWorld=None
        # constraint for mouse picking
        self.m_pickConstraint=None;
        self.m_shootBoxShape=None;
        self.m_cameraDistance=15.0;
        self.m_debugMode=0;
        self.m_ele=20.0;
        self.m_azi=0;
        self.m_cameraPosition=(0, 0, 0);
        #look at
        self.m_cameraTargetPosition=(0, 0, 0);
        self.m_mouseOldX=0;
        self.m_mouseOldY=0;
        self.m_mouseButtons=0;
        self.m_alt_key=False
        self.m_ctrl_key=False
        self.m_shift_key=False
        self.m_scaleBottom=0.5;
        self.m_scaleFactor=2.0;
        self.m_cameraUp=(0, 1, 0);
        self.m_forwardAxis=2;
        self.m_zoomStepSize=0.4;
        self.m_glutScreenWidth=0;
        self.m_glutScreenHeight=0;
        self.m_frustumZNear=1.0;
        self.m_frustumZFar=10000.0;
        self.m_ortho=0;
        self.m_ShootBoxInitialSpeed=40.0;
        self.m_stepping=True;
        self.m_singleStep=False;
        self.m_idle=False;
        self.m_lastKey=0;
        self.m_enableshadows=False;
        self.m_sundirection=(1*1000, -2*1000, 1*1000)
        self.m_defaultContactProcessingThreshold=bullet.BT_LARGE_FLOAT;
        self.m_use6Dof = False;
        self.m_oldPickingDist  = 0.0;
        self.m_keep=[]

    def displayProfileString(self, xOffset, yStart, message):
        pass

    def removePickingConstraint(self):
        if (self.m_pickConstraint and self.m_dynamicsWorld):
            self.m_dynamicsWorld.removeConstraint(self.m_pickConstraint);
            self.m_pickConstraint = None
            self.pickedBody.forceActivationState(bullet.ACTIVE_TAG);
            self.pickedBody.setDeactivationTime(0.0);
            self.pickedBody = None;

    def showProfileInfo(self, xOffset, yStart, yIncr):
        time_since_reset = 0.0;
        if (not self.m_idle):
            time_since_reset = bullet.CProfileManager.Get_Time_Since_Reset();

        # recompute profiling data, and store profile strings
        totalTime = 0;
        frames_since_reset = bullet.CProfileManager.Get_Frame_Count_Since_Reset();
        self.m_profileIterator.First();

        parent_time = (self.m_profileIterator.Is_Root() 
                and time_since_reset 
                or self.m_profileIterator.Get_Current_Parent_Total_Time());

        self.displayProfileString(xOffset,yStart,
                "--- Profiling: %s (total running time: %.3f ms) ---" % (
                    self.m_profileIterator.Get_Current_Parent_Name(), 
                    parent_time)
                );
        yStart += yIncr;

        self.displayProfileString(xOffset,yStart,
                "press (1,2...) to display child timings, or 0 for parent");
        yStart += yIncr;

        accumulated_time = 0.0;
        i=1
        while not self.m_profileIterator.Is_Done():
            current_total_time = self.m_profileIterator.Get_Current_Total_Time();
            accumulated_time += current_total_time;
            fraction = (parent_time > bullet.SIMD_EPSILON 
                    and (current_total_time / parent_time) * 100 
                    or 0.0);

            self.displayProfileString(xOffset,yStart,"%d -- %s (%.2f %%) . %.3f ms / frame (%d calls)" % (
                i, self.m_profileIterator.Get_Current_Name(), fraction,
                (current_total_time / float(frames_since_reset)),
                self.m_profileIterator.Get_Current_Total_Calls()));
            yStart += yIncr;
            totalTime += current_total_time;
            self.m_profileIterator.Next()
            i+=1

        # (min(0, time_since_reset - totalTime) / time_since_reset) * 100);
        self.displayProfileString(xOffset,yStart,"%s (%.3f %%) . %.3f ms" % ("Unaccounted",
            (parent_time > bullet.SIMD_EPSILON 
                and ((parent_time - accumulated_time) / parent_time) * 100 
                or 0.0), 
            parent_time - accumulated_time)
            );
        yStart += yIncr;

        self.displayProfileString(xOffset,yStart,"-------------------------------------------------");
        yStart += yIncr;

    def renderscene(self, renderpass):
        pass

    def	getDynamicsWorld(self):
        return self.m_dynamicsWorld;

    @abc.abstractmethod
    def initPhysics(self):
        assert(False)

    def setDrawClusters(self, drawClusters):
        pass

    def setOrthographicProjection(self):
        pass

    def resetPerspectiveProjection(self):
        pass

    def	setTexturing(self, enable):
        pass

    def	getTexturing(self):
        pass

    def	setShadows(self, enable):
        p=self.m_enableshadows;
        self.m_enableshadows=enable;
        return p;

    def	getShadows(self):
        return self.m_enableshadows;

    def getDebugMode(self):
        return self.m_debugMode ;

    def	setDebugMode(self, mode):
        self.m_debugMode = mode;
        if (self.getDynamicsWorld() and self.getDynamicsWorld().getDebugDrawer()):
            self.getDynamicsWorld().getDebugDrawer().setDebugMode(mode);

    def	setAzi(self, azi):
        self.m_azi = azi;

    def	setCameraUp(self, camUp):
        self.m_cameraUp = camUp;

    def	setCameraForwardAxis(self, axis):
        self.m_forwardAxis = axis;

    def myinit(self):
        print 'myinit'

    def toggleIdle(self):
        if (self.m_idle):
            self.m_idle = False;
        else:
            self.m_idle = True;

    def updateCamera(self):
        rele = self.m_ele * 0.01745329251994329547;# rads per deg
        razi = self.m_azi * 0.01745329251994329547;# rads per deg

        rot=bullet.btQuaternion(self.m_cameraUp, razi);

        eyePos=[0, 0, 0];
        eyePos[self.m_forwardAxis] = -self.m_cameraDistance;
        eyePos=tuple(eyePos)

        forward=(eyePos[0], eyePos[1], eyePos[2]);
        if (vector3.length2(forward) < bullet.SIMD_EPSILON):
            forward=(1.0, 0.0, 0.0);

        right = vector3.cross(self.m_cameraUp, forward);
        roll=bullet.btQuaternion(right,-rele);

        m=bullet.btMatrix3x3(rot) * bullet.btMatrix3x3(roll)
        eyePos =m.apply(eyePos);

        self.m_cameraPosition=vector3.add(eyePos, self.m_cameraTargetPosition);

        if (self.m_glutScreenWidth == 0 and self.m_glutScreenHeight == 0):
            return;

        aspect = float(self.m_glutScreenWidth) / float(self.m_glutScreenHeight);
        assert(aspect!=0.0)

        extents=(aspect * 1.0, 1.0, 0.0);


        if (self.m_ortho):
            # reset matrix

            extents *= self.m_cameraDistance;
            lower = self.m_cameraTargetPosition - extents;
            upper = self.m_cameraTargetPosition + extents;

        else:
            pass

    def	getCameraPosition(self):
        return self.m_cameraPosition;

    def	getCameraTargetPosition(self):
        return self.m_cameraTargetPosition;

    def	getDeltaTimeMicroseconds(self):
        dt = self.m_clock.getTimeMicroseconds();
        self.m_clock.reset();
        return dt;

    def setFrustumZPlanes(self, zNear, zFar):
        self.m_frustumZNear = zNear;
        self.m_frustumZFar = zFar;

    # glut callbacks
    def	getCameraDistance(self):
        return self.m_cameraDistance;

    def	setCameraDistance(self, dist):
        self.m_cameraDistance  = dist;

    def	moveAndDisplay(self):
        if (not self.m_idle):
            self.clientMoveAndDisplay();
        else:
            self.displayCallback();

    @abc.abstractmethod
    def clientMoveAndDisplay(self):
        assert(False)

    def clientResetScene(self):
        self.removePickingConstraint();

        numObjects = 0;
        i=0;

        if (self.m_dynamicsWorld):
            numConstraints = self.m_dynamicsWorld.getNumConstraints();
            for i in range(numConstraints):
                self.m_dynamicsWorld.getConstraint(0).setEnabled(True);
            numObjects = m_dynamicsWorld.getNumCollisionObjects();

            # create a copy of the array, not a reference!
            for i, colObj in enumerate(self.m_dynamicsWorld.getCollisionObjectArray()):
                body = btRigidBody.upcast(colObj);
                if (body):
                    if (body.getMotionState()):
                        myMotionState = bullet.btDefaultMotionState.downcast(body.getMotionState());
                        myMotionState.m_graphicsWorldTrans = myMotionState.m_startWorldTrans;
                        body.setCenterOfMassTransform(myMotionState.m_graphicsWorldTrans);
                        colObj.setInterpolationWorldTransform( myMotionState.m_startWorldTrans );
                        colObj.forceActivationState(bullet.ACTIVE_TAG);
                        colObj.activate();
                        colObj.setDeactivationTime(0);
                    # removed cached contact points
                    # (this is not necessary if all objects have been removed from the dynamics world)
                    if (self.m_dynamicsWorld.getBroadphase().getOverlappingPairCache()):
                        self.m_dynamicsWorld.getBroadphase().getOverlappingPairCache().cleanProxyFromPairs(
                                colObj.getBroadphaseHandle(),self.getDynamicsWorld().getDispatcher());

                    body = bullet.btRigidBody.upcast(colObj);
                    if (body and not body.isStaticObject()):
                        bullet.btRigidBody.upcast(colObj).setLinearVelocity((0,0,0));
                        bullet.btRigidBody.upcast(colObj).setAngularVelocity((0,0,0));

            # reset some internal cached data in the broadphase
            self.m_dynamicsWorld.getBroadphase().resetPool(self.getDynamicsWorld().getDispatcher());
            self.m_dynamicsWorld.getConstraintSolver().reset();


    # Demo functions
    def setShootBoxShape(self):
        if self.m_shootBoxShape:
            return
        box = bullet.btBoxShape((0.5,0.5,0.5));
        box.initializePolyhedralFeatures();
        self.m_shootBoxShape = box;

    def	shootBox(self, destination):
        if not self.m_dynamicsWorld:
            return
        print 'shootBox'
        mass = 1.0;
        startTransform=bullet.btTransform();
        startTransform.setIdentity();
        camPos = self.getCameraPosition();
        startTransform.setOrigin(camPos);

        self.setShootBoxShape ();

        body = self.localCreateRigidBody(mass, startTransform, self.m_shootBoxShape);
        body.setLinearFactor((1,1,1));

        linVel= vector3.normalize(
                (destination[0]-camPos[0],destination[1]-camPos[1],destination[2]-camPos[2]));
        linVel=vector3.mul(linVel, self.m_ShootBoxInitialSpeed);

        body.getWorldTransform().setOrigin(camPos);
        body.getWorldTransform().setRotation(bullet.btQuaternion(0,0,0,1));
        body.setLinearVelocity(linVel);
        body.setAngularVelocity((0,0,0));
        body.setCcdMotionThreshold(0.5);
        body.setCcdSweptSphereRadius(0.9);

    def	getRayTo(self, x, y):
        if (self.m_ortho):

            aspect = m_glutScreenWidth / m_glutScreenHeight;
            extents=(aspect * 1.0, 1.0, 0.0);

            extents *= m_cameraDistance;
            lower = self.m_cameraTargetPosition - extents;
            upper = self.m_cameraTargetPosition + extents;

            u = x / self.m_glutScreenWidth;
            v = (self.m_glutScreenHeight - y) / self.m_glutScreenHeight;

            p=(0,0,0);
            p.setValue(
                    (1.0 - u) * lower.getX() + u * upper.getX(),
                    (1.0 - v) * lower.getY() + v * upper.getY(),
                    m_cameraTargetPosition.getZ());
            return p;

        top = 1.0;
        bottom = -1.0;
        nearPlane = 1.0;
        tanFov = (top-bottom)*0.50 / nearPlane;
        fov = 2.0 * bullet.btAtan(tanFov);

        rayFrom = self.getCameraPosition();
        rayForward = vector3.normalize(
                vector3.sub(self.getCameraTargetPosition(), self.getCameraPosition()));
        farPlane = 10000.0;
        rayForward= vector3.mul(rayForward, farPlane);

        vertical = self.m_cameraUp;

        hor = vector3.normalize(vector3.cross(rayForward, vertical));
        vertical = vector3.normalize(vector3.cross(hor, rayForward));

        tanfov = math.tan(0.5*fov);


        hor = vector3.mul(hor, 2.0 * farPlane * tanfov);
        vertical = vector3.mul(vertical, 2.0 * farPlane * tanfov);

        aspect = float(self.m_glutScreenWidth) / float(self.m_glutScreenHeight);

        hor=vector3.mul(hor, aspect);

        rayToCenter = vector3.add(rayFrom, rayForward);
        dHor = vector3.mul(hor, (1.0/float(self.m_glutScreenWidth)));
        dVert = vector3.mul(vertical, (1.0/float(self.m_glutScreenHeight)));

        rayTo = vector3.add(
                vector3.sub(rayToCenter, 
                    vector3.mul(hor, 0.5)), 
                vector3.mul(vertical, 0.5));
        rayTo = vector3.add(rayTo, vector3.mul(dHor, x));
        rayTo = vector3.sub(rayTo, vector3.mul(dVert, y));
        return rayTo;

    def	localCreateRigidBody(self, mass, startTransform, shape):
        assert((not shape or shape.getShapeType() != bullet.INVALID_SHAPE_PROXYTYPE));

        # rigidbody is dynamic if and only if mass is non zero, otherwise static
        isDynamic = (mass != 0.0);

        localInertia=(0,0,0);
        if (isDynamic):
            shape.calculateLocalInertia(mass,localInertia);

        # using motionstate is recommended,
        # it provides interpolation capabilities,
        # and only synchronizes 'active' objects

        myMotionState = bullet.btDefaultMotionState(startTransform);

        cInfo=bullet.btRigidBodyConstructionInfo (mass,myMotionState,shape,localInertia);

        body = bullet.btRigidBody(cInfo);
        body.setContactProcessingThreshold(self.m_defaultContactProcessingThreshold);

        self.m_dynamicsWorld.addRigidBody(body);

        self.m_keep.append((myMotionState, cInfo, body, shape))

        return body;

    # callback methods by glut	
    def keyboardCallback(self, key, x, y):
        m_lastKey = 0;

        if (key >= 0x31 and key <= 0x39):
            child = key-0x31;
            self.m_profileIterator.Enter_Child(child);

        if (key==0x30):
            self.m_profileIterator.Enter_Parent();

        if key== 'q' :
            sys.exit(0);

        elif key=='l' :
            self.stepLeft();
        elif key=='r' :
            self.stepRight();
        elif key=='f' :
            self.stepFront();
        elif key=='b' :
            self.stepBack();
        elif key=='z' :
            self.zoomIn();
        elif key=='x' :
            self.zoomOut();
        elif key=='i' :
            self.toggleIdle();
        elif key=='g' :
            self.m_enableshadows= not self.m_enableshadows;
        elif key=='h':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_NoHelpText):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_NoHelpText);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_NoHelpText;

        elif key=='w':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DrawWireframe):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DrawWireframe);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DrawWireframe;

        elif key=='p':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_ProfileTimings):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_ProfileTimings);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_ProfileTimings;

        elif key=='=':
            maxSerializeBufferSize = 1024*1024*5;
            serializer = btDefaultSerializer(maxSerializeBufferSize);
            # serializer.setSerializationFlags(BT_SERIALIZE_NO_DUPLICATE_ASSERT);
            m_dynamicsWorld.serialize(serializer);
            f2 = open("testFile.bullet","wb");
            f2.write(serializer.getBufferPointer(),serializer.getCurrentBufferSize(),1,f2);
            f2.close();

        elif key=='m':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_EnableSatComparison):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_EnableSatComparison);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_EnableSatComparison;

        elif key=='n':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DisableBulletLCP):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DisableBulletLCP);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DisableBulletLCP;

        elif key=='t' :
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DrawText):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DrawText);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DrawText;

        elif key=='y':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DrawFeaturesText):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DrawFeaturesText);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DrawFeaturesText;

        elif key=='a':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DrawAabb):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DrawAabb);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DrawAabb;

        elif key=='c' :
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DrawContactPoints):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DrawContactPoints);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DrawContactPoints;

        elif key=='C' :
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DrawConstraints):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DrawConstraints);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DrawConstraints;

        elif key=='L' :
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_DrawConstraintLimits):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_DrawConstraintLimits);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_DrawConstraintLimits;

        elif key=='d' :
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_NoDeactivation):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_NoDeactivation);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_NoDeactivation;
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_NoDeactivation):
                gDisableDeactivation = true;
            else:
                gDisableDeactivation = false;

        elif key=='o' :
                m_ortho = not m_ortho; # m_stepping = !m_stepping;

        elif key=='s' :
            clientMoveAndDisplay();

        # elif key==' ' : newRandom(); break;

        elif key==' ':
            clientResetScene();

        elif key=='1':
            if (self.m_debugMode & bullet.btIDebugDraw.DBG_EnableCCD):
                self.m_debugMode = self.m_debugMode & (~bullet.btIDebugDraw.DBG_EnableCCD);
            else:
                self.m_debugMode |= bullet.btIDebugDraw.DBG_EnableCCD;

        elif key=='.':
            self.shootBox(self.getRayTo(x,y)); # getCameraTargetPosition());

        elif key=='+':
            m_ShootBoxInitialSpeed += 10.0;

        elif key=='-':
            m_ShootBoxInitialSpeed -= 10.0;

        else:
            # std.cout << "unused key : " << key << std.endl;
            pass

        if (self.getDynamicsWorld() and self.getDynamicsWorld().getDebugDrawer()):
            self.getDynamicsWorld().getDebugDrawer().setDebugMode(self.m_debugMode);

    def keyboardUpCallback(self, key, x, y):
        pass

    def specialKeyboard(self, key, x, y):
        pass

    def specialKeyboardUp(self, key, x, y):
        pass

    def reshape(self, w, h):
        print('reshape', w, h)
        self.myinit()

        self.m_glutScreenWidth = w;
        self.m_glutScreenHeight = h;

        self.updateCamera();

    def mouseFunc(self, button, state, x, y):
        print('mouseFunc', button, state, x, y)
        if (state == 0):
            self.m_mouseButtons |= 1<<button;
        else:
            self.m_mouseButtons = 0;

        self.m_mouseOldX = x;
        self.m_mouseOldY = y;

        self.updateModifierKeys();
        if ((self.m_alt_key) and (state==0)):
            return;

        rayTo = self.getRayTo(x,y);
        print 'rayTo', rayTo

        if button==2:
            if (state==0):
                self.shootBox(rayTo);

        elif button== 1:
            if (state==0):
                pass

        elif button== 0:
            if (state==0):
                # add a point to point constraint for picking
                if not self.m_dynamicsWorld:
                    self.removePickingConstraint();
                else:
                    print 'picking'
                    if (self.m_ortho):
                        rayFrom = (rayTo[0], rayTo[1], -100.0);
                    else:
                        rayFrom = self.m_cameraPosition;
                    rayCallback=bullet.ClosestRayResultCallback(rayFrom, rayTo);
                    self.m_dynamicsWorld.rayTest(rayFrom, rayTo, rayCallback);
                    if (rayCallback.hasHit()):
                        body = bullet.btRigidBody.upcast(rayCallback.m_collisionObject);
                        if (body):
                            print 'hit'
                            # other exclusions?
                            if (not (body.isStaticObject() or body.isKinematicObject())):
                                print body
                                self.pickedBody = body;
                                self.pickedBody.setActivationState(bullet.DISABLE_DEACTIVATION);
                                #pickPos = rayCallback.m_hitPointWorld;
                                pickPos = rayCallback.m_hitPointWorld
                                # printf("pickPos=%f,%f,%f\n",pickPos.getX(),pickPos.getY(),pickPos.getZ());
                                localPivot = body.getCenterOfMassTransform().inverse().apply(pickPos);

                                self.m_keep.append(self.m_pickConstraint)
                                if (self.m_use6Dof):
                                    print 'm_use6Dof'
                                    tr=bullet.btTransform();
                                    tr.setIdentity();
                                    tr.setOrigin(localPivot);
                                    dof6 = bullet.btGeneric6DofConstraint(body, tr, False);
                                    dof6.setLinearLowerLimit((0,0,0));
                                    dof6.setLinearUpperLimit((0,0,0));
                                    dof6.setAngularLowerLimit((0,0,0));
                                    dof6.setAngularUpperLimit((0,0,0));

                                    self.m_dynamicsWorld.addConstraint(dof6);
                                    self.m_pickConstraint = dof6;

                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_CFM,0.8,0);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_CFM,0.8,1);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_CFM,0.8,2);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_CFM,0.8,3);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_CFM,0.8,4);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_CFM,0.8,5);

                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_ERP,0.1,0);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_ERP,0.1,1);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_ERP,0.1,2);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_ERP,0.1,3);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_ERP,0.1,4);
                                    dof6.setParam(bullet.BT_CONSTRAINT_STOP_ERP,0.1,5);
                                else:
                                    print 'not m_use6Dof'
                                    p2p = bullet.btPoint2PointConstraint(body,localPivot);
                                    self.m_dynamicsWorld.addConstraint(p2p);
                                    self.m_pickConstraint = p2p;
                                    p2p.m_setting.m_impulseClamp = 30.0;
                                    # very weak constraint for picking
                                    p2p.m_setting.m_tau = 0.001;

                                self.m_use6Dof = not self.m_use6Dof;

                                # save mouse position for dragging
                                self.gOldPickingPos = rayTo;
                                self.gHitPos = pickPos;

                                self.m_oldPickingDist  = vector3.length(
                                        vector3.sub(pickPos, rayFrom));
                                print 'end'


    def	mouseMotionFunc(self, x, y):
        if (self.m_pickConstraint):
            # move the constraint pivot

            if (self.m_pickConstraint.getConstraintType() == bullet.D6_CONSTRAINT_TYPE):
                print 'bullet.D6_CONSTRAINT_TYPE'
                pickCon = bullet.btGeneric6DofConstraint.downcast(self.m_pickConstraint);
                if (pickCon):
                    # keep it at the same picking distance
                    newRayTo = self.getRayTo(x,y);
                    oldPivotInB = pickCon.getFrameOffsetA().getOrigin();

                    if (self.m_ortho):
                        newPivotB = oldPivotInB;
                        newPivotB.setX(newRayTo.getX());
                        newPivotB.setY(newRayTo.getY());
                    else:
                        rayFrom = self.m_cameraPosition;
                        dir = vector3.normalize(
                                vector3.sub(newRayTo, rayFrom));
                        dir = vector3.mul(dir, self.m_oldPickingDist);

                        newPivotB = vector3.add(rayFrom, dir);
                    pickCon.getFrameOffsetA().setOrigin(newPivotB);
            else:
                print 'other'
                pickCon = bullet.btPoint2PointConstraint.downcast(self.m_pickConstraint);
                if (pickCon):
                    # keep it at the same picking distance
                    newRayTo = self.getRayTo(x,y);
                    oldPivotInB = pickCon.getPivotInB();
                    if (self.m_ortho):
                        newPivotB = oldPivotInB;
                        newPivotB.setX(newRayTo.getX());
                        newPivotB.setY(newRayTo.getY());
                    else:
                        rayFrom = self.m_cameraPosition;
                        dir = vector3.normalize(vector3.sub(newRayTo, rayFrom));
                        dir = vector3.mul(dir, self.m_oldPickingDist);

                        newPivotB = vector3.add(rayFrom, dir);
                    pickCon.setPivotB(newPivotB);

        dx = x - self.m_mouseOldX;
        dy = y - self.m_mouseOldY;
        print dx, dy

        # only if ALT key is pressed (Maya style)
        if (self.m_alt_key):
            if(self.m_mouseButtons & 2):
                hor = vector3.sub(self.getRayTo(0,0), self.getRayTo(1,0));
                vert = vector3.sub(self.getRayTo(0,0), self.getRayTo(0,1));
                multiplierX = 0.001;
                multiplierY = 0.001;
                if (self.m_ortho):
                    multiplierX = 1;
                    multiplierY = 1;

                self.m_cameraTargetPosition = vector3.add(
                        self.m_cameraTargetPosition, 
                        vector3.mul(hor, dx * multiplierX));
                self.m_cameraTargetPosition = vector3.add(
                        self.m_cameraTargetPosition, 
                        vector3.mul(vert, dy * multiplierY));

            if(self.m_mouseButtons & (2 << 2) and self.m_mouseButtons & 1):
                pass
            elif(self.m_mouseButtons & 1):
                self.m_azi += dx * 0.2;
                self.m_azi = math.fmod(self.m_azi, 360.0);
                self.m_ele += dy * 0.2;
                self.m_ele = math.fmod(self.m_ele, 180.0);
            elif(self.m_mouseButtons & 4):
                self.m_cameraDistance -= dy * 0.020;
                if (self.m_cameraDistance<0.1):
                    self.m_cameraDistance = 0.1;

        self.m_mouseOldX = x;
        self.m_mouseOldY = y;
        self.updateCamera();

    def displayCallback(self):
        pass

    def renderme(self):
        pass

    @abc.abstractmethod
    def swapBuffers(self):
        assert(False)

    @abc.abstractmethod
    def	updateModifierKeys(self):
        assert(False)

    def stepLeft(self):
        global STEPSIZE
        self.m_azi -= STEPSIZE;
        if (self.m_azi < 0):
            self.m_azi += 360;
        self.updateCamera();

    def stepRight(self):
        self.m_azi += STEPSIZE;
        if (self.m_azi >= 360):
            self.m_azi -= 360;
        self.updateCamera();

    def stepFront(self):
        self.m_ele += STEPSIZE;
        if (self.m_ele >= 360):
            self.m_ele -= 360;
        self.updateCamera();

    def stepBack(self):
        self.m_ele -= STEPSIZE;
        if (self.m_ele < 0):
            self.m_ele += 360;
        self.updateCamera();

    def zoomIn(self):
        m_cameraDistance -= btScalar(m_zoomStepSize); updateCamera();
        if (m_cameraDistance < 0.1):
            m_cameraDistance = 0.1;

    def zoomOut(self):
        self.m_cameraDistance += btScalar(m_zoomStepSize); updateCamera();

    def	isIdle(self):
        return	self.m_idle;

    def	setIdle(self, idle):
        self.m_idle = idle;

