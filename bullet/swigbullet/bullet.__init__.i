%module(directors="1") bullet
%pythoncode {
SIMD_EPSILON=0.0000001192092896;
}
%{
#include <btBulletDynamicsCommon.h>
%}

//////////////////////////////////////////////////////////////////////////////
// typemaps
//////////////////////////////////////////////////////////////////////////////

// in btVector3
%typemap(in)const btVector3&(btVector3 tmp) {
    if (PyTuple_Check($input)) {
        if (!PyArg_ParseTuple($input,"fff", tmp.m_floats, tmp.m_floats+1, tmp.m_floats+2)) {
            PyErr_SetString(PyExc_TypeError,"tuple must have 3 elements");
            return NULL;
        }
        $1 = &tmp;
    }
    else{
        PyErr_SetString(PyExc_TypeError,"expected a tuple.");
        return NULL;
    }
}
%typemap(in)btVector3&(btVector3 tmp) {
    if (PyTuple_Check($input)) {
        if (!PyArg_ParseTuple($input,"fff", tmp.m_floats, tmp.m_floats+1, tmp.m_floats+2)) {
            PyErr_SetString(PyExc_TypeError,"tuple must have 3 elements");
            return NULL;
        }
        $1 = &tmp;
    }
    else{
        PyErr_SetString(PyExc_TypeError,"expected a tuple.");
        return NULL;
    }
}
%typemap(out)btVector3{
    $result = PyTuple_New(3);
    PyTuple_SetItem($result, 0, PyFloat_FromDouble($1.getX()));
    PyTuple_SetItem($result, 1, PyFloat_FromDouble($1.getY()));
    PyTuple_SetItem($result, 2, PyFloat_FromDouble($1.getZ()));
}
%typemap(out)const btVector3 &{
    $result = PyTuple_New(3);
    PyTuple_SetItem($result, 0, PyFloat_FromDouble($1->getX()));
    PyTuple_SetItem($result, 1, PyFloat_FromDouble($1->getY()));
    PyTuple_SetItem($result, 2, PyFloat_FromDouble($1->getZ()));
}
%typemap(out)btVector3 &{
    $result = PyTuple_New(3);
    PyTuple_SetItem($result, 0, PyFloat_FromDouble($1->getX()));
    PyTuple_SetItem($result, 1, PyFloat_FromDouble($1->getY()));
    PyTuple_SetItem($result, 2, PyFloat_FromDouble($1->getZ()));
}

// getBroadphaseAabb
%typemap(ignore) (btVector3& aabbMin,btVector3& aabbMax)(btVector3 tmpmin, btVector3 tmpmax){
    $1=&tmpmin;
    $2=&tmpmax;
}
%typemap(argout) (btVector3& aabbMin,btVector3& aabbMax){

    PyObject *v1=PyTuple_New(3);
    PyTuple_SET_ITEM(v1, 0, PyFloat_FromDouble($1->getX()));
    PyTuple_SET_ITEM(v1, 1, PyFloat_FromDouble($1->getY()));
    PyTuple_SET_ITEM(v1, 2, PyFloat_FromDouble($1->getZ()));

    PyObject *v2=PyTuple_New(3);
    PyTuple_SET_ITEM(v2, 0, PyFloat_FromDouble($2->getX()));
    PyTuple_SET_ITEM(v2, 1, PyFloat_FromDouble($2->getY()));
    PyTuple_SET_ITEM(v2, 2, PyFloat_FromDouble($2->getZ()));

    if ((!$result) || ($result == Py_None)) {
        // a single return value
        $result =  PyTuple_New(2);
        PyTuple_SetItem($result, 0, v1);
        PyTuple_SetItem($result, 1, v2);
    } 
    else if(PyTuple_Check($result)){
        // connect return values
        PyObject *o1 = $result;
        PyObject *o2 =  PyTuple_New(2);
        PyTuple_SetItem(o2, 0, v1);
        PyTuple_SetItem(o2, 1, v2);
        $result = PySequence_Concat(o1, o2);
        Py_DECREF(o1);
        Py_DECREF(o2);
    }
    else{
        // create new return tuple
        PyObject *o=$result;
        $result =  PyTuple_New(3);
        PyTuple_SetItem($result, 0, o);
        PyTuple_SetItem($result, 1, v1);
        PyTuple_SetItem($result, 2, v2);
    }
}

// getOpenGLMatrix
%typemap(ignore) (btScalar *m)(btScalar tmpM[16]) {
    $1=tmpM;    
}
%typemap(argout) (btScalar *m) {
    PyObject *o = PyTuple_New(16);
    for(int i=0; i<16; ++i){
        PyTuple_SetItem(o, i, PyFloat_FromDouble($1[i]));
    }

    if ((!$result) || ($result == Py_None)) {
        // 単独の返り値
        $result = o;
    } 
    else if(PyTuple_Check($result)){
        // 既存のtuple返り値と連結
        PyObject *o2 = $result;

        PyObject *o3 = PyTuple_New(1);
        PyTuple_SetItem(o3,0,o);

        $result = PySequence_Concat(o2,o3);
        Py_DECREF(o2);
        Py_DECREF(o3);
    }
    else{
        // 非tuple返り値と連結
        PyObject *o2=$result;
        $result=PyTuple_New(2);
        PyTuple_SetItem($result, 0, o2);
        PyTuple_SetItem($result, 1, o);
    }
}
//////////////////////////////////////////////////////////////////////////////

//%javaconst(1);
//%include cpointer.i
%include stl.i
%feature("director") btIDebugDraw;
%include "LinearMath/btScalar.h"
%include "LinearMath/btVector3.h"
%include "LinearMath/btQuaternion.h"
%include "LinearMath/btTransform.h"
%include "LinearMath/btMatrix3x3.h"
%include "LinearMath/btMotionState.h"
%include "LinearMath/btAlignedObjectArray.h"
%include "LinearMath/btDefaultMotionState.h"
%include "LinearMath/btIDebugDraw.h"
%include "LinearMath/btQuickprof.h"
%include "btBulletCollisionCommon.h"
%include "BulletCollision/BroadphaseCollision/btBroadphaseProxy.h"
%include "BulletCollision/BroadphaseCollision/btBroadphaseInterface.h"
%include "BulletCollision/BroadphaseCollision/btDbvtBroadphase.h"
%include "BulletCollision/BroadphaseCollision/btDispatcher.h"
%include "BulletCollision/CollisionDispatch/btCollisionConfiguration.h"
%include "BulletCollision/CollisionDispatch/btDefaultCollisionConfiguration.h"
%include "BulletCollision/CollisionDispatch/btCollisionDispatcher.h"
%include "BulletCollision/CollisionShapes/btCollisionShape.h"
%include "BulletCollision/CollisionShapes/btConvexShape.h"
%include "BulletCollision/CollisionShapes/btConvexInternalShape.h"
%include "BulletCollision/CollisionShapes/btSphereShape.h"
%include "BulletCollision/CollisionShapes/btMultiSphereShape.h"
%include "BulletCollision/CollisionShapes/btConcaveShape.h"
%include "BulletCollision/CollisionShapes/btStaticPlaneShape.h"
%include "BulletCollision/CollisionShapes/btPolyhedralConvexShape.h"
%include "BulletCollision/CollisionShapes/btBoxShape.h"
%include "BulletCollision/CollisionDispatch/btCollisionObject.h"
%include "BulletCollision/CollisionDispatch/btCollisionWorld.h"
%include "BulletDynamics/Dynamics/btDynamicsWorld.h"
%include "BulletDynamics/Dynamics/btDiscreteDynamicsWorld.h"
//%include "BulletDynamics/Dynamics/btContinuousDynamicsWorld.h"
%include "BulletDynamics/Dynamics/btSimpleDynamicsWorld.h"
//%include "BulletDynamics/Dynamics/btRigidBodyConstructionInfo.h"
%include "BulletDynamics/Dynamics/btRigidBody.h"
%include "BulletDynamics/ConstraintSolver/btConstraintSolver.h"
%include "BulletDynamics/ConstraintSolver/btTypedConstraint.h"
%include "BulletDynamics/ConstraintSolver/btPoint2PointConstraint.h"
%include "BulletDynamics/ConstraintSolver/btHingeConstraint.h"
%include "BulletDynamics/ConstraintSolver/btConeTwistConstraint.h"
%include "BulletDynamics/ConstraintSolver/btGeneric6DofConstraint.h"
%include "BulletDynamics/ConstraintSolver/btSliderConstraint.h"
%include "BulletDynamics/ConstraintSolver/btGeneric6DofSpringConstraint.h"
%include "BulletDynamics/ConstraintSolver/btUniversalConstraint.h"
%include "BulletDynamics/ConstraintSolver/btHinge2Constraint.h"
%include "BulletDynamics/ConstraintSolver/btSequentialImpulseConstraintSolver.h"

//////////////////////////////////////////////////////////////////////////////
// template
//////////////////////////////////////////////////////////////////////////////
%template(btCollisionObjectArray) btAlignedObjectArray<btCollisionObject*>;
%template(btScalarArray) btAlignedObjectArray<btScalar>;

//////////////////////////////////////////////////////////////////////////////
// btVector3
//////////////////////////////////////////////////////////////////////////////
%extend btVector3 {

btVector3 operator+(const btVector3 &rhs) {
    return (* $self) + rhs;
}

btVector3 operator-(const btVector3 &rhs) {
    return (* $self) - rhs;
}

btVector3 operator*(const btScalar s) {
    return (* $self) * s;
}

%pythoncode {
    def __getitem__(self, k):
        if k==0:
            return self.getX()
        elif k==1:
            return self.getY()
        elif k==2:
            return self.getZ()
        else:
            raise KeyError()

    def __setitem__(self, k, v):
        if k==0:
            self.setX(v)
        elif k==1:
            self.setY(v)
        elif k==2:
            self.setZ(v)
        else:
            raise KeyError()
} 

};

//////////////////////////////////////////////////////////////////////////////
%extend btMatrix3x3 {

btVector3 apply(const btVector3 &rhs) {
    return (* $self) * rhs;
}

btMatrix3x3 operator*(const btMatrix3x3 &rhs) {
    return (* $self) * rhs;
}

};

%extend btTransform {

btVector3 apply(const btVector3 &rhs) {
    return (* $self) * rhs;
}

};

//////////////////////////////////////////////////////////////////////////////
%inline %{

btCollisionObject* btCollisionObjectPP_deref(btCollisionObject** p)
{
    return *p;
}

%}

%extend btAlignedObjectArray<btCollisionObject*> {

%pythoncode {
    def __iter__(self):
        for i in range(self.size()):
            yield btCollisionObjectPP_deref(self.at(i))
}

};

//////////////////////////////////////////////////////////////////////////////
// downcast
//////////////////////////////////////////////////////////////////////////////
%extend btDefaultMotionState {

static btDefaultMotionState* downcast(btMotionState *s)
{
    return (btDefaultMotionState*)(s);
}

};

%extend btPoint2PointConstraint {

static btPoint2PointConstraint* downcast(btTypedObject *c)
{
    return (btPoint2PointConstraint*)(c);
}

};

%extend btGeneric6DofConstraint {

static btGeneric6DofConstraint* downcast(btTypedObject *c)
{
    return (btGeneric6DofConstraint*)(c);
}

};

//////////////////////////////////////////////////////////////////////////////
// btCollisionShape downcast
//////////////////////////////////////////////////////////////////////////////
%extend btBoxShape {

static btBoxShape* downcast(btCollisionShape *s)
{
    return (btBoxShape*)(s);
}

};

%extend btUniformScalingShape {

static btUniformScalingShape* downcast(btCollisionShape *s)
{
    return (btUniformScalingShape*)(s);
}

};

%extend btSphereShape {

static btSphereShape* downcast(btCollisionShape *s)
{
    return (btSphereShape*)(s);
}

};

%extend btMultiSphereShape {

static btMultiSphereShape* downcast(btCollisionShape *s)
{
    return (btMultiSphereShape*)(s);
}

};

%extend btStaticPlaneShape {

static btStaticPlaneShape* downcast(btCollisionShape *s)
{
    return (btStaticPlaneShape*)(s);
}

};

%extend btPolyhedralConvexShape {

static btPolyhedralConvexShape* downcast(btCollisionShape *s)
{
    return (btPolyhedralConvexShape*)(s);
}

};

%extend btConvexShape {

static btConvexShape* downcast(btCollisionShape *s)
{
    return (btConvexShape*)(s);
}

};

%extend btConcaveShape {

static btConcaveShape* downcast(btCollisionShape *s)
{
    return (btConcaveShape*)(s);
}

};

