#include <irrlicht.h>
#include "HMDStereoRender.h"
#include "CSceneNodeAnimatorCameraOculusOnFPS.h"
#include <memory>
#include <assert.h>


const int WIDTH=1280;
const int HEIGHT=800;
const int MSPF=1000/30;
#define MEDIA_PATH "../../media/"

int main(int argc, char **argv)
{
	bool isFullscreen=true;
    auto device = std::shared_ptr<irr::IrrlichtDevice>(
            irr::createDevice(
                irr::video::EDT_OPENGL,
                irr::core::dimension2d<irr::u32>(WIDTH, HEIGHT), 
                16, isFullscreen, false, false),
            [](irr::IrrlichtDevice* p){ p->drop(); }
            );
    assert(device);
    device->setWindowCaption(L"Irrlicht");

    // Oculus stereo renderer
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
    HMDStereoRender renderer(device.get(), HMD, 10);

    // camera
    irr::core::array<irr::SKeyMap> keymaps;
    keymaps.push_back(irr::SKeyMap(irr::EKA_MOVE_FORWARD, irr::KEY_KEY_W));
    keymaps.push_back(irr::SKeyMap(irr::EKA_MOVE_BACKWARD, irr::KEY_KEY_S));
    keymaps.push_back(irr::SKeyMap(irr::EKA_STRAFE_LEFT, irr::KEY_KEY_A));
    keymaps.push_back(irr::SKeyMap(irr::EKA_STRAFE_RIGHT, irr::KEY_KEY_D));
    keymaps.push_back(irr::SKeyMap(irr::EKA_JUMP_UP, irr::KEY_SPACE));
    auto camera= irr::scene::CSceneNodeAnimatorCameraOculusOnFPS::addCameraSceneNodeOclusOnFPS(
		device->getSceneManager(), device->getCursorControl(),
			0, 
                80.0f, .1f, -1, 
                keymaps.pointer(), keymaps.size(), 
                true, .5f, false, true);
    camera->setPosition(irr::core::vector3df(50,50,-60));
    camera->setTarget(irr::core::vector3df(-70,30,-60));
    {
		irr::scene::ISceneNodeAnimator* anim = device->getSceneManager()->createCollisionResponseAnimator(
                0, camera, 
                irr::core::vector3df(30,50,30),
                irr::core::vector3df(0,-10,0), 
                irr::core::vector3df(0,30,0));
        camera->addAnimator(anim);
        anim->drop();  // And likewise, drop the animator when we're done referring to it.
    }
 
	////////////////////////////////////////////////////////////
	// setup scene
	////////////////////////////////////////////////////////////
	// load the irrlicht engine logo
	device->getFileSystem()->addFileArchive(MEDIA_PATH);

	auto img =
		device->getGUIEnvironment()->addImage(
				device->getVideoDriver()->getTexture("irrlichtlogo2.png"),
				irr::core::position2d<irr::s32>(
					10, device->getVideoDriver()->getScreenSize().Height - 128));

	{
		// add skybox
		auto SkyBox = 
			device->getSceneManager()->addSkyBoxSceneNode(
					device->getVideoDriver()->getTexture("irrlicht2_up.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_dn.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_lf.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_rt.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_ft.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_bk.jpg"));
	}
	{
		auto planemesh = 
			device->getSceneManager()->addHillPlaneMesh("myHill", 
					irr::core::dimension2d<irr::f32>(24, 24), 
					irr::core::dimension2d<irr::u32>(100, 100));
		auto q3sn = device->getSceneManager()->
			addOctreeSceneNode(planemesh);
		//q3sn->setMaterialFlag(video::EMF_LIGHTING, false);
		q3sn->setMaterialTexture(0, device->getVideoDriver()->getTexture(MEDIA_PATH "wall.jpg"));
	}
	{
		// create light
		auto light 
			= device->getSceneManager()->addLightSceneNode(camera, 
					irr::core::vector3df(100, 100, -100), 
					irr::video::SColorf(100.0, 100.0, 100.0, 0.0), 1500.0f);
	}

#if 0
	////////////////////////////////////////////////////////////
	// load pmd model and vmd motion
	////////////////////////////////////////////////////////////
	// setup custom loader
	irrMMDsetup(device);

	// load 
	scene::CCustomSkinnedMesh *mesh=0;
	for(int i=1; i<argc; ++i){
#ifdef UNICODE
		wchar_t unicode[MAX_PATH];
		MultiByteToWideChar(CP_OEMCP, 0, argv[i], -1,
			unicode, MAX_PATH);

		io::path path(unicode);
#else
		io::path path(argv[i]);
#endif
		if(core::hasFileExtension(path, "pmd")){
			mesh=dynamic_cast<scene::CCustomSkinnedMesh*>(
					receiver->loadMesh(path));
		}
		else if(core::hasFileExtension(path, "vmd")){
			scene::CVMDCustomSkinMotion *motion=new scene::CVMDCustomSkinMotion;
			if(motion->load(path)){
				mesh->setMotion(motion);
			}
			motion->drop();
		}
	}
#endif

    device->getCursorControl()->setVisible(false);

    irr::u32 last=device->getTimer()->getRealTime();
    while(device->run())
    {
        // draw
        device->getVideoDriver()->beginScene(true, true, 0xFF6060FF);
		renderer.drawAll(device->getSceneManager());
        device->getVideoDriver()->endScene();

        // fixed FPS. wait for next frame
        while(true){
            irr::u32 current=device->getTimer()->getRealTime();
            if(current-last>MSPF){
                last=current;
                break;
            }
            device->sleep(1);
        }
    }

	return 0;
}

