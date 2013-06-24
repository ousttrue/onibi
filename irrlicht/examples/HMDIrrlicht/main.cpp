/*
Copyright (C) 2012 Luca Siciliano

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, 
modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the 
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT 
OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

#include <irrlicht.h>
#include "HMDStereoRender.h"
#define MEDIA_PATH "../../media/"
#include <iostream>
#include <ovr.h>

class Oculus
{
    OVR::Ptr<OVR::DeviceManager> pManager;
    OVR::Ptr<OVR::HMDDevice> pHMD;
    OVR::Ptr<OVR::SensorDevice> pSensor;
    OVR::SensorFusion SFusion;

public:
    Oculus()
    {
        OVR::System::Init(OVR::Log::ConfigureDefaultLog(OVR::LogMask_All));
    }

    ~Oculus()
    {
        OVR::System::Destroy();
    }

    bool initilaize()
    {
        pManager = *OVR::DeviceManager::Create();
        if(!pManager){
            return false;
        }
        pHMD = *pManager->EnumerateDevices<OVR::HMDDevice>().CreateDevice();
        if(!pHMD){
            return false;
        }
        pSensor = *pHMD->GetSensor();
        if(!pSensor){
            return false;
        }

        SFusion.AttachToSensor(pSensor);
        return true;
    }

	irr::core::quaternion getRotation()
	{
        OVR::Quatf hmdOrient = SFusion.GetOrientation();
		return irr::core::quaternion(hmdOrient.x, hmdOrient.y, hmdOrient.z, hmdOrient.w);
	}
};


// Configuration

int SCREEN_WIDTH = 1280;
int SCREEN_HEIGHT = 800;
bool fullscreen = false;
bool vsync = true;
float mouseSpeed = 40.0f;
float walkSpeed = 3.0f;

class MyEventReceiver : public irr::IEventReceiver
{
public:
   bool OnEvent(const irr::SEvent& event)
   {   
       switch(event.EventType)
       {
           case irr::EET_KEY_INPUT_EVENT:
               if(event.KeyInput.PressedDown) {
                   if (event.KeyInput.Key == irr::KEY_ESCAPE || event.KeyInput.Key==irr::KEY_KEY_Q)
                   {
                       device->closeDevice();
                       return true;
                   }
               }
               break;
       }
       return false;
   }
   irr::IrrlichtDevice* device;
   irr::gui::ICursorControl* cursor;
};


static inline irr::core::quaternion flip_quaternion(const irr::core::quaternion &q)
{
	irr::f32 angle;
	irr::core::vector3df axis;
	q.toAngleAxis(angle, axis);
	return irr::core::quaternion().fromAngleAxis(angle, 
		irr::core::vector3df(
		axis.X,
		axis.Y,
		-axis.Z
		));
}


int main(int argc, char* argv[]){
  // Check fullscreen
  for (int i=1;i<argc;i++) fullscreen |= !strcmp("-f", argv[i]);

  MyEventReceiver receiver;
  irr::IrrlichtDevice *device = createDevice(irr::video::EDT_OPENGL, irr::core::dimension2d<irr::u32>(SCREEN_WIDTH, SCREEN_HEIGHT), 16, fullscreen, false, vsync, &receiver);
  receiver.device = device;
  receiver.cursor = device->getCursorControl();

  irr::video::IVideoDriver* driver = device->getVideoDriver();
  irr::scene::ISceneManager* smgr = device->getSceneManager();
  irr::gui::IGUIEnvironment* guienv = device->getGUIEnvironment();
  irr::video::IGPUProgrammingServices* gpu = driver->getGPUProgrammingServices();

  HMDDescriptor HMD;
  // Parameters from the Oculus Rift DK1
  HMD.hResolution = 1280;
  HMD.vResolution = 800;
  HMD.hScreenSize = 0.14976;
  HMD.vScreenSize = 0.0936;
  HMD.interpupillaryDistance = 0.064;
  HMD.lensSeparationDistance = 0.064;
  HMD.eyeToScreenDistance = 0.041;
  HMD.distortionK[0] = 1.0;
  HMD.distortionK[1] = 0.22;
  HMD.distortionK[2] = 0.24;
  HMD.distortionK[3] = 0.0;

  HMDStereoRender renderer(device, HMD, 10);
  
  // load the quake map
  device->getFileSystem()->addFileArchive("../../media/map-20kdm2.pk3");

  irr::scene::IAnimatedMesh* q3levelmesh = smgr->getMesh("20kdm2.bsp");
  irr::scene::IMeshSceneNode* q3node = 0;

  if (q3levelmesh)
      q3node = smgr->addOctreeSceneNode(q3levelmesh->getMesh(0), 0, -1);

  irr::scene::ITriangleSelector* selector = 0;

  if (q3node)
  {
      q3node->setPosition(irr::core::vector3df(-1350,-130,-1400));

      selector = smgr->createOctreeTriangleSelector(
              q3node->getMesh(), q3node, 128);
      q3node->setTriangleSelector(selector);
      // We're not done with this selector yet, so don't drop it.
  }

  // Create world
  irr::core::array<irr::SKeyMap> keymaps;
  keymaps.push_back(irr::SKeyMap(irr::EKA_MOVE_FORWARD, irr::KEY_KEY_W));
  keymaps.push_back(irr::SKeyMap(irr::EKA_MOVE_BACKWARD, irr::KEY_KEY_S));
  keymaps.push_back(irr::SKeyMap(irr::EKA_STRAFE_LEFT, irr::KEY_KEY_A));
  keymaps.push_back(irr::SKeyMap(irr::EKA_STRAFE_RIGHT, irr::KEY_KEY_D));
  keymaps.push_back(irr::SKeyMap(irr::EKA_JUMP_UP, irr::KEY_SPACE));
  irr::scene::ICameraSceneNode* camera =
      smgr->addCameraSceneNodeFPS(0, 
              80.0f, .1f, -1, 
              keymaps.pointer(), keymaps.size(), 
              true, .5f, false, true,
              true
              );
  camera->setPosition(irr::core::vector3df(50,50,-60));
  camera->setTarget(irr::core::vector3df(-70,30,-60));
  {
      irr::scene::ISceneNodeAnimator* anim = smgr->createCollisionResponseAnimator(
              selector, camera, 
              irr::core::vector3df(30,50,30),
              irr::core::vector3df(0,-10,0), 
              irr::core::vector3df(0,30,0));
      selector->drop(); // As soon as we're done with the selector, drop it.
      camera->addAnimator(anim);
      anim->drop();  // And likewise, drop the animator when we're done referring to it.
  }

  // load a faerie 
  auto faerie = smgr->getMesh(MEDIA_PATH "faerie.md2");
  auto faerieNode = smgr->addAnimatedMeshSceneNode(faerie);
  faerieNode->setMaterialTexture(0, driver->getTexture(MEDIA_PATH "faerie2.bmp"));
  faerieNode->setMaterialFlag(irr::video::EMF_LIGHTING, false);
  faerieNode->setPosition(irr::core::vector3df(40,190,-1030));
  faerieNode->setRotation(irr::core::vector3df(0,-90,0));
  faerieNode->setMD2Animation(irr::scene::EMAT_SALUTE);

  // load a dwarf
  auto dwarf = smgr->getMesh(MEDIA_PATH "dwarf.x");
  auto dwarfNode = smgr->addAnimatedMeshSceneNode(dwarf);
  dwarfNode->setPosition(irr::core::vector3df(40,-25,20));

  device->getCursorControl()->setVisible(false);

  {
  Oculus oculus;
  oculus.initilaize();

  // Render loop
  irr::core::vector3df rot;
  while(device->run()){
    // get Oculus rift rotation
	irr::core::quaternion q=oculus.getRotation();

    driver->beginScene(true,true,irr::video::SColor(0,100,100,100));

    renderer.drawAll(smgr, flip_quaternion(q));
   
    // end scene
    driver->endScene();
  }
  device->drop();
  }

  return 0;
}

