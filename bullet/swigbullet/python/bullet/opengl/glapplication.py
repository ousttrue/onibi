from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy
from . import demoapplication
from . import glshapedrawer 
from . import gldebugfont
from . import vector3
import bullet.opengl.gldebugdrawer


class GLApplication(demoapplication.DemoApplication):

    def __init__(self):
        demoapplication.DemoApplication.__init__(self)
        self.m_shapeDrawer=glshapedrawer.GL_ShapeDrawer();
        self.m_shapeDrawer.enableTexture(True);
        self.m_isInitialized=False

    def myinit(self):
        print 'myinit'
        light_ambient = [ 0.2, 0.2, 0.2, 1.0 ];
        light_diffuse = [ 1.0, 1.0, 1.0, 1.0 ];
        light_specular = [ 1.0, 1.0, 1.0, 1.0 ];
        light_position0 = [ 1.0, 10.0, 1.0, 0.0 ];
        light_position1 = [ -1.0, -10.0, -1.0, 0.0 ];

        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient);
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse);
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular);
        glLightfv(GL_LIGHT0, GL_POSITION, light_position0);

        glLightfv(GL_LIGHT1, GL_AMBIENT, light_ambient);
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light_diffuse);
        glLightfv(GL_LIGHT1, GL_SPECULAR, light_specular);
        glLightfv(GL_LIGHT1, GL_POSITION, light_position1);

        glEnable(GL_LIGHTING);
        glEnable(GL_LIGHT0);
        glEnable(GL_LIGHT1);

        glShadeModel(GL_SMOOTH);
        glEnable(GL_DEPTH_TEST);
        glDepthFunc(GL_LESS);

        glClearColor(0.7, 0.7, 0.7, 0.0);

    def reshape(self, w, h):
        print('reshape', w, h)
        self.myinit()
        gldebugfont.GLDebugResetFont(w,h);

        self.m_glutScreenWidth = w;
        self.m_glutScreenHeight = h;

        glViewport(0, 0, w, h);
        self.updateCamera();
        self.m_isInitialized=True

    def updateCamera(self):
        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
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
            glLoadIdentity();

            extents *= self.m_cameraDistance;
            lower = self.m_cameraTargetPosition - extents;
            upper = self.m_cameraTargetPosition + extents;
            # gluOrtho2D(lower.x, upper.x, lower.y, upper.y);
            glOrtho(lower.getX(), upper.getX(),
                    lower.getY(), upper.getY(),
                    -1000, 1000);

            glMatrixMode(GL_MODELVIEW);
            glLoadIdentity();
            # glTranslatef(100, 210, 0);
        else:
            # glFrustum (-aspect, aspect, -1.0, 1.0, 1.0, 10000.0);
            glFrustum (-aspect * self.m_frustumZNear, aspect * self.m_frustumZNear,
                    -self.m_frustumZNear, self.m_frustumZNear,
                    self.m_frustumZNear, self.m_frustumZFar);
            glMatrixMode(GL_MODELVIEW);
            glLoadIdentity();
            gluLookAt(
                    self.m_cameraPosition[0], self.m_cameraPosition[1], self.m_cameraPosition[2],
                    self.m_cameraTargetPosition[0],
                    self.m_cameraTargetPosition[1],
                    self.m_cameraTargetPosition[2],
                    self.m_cameraUp[0],self.m_cameraUp[1],self.m_cameraUp[2]);

    def renderme(self):
        if not self.m_isInitialized:
            return

        self.updateCamera();

        if (self.m_dynamicsWorld):
            if(self.m_enableshadows):
                glClear(GL_STENCIL_BUFFER_BIT);
                glEnable(GL_CULL_FACE);
                self.renderscene(0);

                glDisable(GL_LIGHTING);
                glDepthMask(GL_FALSE);
                glDepthFunc(GL_LEQUAL);
                glEnable(GL_STENCIL_TEST);
                glColorMask(GL_FALSE,GL_FALSE,GL_FALSE,GL_FALSE);
                glStencilFunc(GL_ALWAYS,1,0xFFFFFFFFL);
                glFrontFace(GL_CCW);
                glStencilOp(GL_KEEP,GL_KEEP,GL_INCR);
                self.renderscene(1);
                glFrontFace(GL_CW);
                glStencilOp(GL_KEEP,GL_KEEP,GL_DECR);
                self.renderscene(1);
                glFrontFace(GL_CCW);

                glPolygonMode(GL_FRONT,GL_FILL);
                glPolygonMode(GL_BACK,GL_FILL);
                glShadeModel(GL_SMOOTH);
                glEnable(GL_DEPTH_TEST);
                glDepthFunc(GL_LESS);
                glEnable(GL_LIGHTING);
                glDepthMask(GL_TRUE);
                glCullFace(GL_BACK);
                glFrontFace(GL_CCW);
                glEnable(GL_CULL_FACE);
                glColorMask(GL_TRUE,GL_TRUE,GL_TRUE,GL_TRUE);

                glDepthFunc(GL_LEQUAL);
                glStencilFunc( GL_NOTEQUAL, 0, 0xFFFFFFFFL );
                glStencilOp( GL_KEEP, GL_KEEP, GL_KEEP );
                glDisable(GL_LIGHTING);
                self.renderscene(2);
                glEnable(GL_LIGHTING);
                glDepthFunc(GL_LESS);
                glDisable(GL_STENCIL_TEST);
                glDisable(GL_CULL_FACE);
            else:
                glDisable(GL_CULL_FACE);
                self.renderscene(0);

            xOffset = 10;
            yStart = 20;
            yIncr = 20;

            glDisable(GL_LIGHTING);
            glColor3f(0, 0, 0);

            if ((self.m_debugMode & bullet.btIDebugDraw.DBG_NoHelpText)==0):
                self.setOrthographicProjection();

                self.showProfileInfo(xOffset,yStart,yIncr);

                self.resetPerspectiveProjection();

            glDisable(GL_LIGHTING);

        #self.updateCamera();

    def renderscene(self, renderpass):
        rot=bullet.btMatrix3x3();
        rot.setIdentity();
        m=numpy.array([
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0,
            0, 0, 0, 0
            ], 'f')
        for i, colObj in enumerate(self.m_dynamicsWorld.getCollisionObjectArray()):
            body=bullet.btRigidBody.upcast(colObj);
            if(body and body.getMotionState()):
                myMotionState = bullet.btDefaultMotionState.downcast(body.getMotionState());
                _m=myMotionState.m_graphicsWorldTrans.getOpenGLMatrix();
                rot=myMotionState.m_graphicsWorldTrans.getBasis();
            else:
                _m=colObj.getWorldTransform().getOpenGLMatrix();
                rot=colObj.getWorldTransform().getBasis();

            for j, v in enumerate(_m):
                m[j]=v                

            state=colObj.getActivationState()
            if(i&1): # odd
                if state==1: # active
                    wireColor=(1.0, 0.0, 1.0);
                elif state==2: # ISLAND_SLEEPING
                    wireColor=(0.0, 1.0, 1.0);
                else:
                    wireColor=(0.0, 0.0, 1.0);
            else: # even
                # color differently for active, sleeping, wantsdeactivation states
                if state==1: # active
                    wireColor=(1.5, 1.0, 0.5);
                elif state==2: # ISLAND_SLEEPING
                    wireColor=(1.0, 1.5, 0.5);
                else:
                    wireColor=(1.0, 1.0, 0.5); # wants deactivation

            aabbMin, aabbMax=self.m_dynamicsWorld.getBroadphase().getBroadphaseAabb();

            vector3.sub(aabbMin, (
                bullet.BT_LARGE_FLOAT,
                bullet.BT_LARGE_FLOAT,
                bullet.BT_LARGE_FLOAT));
            vector3.sub(aabbMax, (
                bullet.BT_LARGE_FLOAT,
                bullet.BT_LARGE_FLOAT,
                bullet.BT_LARGE_FLOAT));

            if (not (self.getDebugMode() & bullet.btIDebugDraw.DBG_DrawWireframe)):
                if renderpass==0:
                    self.m_shapeDrawer.drawOpenGL(m,
                            colObj.getCollisionShape(),
                            wireColor, self.getDebugMode(),
                            aabbMin, aabbMax);
                elif renderpass==1:
                    self.m_shapeDrawer.drawShadow(m,
                            rot.apply(self.m_sundirection), colObj.getCollisionShape(),
                            aabbMin,aabbMax);
                elif renderpass==2:
                    self.m_shapeDrawer.drawOpenGL(m,
                            colObj.getCollisionShape(),
                            vector3.mul(wireColor, 0.3), 0,
                            aabbMin, aabbMax);

    def setOrthographicProjection(self):
        # See http://www.lighthouse3d.com/opengl/glut/index.php?bmpfontortho

        glMatrixMode(GL_PROJECTION);
        glPushMatrix();
        glLoadIdentity();
        # set a 2D orthographic projection
        if self.m_glutScreenWidth>0 and self.m_glutScreenWidth>0:
            gluOrtho2D(0, self.m_glutScreenWidth, 0, self.m_glutScreenHeight);
        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();

        # invert the y axis, down is positive
        glScalef(1, -1, 1);
        # mover the origin from the bottom left corner
        # to the upper left corner
        glTranslatef(0, -self.m_glutScreenHeight, 0);

    def displayProfileString(self, xOffset, yStart, message):
        glRasterPos3f(xOffset, yStart, 0);
        gldebugfont.GLDebugDrawString(xOffset, yStart, message);

    def resetPerspectiveProjection(self):
        glMatrixMode(GL_PROJECTION);
        glPopMatrix();
        glMatrixMode(GL_MODELVIEW);
        self.updateCamera();

    def overrideGLShapeDrawer(self, shapeDrawer):
        shapeDrawer.enableTexture(self.m_shapeDrawer.hasTextureEnabled());
        self.m_shapeDrawer = shapeDrawer;

    def	setTexturing(self, enable):
        return self.m_shapeDrawer.enableTexture(enable);

    def	getTexturing(self):
        return self.m_shapeDrawer.hasTextureEnabled();

    # callback methods by glut	
    def keyboardCallback(self, key, x, y):
        if key=='u' :
            self.m_shapeDrawer.enableTexture(not self.m_shapeDrawer.enableTexture(False));
        else:
            demoapplication.DemoApplication.keyboardCallback(self, key, x, y)

