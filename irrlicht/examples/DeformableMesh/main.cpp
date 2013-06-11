#include <irrlicht.h>
#include <iostream>
#include "SDeformableMesh.h"
#include "SSkeleton.h"
#include "SSkeletalMeshDeformer.h"
#include "SSkeletonMotion.h"
#include <cassert>
#include <iostream>
#include <meshio.h>
 
#ifdef _MSC_VER
#define _USE_MATH_DEFINES
#endif
#include <cmath>

#define MEDIA_PATH "../../media/"
#define PMD_PATH "../../media/"
#define PMD_FILE "../../media/miku.pmd"
#define VMD_FILE "../../media/miku.vmd"
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
		return false;
	}

};
}


unsigned char toByte(float num)
{
    unsigned char n=num * 255;
    if(n<0)
        return 0;
    if(n>255)
        return 255;
    return n;
}

irr::scene::IMesh *createTriangle()
{
    using namespace irr;

    scene::SMeshBuffer *buf = new scene::SMeshBuffer();

    buf->Vertices.set_used(3);

    {
        video::S3DVertex& v = buf->Vertices[0];
        v.Pos.set(-10, 0, 0);
        v.Normal.set(0, 0, -1);
        v.Color.set(255, 255, 0, 0);
        v.TCoords.set(0, 0);
    }
    {
        video::S3DVertex& v = buf->Vertices[1];
        v.Pos.set(10, 0, 0);
        v.Normal.set(0, 0, -1);
        v.Color.set(255, 0, 255, 0);
        v.TCoords.set(0, 0);
    }
    {
        video::S3DVertex& v = buf->Vertices[2];
        v.Pos.set(0, 10, 0);
        v.Normal.set(0, 0, -1);
        v.Color.set(255, 0, 0, 255);
        v.TCoords.set(0, 0);
    }

    /*
    scene::SMesh *mesh = new scene::SMesh();
    // create new buffer
    mesh->addMeshBuffer(buf);
    // to simplify things we drop here but continue using buf
    buf->drop();
    */
    scene::SDeformableMesh *mesh = new scene::SDeformableMesh(buf);
    {
        scene::SSharedMeshBuffer *buf = mesh->createIndexBuffer();
        buf->Indices.set_used(3);
        buf->Indices[0]=0;
        buf->Indices[1]=1;
        buf->Indices[2]=2;
        buf->recalculateBoundingBox();
    }

    return mesh;
}

irr::scene::SDeformableMesh *loadPMD(irr::video::IVideoDriver *driver, const char *file)
{
    using namespace irr;

    // load pmd model
    meshio::pmd::IO pmd;
    if(!pmd.read(file)){
        std::cout << "fail to read " << file << std::endl;
        return 0;
    }
    std::cout << pmd << std::endl;

	// vertices
    scene::SMeshBuffer *vertexBuffer=new scene::SMeshBuffer;
    vertexBuffer->Vertices.set_used(pmd.vertices.size());
    core::array<scene::SBoneWeight> boneWeights;
    boneWeights.reallocate(pmd.vertices.size());
    int i=0;
    for(auto v=pmd.vertices.begin(); v!=pmd.vertices.end(); ++v, ++i){
        vertexBuffer->Vertices[i]=video::S3DVertex(
                v->pos.x, v->pos.y, v->pos.z,
                v->normal.x, v->normal.y, v->normal.z,
                video::SColor(255, 255, 255, 255), // white
                v->uv.x, v->uv.y);
        // [0, 100] to [0, 1.0]
        boneWeights.push_back(
                scene::SBoneWeight(v->bone0, v->bone1, v->weight0*0.01f));
    }
	vertexBuffer->recalculateBoundingBox();

    scene::SDeformableMesh *mesh=
        new scene::SDeformableMesh(vertexBuffer);

    // index
    typedef std::map<io::path, video::ITexture*> TEXTURE_MAP;
	TEXTURE_MAP texture_map;
    auto indices=pmd.indices.begin();
    for(auto m=pmd.materials.begin(); m!=pmd.materials.end(); ++m){
        // each material has indexBuffer.
        video::SColor diffuse(toByte(m->diffuse.a),
                toByte(m->diffuse.r), 
                toByte(m->diffuse.g),
                toByte(m->diffuse.b));
        video::SColor ambient(255,
                toByte(m->ambient.r),
                toByte(m->ambient.g),
                toByte(m->ambient.b));
        video::SColor specular(255,
                toByte(m->specular.r),
                toByte(m->specular.g),
                toByte(m->specular.b));
        // sharing vertexBuffer.
        scene::SSharedMeshBuffer *indexBuffer=mesh->createIndexBuffer();
        // store triangle indices
        for(size_t j=0; j<m->vertex_count; ++j, ++indices){
            indexBuffer->Indices.push_back(*indices);
            mesh->getDeformedBuffer()->Vertices[*indices].Color=diffuse;
            mesh->getVertexBuffer()->Vertices[*indices].Color=diffuse;
        }
        // setup material
        video::SMaterial &material=indexBuffer->Material;
        material.DiffuseColor=diffuse;
        material.AmbientColor=ambient;
        material.SpecularColor=specular;
        material.Shininess=m->shinness;

        material.GouraudShading=false;
        material.Lighting=true;
        //material.BackfaceCulling=false;

        std::string texture_file=m->texture.str();
        if(texture_file!=""){
            // setup texture
            io::path texture_path(texture_file.c_str());
            texture_path.replace(L'\\', L'/');

            TEXTURE_MAP::iterator found=texture_map.find(texture_path);
            video::ITexture *texture=0;
            if(found==texture_map.end()){
                texture=
                    driver->getTexture(texture_path);
                if(texture){
                    texture_map.insert(std::make_pair(texture_path, texture));
                }
                else{
                    std::wcout << "fail to load: " 
                        << texture_path.c_str() << std::endl;
                }
            }
            else{
                texture=found->second;
            }
            material.setTexture(0, texture);
            material.MaterialType=
                video::EMT_TRANSPARENT_ALPHA_CHANNEL_REF;
        }
    }

	// bones
    {
        scene::SSkeleton *skeleton=new scene::SSkeleton;
        for(auto b=pmd.bones.begin(); b!=pmd.bones.end(); ++b){
            skeleton->createBone(
                    core::stringc(b->name.str().c_str()),
                    core::vector3df(b->pos.x, b->pos.y, b->pos.z));
        }
        // build herarchy
        size_t i=0;
        for(auto b=pmd.bones.begin(); b!=pmd.bones.end(); ++b, ++i){
            scene::SBone *bone=skeleton->getBone(i);
            scene::SBone *parent=(b->parent_index==0xFFFF) ?
                skeleton->getBone(0) : skeleton->getBone(b->parent_index);
            if(i>0){
                parent->addChild(bone);
            }
        }
        mesh->addDeformer(new scene::SSkeletalMeshDeformer(boneWeights, skeleton));
    }

    return mesh;
}

irr::scene::SSkeletonMotion *createMotion(const meshio::vmd::IO &vmd)
{
    using namespace irr;

    scene::SSkeletonMotion *motion=new scene::SSkeletonMotion;
    for(auto it=vmd.boneMap.begin();
            it!=vmd.boneMap.end();
            ++it){
        scene::SRotPosLinearCurve *curve=motion->addCurve(it->first.c_str());
        meshio::vmd::BoneKeyFrameList *buf=it->second;
        curve->reallocate(buf->size());
        for(auto frame=buf->begin(); frame!=buf->end(); ++frame){
            meshio::vmd::BoneKey &key=frame->key;
            curve->addKeyFrame(frame->frame,
                    scene::SRotPosKey(
                        core::vector3df(key.pos.x, key.pos.y, key.pos.z),
                        core::quaternion(
                            key.q.x, key.q.y, key.q.z, key.q.w))
                    );
        }
        curve->sort();
    }

    return motion;
}

///////////////////////////////////////////////////////////////////////////////
// entry point
///////////////////////////////////////////////////////////////////////////////
int main(int argc, char **argv)
{
	using namespace irr;

	IrrlichtDevice *device = createDevice(
			video::EDT_OPENGL,
			core::dimension2d<u32>(WIDTH, HEIGHT), 16, false, false, false);
    scene::ISceneManager* smgr = device->getSceneManager();
    video::IVideoDriver *driver=device->getVideoDriver();
	assert(device);
	device->setWindowCaption(L"Deformable Mesh Sample");

	MyReceiver *receiver=new MyReceiver(device);
	device->setEventReceiver(receiver);
	device->setResizable(true);

    {
        // load pmd model
        device->getFileSystem()->addFileArchive(PMD_PATH); 
        scene::SDeformableMesh *mesh=loadPMD(driver, PMD_FILE);
        if(!mesh){
            return 1;
        }

        // load vmd motion
        meshio::vmd::IO vmd;
        if(!vmd.read(VMD_FILE)){
            std::cout << "fail to read " << VMD_FILE << std::endl;
            return 2;
        }

        if(mesh->getSkeletalMeshDeformer()){
            mesh->getSkeletalMeshDeformer()->addMotion(createMotion(vmd));
        }

        // set default material properties
        scene::IAnimatedMeshSceneNode* node = 
            smgr->addAnimatedMeshSceneNode(mesh);
        node->setAnimationSpeed(30);
        node->setMaterialFlag(video::EMF_LIGHTING, false);
        node->setMaterialFlag(video::EMF_BACK_FACE_CULLING, false);
        //node->setDebugDataVisible(scene::EDS_OFF);
    }

    /*
    {
        scene::IMeshSceneNode* node = smgr->addMeshSceneNode(createTriangle());
        node->setMaterialFlag(video::EMF_BACK_FACE_CULLING, false);
    }
    */

	// custom camera
	scene::ICameraSceneNode* camera= 
        smgr->addCameraSceneNodeMaya();
	camera->setFOV(static_cast<f32>(M_PI*30.0/180.0));
	camera->setNearValue(1.0f);
	//camera->setFarValue(5000.0f);
	camera->setFarValue(20000.f);
	camera->setTarget(core::vector3df(0, 10, 0));
	// Maya cameras reposition themselves relative to their target, so target the location
	// where the mesh scene node is placed.


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
			smgr->addSkyBoxSceneNode(
					device->getVideoDriver()->getTexture("irrlicht2_up.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_dn.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_lf.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_rt.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_ft.jpg"),
					device->getVideoDriver()->getTexture("irrlicht2_bk.jpg"));
	}
	{
		scene::IAnimatedMesh *planemesh = 
			smgr->addHillPlaneMesh("myHill", 
					core::dimension2d<f32>(24, 24), 
					core::dimension2d<u32>(100, 100));
		scene::ISceneNode *q3sn = smgr->
			addOctTreeSceneNode(planemesh);
		//q3sn->setMaterialFlag(video::EMF_LIGHTING, false);
		q3sn->setMaterialTexture(0, device->getVideoDriver()->getTexture(MEDIA_PATH "wall.jpg"));
	}
	{
		// create light
		scene::ISceneNode* light 
			= smgr->addLightSceneNode(camera, 
					core::vector3df(100, 100, -100), 
					video::SColorf(100.0, 100.0, 100.0, 0.0), 1500.0f);
	}

    /*
	////////////////////////////////////////////////////////////
	// load pmd model and vmd motion
	////////////////////////////////////////////////////////////
	// setup custom loader
	irrMMDsetup(device);

	// load 
	scene::IMotionedMesh *mesh=0;
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
            std::cout << mesh << std::endl;
			mesh=(scene::IMotionedMesh*)
					receiver->loadMesh(path);
            std::cout << mesh << std::endl;
		}
		else if(core::hasFileExtension(path, "vmd")){
			scene::IMotion *motion=scene::createVMDMotion();
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
    */

	{
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
			smgr->drawAll();
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

