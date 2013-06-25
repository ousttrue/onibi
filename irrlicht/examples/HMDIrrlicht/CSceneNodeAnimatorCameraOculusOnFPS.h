#pragma once
#include <irrlicht.h>


namespace irr { 

namespace gui
{
	class ICursorControl;
}

namespace scene {

class Oculus;
class CSceneNodeAnimatorCameraOculusOnFPS: public ISceneNodeAnimatorCameraFPS
{
public:

    //! Constructor
    CSceneNodeAnimatorCameraOculusOnFPS(gui::ICursorControl* cursorControl,
        f32 rotateSpeed = 100.0f, f32 moveSpeed = .5f, f32 jumpSpeed=0.f,
        SKeyMap* keyMapArray=0, u32 keyMapSize=0, bool noVerticalMovement=false,
        bool invertY=false);

    //! Destructor
    virtual ~CSceneNodeAnimatorCameraOculusOnFPS();

    static ICameraSceneNode* addCameraSceneNodeOclusOnFPS(ISceneManager *smgr,
            gui::ICursorControl *cursorControl,
            ISceneNode *parent,
            f32 rotateSpeed, f32 moveSpeed, s32 id, SKeyMap* keyMapArray,
            s32 keyMapSize, bool noVerticalMovement, f32 jumpSpeed,
            bool invertMouseY, bool makeActive
            );

    //! Animates the scene node, currently only works on cameras
    virtual void animateNode(ISceneNode* node, u32 timeMs);

    //! Event receiver
    virtual bool OnEvent(const SEvent& event);

    //! Returns the speed of movement in units per second
    virtual f32 getMoveSpeed() const;

    //! Sets the speed of movement in units per second
    virtual void setMoveSpeed(f32 moveSpeed);

    //! Returns the rotation speed
    virtual f32 getRotateSpeed() const;

    //! Set the rotation speed
    virtual void setRotateSpeed(f32 rotateSpeed);

    //! Sets the keyboard mapping for this animator (old style)
    //! \param keymap: an array of keyboard mappings, see SKeyMap
    //! \param count: the size of the keyboard map array
    virtual void setKeyMap(SKeyMap *map, u32 count);

    //! Sets the keyboard mapping for this animator
    //!	\param keymap The new keymap array 
    virtual void setKeyMap(const core::array<SKeyMap>& keymap);

    //! Gets the keyboard mapping for this animator
    virtual const core::array<SKeyMap>& getKeyMap() const;

    //! Sets whether vertical movement should be allowed.
    virtual void setVerticalMovement(bool allow);

    //! Sets whether the Y axis of the mouse should be inverted.
    /** If enabled then moving the mouse down will cause
    the camera to look up. It is disabled by default. */
    virtual void setInvertMouse(bool invert);

    //! This animator will receive events when attached to the active camera
    virtual bool isEventReceiverEnabled() const
    {
        return true;
    }

    //! Returns the type of this animator
    virtual ESCENE_NODE_ANIMATOR_TYPE getType() const
    {
        return ESNAT_CAMERA_FPS;
    }

    //! Creates a clone of this animator.
    /** Please note that you will have to drop
    (IReferenceCounted::drop()) the returned pointer once you're
    done with it. */
    virtual ISceneNodeAnimator* createClone(ISceneNode* node, ISceneManager* newManager=0);

private:
    void allKeysUp();

    gui::ICursorControl *CursorControl;

    f32 MaxVerticalAngle;

    f32 MoveSpeed;
    f32 RotateSpeed;
    f32 JumpSpeed;
    // -1.0f for inverted mouse, defaults to 1.0f
    f32 MouseYDirection;

    s32 LastAnimationTime;

    core::array<SKeyMap> KeyMap;
    core::position2d<f32> CenterCursor, CursorPos;

    bool CursorKeys[EKA_COUNT];

    bool firstUpdate;
    bool firstInput;
    bool NoVerticalMovement;

    Oculus *m_oculus;
};

}}
