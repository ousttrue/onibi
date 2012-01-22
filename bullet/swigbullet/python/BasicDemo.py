import sys
from OpenGL.GL import *
from OpenGL.GLU import *
import bullet
from bullet.opengl.sdl import main, DemoApplication
#from bullet.opengl.glut import main, DemoApplication


# create 125 (5x5x5) dynamic object
ARRAY_SIZE_X=5
ARRAY_SIZE_Y=5
ARRAY_SIZE_Z=5

# maximum number of objects (and allow user to shoot additional boxes)
MAX_PROXIES=(ARRAY_SIZE_X*ARRAY_SIZE_Y*ARRAY_SIZE_Z + 1024)

# scaling of the objects (0.1 = 20 centimeter boxes )
SCALING=1.0
START_POS_X=-5
START_POS_Y=-5
START_POS_Z=-3


class BasicDemo(DemoApplication):

    def __init__(self):
        super(BasicDemo, self).__init__()
        self.m_broadphase=None
        self.m_dispatcher=None
        self.m_solver=None
        self.m_collisionConfiguration=None

    def __del__(self):
        self.exitPhysics()

    def createAndAppendBody(self, shape, mass, transform):
        # rigidbody is dynamic if and only if mass is non zero, otherwise static
        isDynamic = (mass != 0.0);

        localInertia=(0,0,0);
        if (isDynamic):
            shape.calculateLocalInertia(mass,localInertia);

        # using motionstate is recommended, 
        # it provides interpolation capabilities, and only synchronizes 'active' objects
        myMotionState = bullet.btDefaultMotionState(transform);
        rbInfo=bullet.btRigidBodyConstructionInfo(mass,
                myMotionState,
                shape,
                localInertia);
        body = bullet.btRigidBody(rbInfo);

        # add the body to the dynamics world
        self.m_dynamicsWorld.addRigidBody(body);
        self.m_keep.append((shape, myMotionState, body));

    def	initPhysics(self):
        self.setTexturing(True);
        #self.setShadows(True);
        #self.setDebugMode(bullet.btIDebugDraw.DBG_NoHelpText)

        self.setCameraDistance(SCALING*50.0);

        # collision configuration contains default setup for memory, collision setup
        self.m_collisionConfiguration = bullet.btDefaultCollisionConfiguration();

        # use the default collision dispatcher. 
        # For parallel processing you can use a diffent dispatcher (see Extras/BulletMultiThreaded)
        self.m_dispatcher = bullet.btCollisionDispatcher(self.m_collisionConfiguration);

        self.m_broadphase = bullet.btDbvtBroadphase();

        # the default constraint solver. 
        # For parallel processing you can use a different solver (see Extras/BulletMultiThreaded)
        self.m_solver = bullet.btSequentialImpulseConstraintSolver();

        self.m_dynamicsWorld = bullet.btDiscreteDynamicsWorld(
                self.m_dispatcher,
                self.m_broadphase,
                self.m_solver,
                self.m_collisionConfiguration);
        self.m_dynamicsWorld.setGravity((0,-10,0));

        self.initGroundShape()
        self.initRigidBodies()

    def initGroundShape(self):
        # create a few basic rigid bodies
        groundShape = bullet.btBoxShape(
                (50.0, 50.0, 50.0));
        
        groundTransform=bullet.btTransform();
        groundTransform.setIdentity();
        groundTransform.setOrigin((0,-50,0));

        self.createAndAppendBody(groundShape, 0.0, groundTransform)

    def initRigidBodies(self):
        # create a few dynamic rigidbodies
        # Re-using the same collision is better for memory usage and performance
        colShape = bullet.btBoxShape((SCALING*1,SCALING*1,SCALING*1));

        # Create Dynamic Objects
        startTransform=bullet.btTransform();
        startTransform.setIdentity();

        start_x = START_POS_X - ARRAY_SIZE_X/2;
        start_y = START_POS_Y;
        start_z = START_POS_Z - ARRAY_SIZE_Z/2;

        for k in range(ARRAY_SIZE_Y):
            for i in range(ARRAY_SIZE_X):
                for j in range(ARRAY_SIZE_Z):
                    startTransform.setOrigin((
                        SCALING* (2.0*i + start_x),
                        SCALING* (20+2.0*k + start_y),
                        SCALING* (2.0*j + start_z)
                        ));

                    self.createAndAppendBody(colShape, 1.0, startTransform)

    def	exitPhysics(self):
        print 'exitPhysics'
        # cleanup in the reverse order of creation/initialization
        # remove the rigidbodies from the dynamics world and delete them
        for i, colObj in enumerate(self.m_dynamicsWorld.getCollisionObjectArray()):
            #print i, 'removeCollisionObject', colObj
            self.m_dynamicsWorld.removeCollisionObject(colObj);
        del self.m_dynamicsWorld;
        del self.m_solver;
        del self.m_dispatcher;
        del self.m_collisionConfiguration;
        del self.m_keep

    def clientMoveAndDisplay(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT); 
        # simple dynamics world doesn't handle fixed-time-stepping
        ms = self.getDeltaTimeMicroseconds();
        # step the simulation
        if (self.m_dynamicsWorld):
            self.m_dynamicsWorld.stepSimulation(ms / 1000000.0);
            # optional but useful: debug drawing
            self.m_dynamicsWorld.debugDrawWorld();
        self.renderme(); 
        glFlush();
        self.swapBuffers();

    def displayCallback(self):
        pass

    def	clientResetScene(self):
        self.exitPhysics()
        self.initPhysics()


if __name__=="__main__":
    main(sys.argv, 
            1024, 600, 
            "Bullet Physics Demo. http://bulletphysics.org", 
            BasicDemo())

