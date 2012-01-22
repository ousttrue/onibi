%module(directors="1") "main"
%{
#include "Irrlicht.h"
#include "driverChoice.h"
#include "IAttribute.h"
using namespace irr;
using namespace core;
using namespace video;
using namespace gui;
using namespace scene;
%}
%feature("director") irr::IEventReceiver;

%include "irr.common.i"

%import "irr.core.i"
%import "irr.io.i"
%import "irr.video.i"
%import "irr.scene.i"
%import "irr.gui.i"

%inline %{
int getKeyAsInt(const irr::SKeyInput keyInput){ return static_cast<int>(keyInput.Key); }
int keyToInt(irr::EKEY_CODE key){ return static_cast<int>(key); }

const float* FloatPointer(const irr::core::vector3df &v){
    return reinterpret_cast<const float*>(&v);
}
const float* FloatPointer(const irr::video::SColorf &c){
    return reinterpret_cast<const float*>(&c);
}

unsigned int* new_u32(unsigned int num){
    unsigned int* p= new unsigned int;
    *p=num;
    return p;
}
void delete_u32(unsigned int *p){
    delete p;
}
%}

//////////////////////////////////////////////////////////////////////////////
// warning
//////////////////////////////////////////////////////////////////////////////
#pragma SWIG nowarn=312
#pragma SWIG nowarn=325
#pragma SWIG nowarn=362
#pragma SWIG nowarn=389
#pragma SWIG nowarn=401
#pragma SWIG nowarn=503

//////////////////////////////////////////////////////////////////////////////
// Irrlicht headers
//////////////////////////////////////////////////////////////////////////////
%include "IrrCompileConfig.h"
%include "irrTypes.h"
%include "Keycodes.h"
%include "ITimer.h"
%include "dimension2d.h"
%include "EDriverTypes.h"
%include "EDeviceTypes.h"
%include "SIrrCreationParameters.h"
%include "IrrlichtDevice.h"
%include "Irrlicht.h"
%include "IEventReceiver.h"
%include "driverChoice.h"

%extend irr::IrrlichtDevice {

irr::core::array<irr::SJoystickInfo> activateJoysticks() {
    irr::core::array<irr::SJoystickInfo> buf;
    $self->activateJoysticks(buf);
    return buf;
}

};

%extend irr::SJoystickEvent {
int getAxis(int axis){
    return $self->Axis[axis];
}
};

