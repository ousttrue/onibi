#include <irrlicht.h>
#include <irrMMD.h>
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
	bool isFullscreen=false;
    // Check fullscreen
    for (int i=1;i<argc;i++) isFullscreen |= !strcmp("-f", argv[i]);

    auto device = std::shared_ptr<irr::IrrlichtDevice>(
            irr::createDevice(
                irr::video::EDT_OPENGL,
                irr::core::dimension2d<irr::u32>(WIDTH, HEIGHT), 
                16, isFullscreen, false, false),
            [](irr::IrrlichtDevice* p){ p->drop(); }
            );
    assert(device);
    auto smgr=device->getSceneManager();
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
    //keymaps.push_back(irr::SKeyMap(irr::EKA_MOVE_UP, irr::KEY_UP));
    keymaps.push_back(irr::SKeyMap(irr::EKA_CROUCH, irr::KEY_DOWN));
    auto camera= irr::scene::CSceneNodeAnimatorCameraOculusOnFPS::addCameraSceneNodeOclusOnFPS(
		smgr, device->getCursorControl(),
			0, 
                80.0f, .1f, -1, 
                keymaps.pointer(), keymaps.size(), 
                true, .5f, false, true);
    camera->setPosition(irr::core::vector3df(0,15, -100));
    camera->setTarget(irr::core::vector3df(0, 15, 0));
    {
		/*
		irr::scene::ISceneNodeAnimator* anim = smgr->createCollisionResponseAnimator(
                0, camera, 
                irr::core::vector3df(30,50,30),
                irr::core::vector3df(0,-10,0), 
                irr::core::vector3df(0,30,0));
        camera->addAnimator(anim);
        anim->drop();  // And likewise, drop the animator when we're done referring to it.
		*/
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
			smgr->addSkyBoxSceneNode(
					device->getVideoDriver()->getTexture("irrlicht2_up.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_dn.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_lf.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_rt.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_ft.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_bk.jpg"));
	}
	{
		auto planemesh = 
			smgr->addHillPlaneMesh("myHill", 
					irr::core::dimension2d<irr::f32>(24, 24), 
					irr::core::dimension2d<irr::u32>(100, 100));
		auto q3sn = smgr->
			addOctreeSceneNode(planemesh);
		//q3sn->setMaterialFlag(video::EMF_LIGHTING, false);
		q3sn->setMaterialTexture(0, device->getVideoDriver()->getTexture(MEDIA_PATH "wall.jpg"));
	}

	{
		// create light
		auto light 
			= smgr->addLightSceneNode(0, 
					irr::core::vector3df(100, 100, -100), 
					irr::video::SColorf(1.0f, 1.0f, 1.0f), 100.0f);
	}

    // load a dwarf
    auto dwarf = smgr->getMesh(MEDIA_PATH "dwarf.x");
    auto dwarfNode = smgr->addAnimatedMeshSceneNode(dwarf);
    dwarfNode->setPosition(irr::core::vector3df(40, 0, 20));

	////////////////////////////////////////////////////////////
	// load pmd model and vmd motion
	////////////////////////////////////////////////////////////
	// setup custom loader
    irr::irrMMDsetup(device.get(), 1.0f);

    auto mesh=dynamic_cast<irr::scene::CCustomSkinnedMesh*>(
            smgr->getMesh(MEDIA_PATH "model.pmd"));
    if(mesh){
        std::shared_ptr<irr::scene::CVMDCustomSkinMotion> motion(
			new irr::scene::CVMDCustomSkinMotion,
            [](irr::scene::CVMDCustomSkinMotion *p){ p->drop(); }
            );
        if(motion->load(MEDIA_PATH "motion.vmd")){
            mesh->setMotion(motion.get());
        }

		auto node = smgr->addAnimatedMeshSceneNode(mesh);
		node->setAnimationSpeed(30);
		//node->setMaterialFlag(irr::video::EMF_LIGHTING, false);
		//Model->setMaterialFlag(video::EMF_BACK_FACE_CULLING, false);
		//node->setDebugDataVisible(scene::EDS_OFF);
    }

    device->getCursorControl()->setVisible(false);

    irr::u32 last=device->getTimer()->getRealTime();
    while(device->run())
    {
        // draw
        device->getVideoDriver()->beginScene(true, true, 0xFF6060FF);
		renderer.drawAll(smgr);
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

