#ifndef INTERFACE_RIGID_BODY_H_INCLUDED
#define INTERFACE_RIGID_BODY_H_INCLUDED

#include <irrlicht.h>
#include <string>

class btRigidBody;

namespace irr {
namespace bullet {

class IShape;

class IRigidBody : public IReferenceCounted
{
protected:
    f32 ScalingFactor;
public:
    IRigidBody(f32 scalingFactor):ScalingFactor(scalingFactor){}
	virtual ~IRigidBody(){};
	virtual btRigidBody* getBulletRigidBody()const=0; 
	virtual IShape* getShape()const=0;
	virtual void draw();
	virtual std::string getName()const=0;
	virtual void syncBone(){};
};


} // namespace bullet
} // namespace irr

#endif // INTERFACE_RIGID_BODY_H_INCLUDED
