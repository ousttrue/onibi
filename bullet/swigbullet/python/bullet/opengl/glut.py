from OpenGL.GLUT import *
from . import glapplication
import bullet.opengl.gldebugdrawer


class DemoApplication(glapplication.GLApplication):

    def specialKeyboard(self, key, x, y):
        if key== GLUT_KEY_F1:
            pass
        elif key== GLUT_KEY_F2:
            pass
        elif key== GLUT_KEY_END:
            numObj = self.getDynamicsWorld().getNumCollisionObjects();
            if (numObj):
                obj = self.getDynamicsWorld().getCollisionObjectArray()[numObj-1];
                self.getDynamicsWorld().removeCollisionObject(obj);
                body = bullet.btRigidBody.upcast(obj);
                if (body and body.getMotionState()):
                    #delete body.getMotionState();
                    pass
                #delete obj;
        elif key== GLUT_KEY_LEFT :
            self.stepLeft()
        elif key== GLUT_KEY_RIGHT :
            self.stepRight()
        elif key== GLUT_KEY_UP :
            self.stepFront()
        elif key== GLUT_KEY_DOWN :
            self.stepBack()
        elif key== GLUT_KEY_PAGE_UP :
            self.zoomIn()
        elif key== GLUT_KEY_PAGE_DOWN :
            self.zoomOut()
        elif key== GLUT_KEY_HOME :
            self.toggleIdle()
        else:
            print "unused (special) key : " + key

        glutPostRedisplay();

    def swapBuffers(self):
        glutSwapBuffers();

    def	updateModifierKeys(self):
        self.m_alt_key=glutGetModifiers() & GLUT_ACTIVE_ALT
        self.m_ctrl_key=glutGetModifiers() & GLUT_ACTIVE_CTRL
        self.m_shift_key=glutGetModifiers() & GLUT_ACTIVE_SHIFT


# glut is C code, this global gDemoApplication links glut to the C++ demo
gDemoApplication = None;


def glutKeyboardCallback(key, x, y):
    gDemoApplication.keyboardCallback(key,x,y);

def glutKeyboardUpCallback(key, x, y):
    gDemoApplication.keyboardUpCallback(key,x,y);

def glutSpecialKeyboardCallback(key, x, y):
    gDemoApplication.specialKeyboard(key,x,y);

def glutSpecialKeyboardUpCallback(key, x, y):
    gDemoApplication.specialKeyboardUp(key,x,y);

def glutReshapeCallback(w, h):
    gDemoApplication.reshape(w,h);

def glutMoveAndDisplayCallback():
    gDemoApplication.moveAndDisplay();

def glutMouseFuncCallback(button, state, x, y):
    gDemoApplication.mouseFunc(button,state,x,y);

def	glutMotionFuncCallback(x, y):
    gDemoApplication.mouseMotionFunc(x,y);

def glutDisplayCallback():
    gDemoApplication.displayCallback();

def main(argv, width, height, title, demoApp):
    global gDemoApplication
    gDemoApplication = demoApp;
    gDemoApplication.initPhysics();
    debugDrawer=bullet.opengl.gldebugdrawer.GLDebugDrawer()
    gDemoApplication.getDynamicsWorld().setDebugDrawer(debugDrawer);

    glutInit(argv);
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_STENCIL);
    glutInitWindowPosition(0, 0);
    glutInitWindowSize(width, height);
    glutCreateWindow(title);

    #gDemoApplication.myinit();

    glutKeyboardFunc(glutKeyboardCallback);
    glutKeyboardUpFunc(glutKeyboardUpCallback);
    glutSpecialFunc(glutSpecialKeyboardCallback);
    glutSpecialUpFunc(glutSpecialKeyboardUpCallback);

    glutReshapeFunc(glutReshapeCallback);
    # createMenu();
    glutIdleFunc(glutMoveAndDisplayCallback);
    glutMouseFunc(glutMouseFuncCallback);
    glutPassiveMotionFunc(glutMotionFuncCallback);
    glutMotionFunc(glutMotionFuncCallback);
    glutDisplayFunc( glutDisplayCallback );

    glutMoveAndDisplayCallback();

    glutMainLoop();
    return 0;

