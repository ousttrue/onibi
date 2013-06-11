#include <irrlicht.h>
#include <cassert>
#include <iostream>

#ifdef _MSC_VER
#define _USE_MATH_DEFINES
#endif
#include <math.h>

#include "irrMMD.h"
#include "CAviCreator.h"

#define MEDIA_PATH "../../media/"
#define WIDTH 640
#define HEIGHT 480

namespace irr {

// frame per second
static const u32 FPS=30;
// milli sec per frame
static const u32 MSPF=1000/FPS;

class MyReceiver: public IEventReceiver
{
	IrrlichtDevice *device_;
	scene::ISceneNode* node_;

public:
	MyReceiver(IrrlichtDevice *device)
		: device_(device), node_(0)
		{
		}

	virtual bool OnEvent(const SEvent& event)
	{
		if (event.EventType == EET_KEY_INPUT_EVENT &&
				event.Info.KeyInput.PressedDown){
			switch(event.Info.KeyInput.Key)
			{
			case 'O':
				device_->getGUIEnvironment()->addFileOpenDialog(
						L"Please select a model file to open");
				break;

			case 27: // ESCAPE
			case 'Q': // fall through
				device_->closeDevice();
				break;

			default:
				std::cout << event.Info.KeyInput.Key << std::endl;
			}
		}
		else if (event.EventType == EET_GUI_EVENT){
			if(event.Info.GUIEvent.EventType==gui::EGET_FILE_SELECTED){
				// load the model file, selected in the file open dialog
				gui::IGUIFileOpenDialog* dialog =
					(gui::IGUIFileOpenDialog*)event.Info.GUIEvent.Caller;
				scene::IAnimatedMesh *m=loadMesh(dialog->getFileName());
				if(m){
					setMesh(m);
				}
			}
		}

		return false;
	}

	scene::IAnimatedMesh* loadMesh(const io::path &filename)
	{
		io::path extension;
		core::getFileNameExtension(extension, filename);
		extension.make_lower();

		// if a texture is loaded apply it to the current model..
		if (extension == ".jpg" || extension == ".pcx" ||
				extension == ".png" || extension == ".ppm" ||
				extension == ".pgm" || extension == ".pbm" ||
				extension == ".psd" || extension == ".tga" ||
				extension == ".bmp" || extension == ".wal")
		{
			video::ITexture * texture =
				device_->getVideoDriver()->getTexture(filename.c_str());
			if ( texture && node_ )
			{
				// always reload texture
				device_->getVideoDriver()->removeTexture(texture);
				texture = device_->getVideoDriver()->getTexture( filename.c_str() );

				node_->setMaterialTexture(0, texture);
			}
			return 0;
		}
		// if a archive is loaded add it to the FileSystems..
		else if (extension == ".pk3" || extension == ".zip")
		{
			device_->getFileSystem()->addFileArchive(filename);
			return 0;
		}
		else if (extension == ".pak")
		{
			device_->getFileSystem()->addFileArchive(filename);
			return 0;
		}

		// load a model into the engine
		if (node_){
			node_->remove();
			node_ = 0;
		}

		return device_->getSceneManager()->getMesh( filename.c_str() );
	}

	void setMesh(scene::IAnimatedMesh *m)
	{
		if(!m){
			return;
		}
		// set default material properties
		scene::IAnimatedMeshSceneNode* node = 
			device_->getSceneManager()->addAnimatedMeshSceneNode(m);
		node->setAnimationSpeed(30);
		node_ = node;
		node_->setMaterialFlag(video::EMF_LIGHTING, false);
		//  Model->setMaterialFlag(video::EMF_BACK_FACE_CULLING, false);
		node_->setDebugDataVisible(scene::EDS_OFF);
	}

};
}

///////////////////////////////////////////////////////////////////////////////
// entry point
///////////////////////////////////////////////////////////////////////////////
int main(int argc, char **argv)
{
	using namespace irr;

	IrrlichtDevice *device = createDevice(
			video::EDT_OPENGL,
			//video::EDT_DIRECT3D9,
			core::dimension2d<u32>(WIDTH, HEIGHT), 16, false, false, false);
	assert(device);
	device->setWindowCaption(L"Irrlicht");

	// event receiver
	MyReceiver *receiver=new MyReceiver(device);
	device->setEventReceiver(receiver);
	device->setResizable(true);

	////////////////////////////////////////////////////////////
	// setup scene
	////////////////////////////////////////////////////////////
	// custom camera
	scene::ICameraSceneNode* camera= 
		scene::irrMMDaddRokuroCamera(device, 100.0f);
	camera->setFOV(static_cast<f32>(M_PI*30.0/180.0));
	camera->setNearValue(1.0f);
	camera->setFarValue(5000.0f);
	camera->setTarget(core::vector3df(0, 10, 0));

	// load the irrlicht engine logo
	device->getFileSystem()->addFileArchive(MEDIA_PATH);

	gui::IGUIImage *img =
		device->getGUIEnvironment()->addImage(
				device->getVideoDriver()->getTexture("irrlichtlogo2.png"),
				core::position2d<s32>(
					10, device->getVideoDriver()->getScreenSize().Height - 128));

	{
		// add skybox
		scene::ISceneNode* SkyBox = 
			device->getSceneManager()->addSkyBoxSceneNode(
					device->getVideoDriver()->getTexture("irrlicht2_up.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_dn.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_lf.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_rt.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_ft.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_bk.jpg"));
	}
	{
		scene::IAnimatedMesh *planemesh = 
			device->getSceneManager()->addHillPlaneMesh("myHill", 
					core::dimension2d<f32>(24, 24), 
					core::dimension2d<u32>(100, 100));
		scene::ISceneNode *q3sn = device->getSceneManager()->
			addOctTreeSceneNode(planemesh);
		//q3sn->setMaterialFlag(video::EMF_LIGHTING, false);
		q3sn->setMaterialTexture(0, device->getVideoDriver()->getTexture(MEDIA_PATH "wall.jpg"));
	}
	{
		// create light
		scene::ISceneNode* light 
			= device->getSceneManager()->addLightSceneNode(camera, 
					core::vector3df(100, 100, -100), 
					video::SColorf(100.0, 100.0, 100.0, 0.0), 1500.0f);
	}

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

	if(mesh){
		// create SceneNode
		receiver->setMesh(mesh);
	}


	{
		/*
		if (glewInit()!=GLEW_OK){
			return 1;
		}
		CAviCreator avi(WIDTH, HEIGHT, "tmp.avi", 1, 30);
		*/

		u32 last=device->getTimer()->getRealTime();
		while(device->run())
		{
			// update aspect ratio
			core::dimension2d<u32> size=
				device->getVideoDriver()->getScreenSize();
			float aspect=(float)size.Width/(float)size.Height;
			camera->setAspectRatio(aspect);

			// draw
			device->getVideoDriver()->beginScene(true, true, 0xFF6060FF);
			device->getSceneManager()->drawAll();
			device->getGUIEnvironment()->drawAll();
			//avi.CaptureWindow();

			// fixed FPS. wait for next frame
			while(true){
				u32 current=device->getTimer()->getRealTime();
				if(current-last>MSPF){
					last=current;
					break;
				}
				device->sleep(1);
			}

			device->getVideoDriver()->endScene();
		}
	}
	device->drop();

	return 0;
}

