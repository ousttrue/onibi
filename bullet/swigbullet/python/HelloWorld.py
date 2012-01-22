import bullet

if __name__=="__main__":
    broadphase = bullet.btDbvtBroadphase();
    collisionConfiguration = bullet.btDefaultCollisionConfiguration();
    dispatcher = bullet.btCollisionDispatcher(collisionConfiguration);

    solver = bullet.btSequentialImpulseConstraintSolver();
    dynamicsWorld = bullet.btDiscreteDynamicsWorld(
            dispatcher, broadphase, solver, collisionConfiguration);

    dynamicsWorld.setGravity((0,-10,0));

    groundShape = bullet.btStaticPlaneShape((0,1,0), 1);

    fallShape = bullet.btSphereShape(1);

    groundMotionState = bullet.btDefaultMotionState(
            bullet.btTransform(
                bullet.btQuaternion(0,0,0,1),
                (0,-1,0)
                )
            );

    groundRigidBodyCI=bullet.btRigidBodyConstructionInfo(0,
            groundMotionState, groundShape, (0,0,0));
    groundRigidBody = bullet.btRigidBody(groundRigidBodyCI);
    dynamicsWorld.addRigidBody(groundRigidBody);
 
    fallMotionState = bullet.btDefaultMotionState(
            bullet.btTransform(
                bullet.btQuaternion(0,0,0,1),
                (0,50,0)
                )
            );

    mass = 1;
    fallInertia=(0,0,0);
    fallShape.calculateLocalInertia(mass,fallInertia);
    fallRigidBodyCI=bullet.btRigidBodyConstructionInfo(mass,fallMotionState,fallShape,fallInertia);
    fallRigidBody = bullet.btRigidBody(fallRigidBodyCI);
    dynamicsWorld.addRigidBody(fallRigidBody);

    for i in range(300):
        dynamicsWorld.stepSimulation(1/60.0, 10);
 
        trans=bullet.btTransform();
        fallRigidBody.getMotionState().getWorldTransform(trans);
 
        print "sphere height: %f" % trans.getOrigin()[1]
 
