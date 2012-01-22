%module(package="irr", directors="1") "scene"
%{
#include "Irrlicht.h"
#include "IQ3Shader.h"
using namespace irr;
using namespace core;
using namespace video;
using namespace gui;
using namespace scene;
%}
%feature("director") irr::scene::ISceneNode;

%include "irr.common.i"
%import "irr.core.i"
%import "irr.video.i"

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
%include "IrrTypes.h"

%include "S3DVertex.h"
%include "EPrimitiveTypes.h"
%include "IMeshBuffer.h"
%include "CMeshBuffer.h"
%include "IIndexBuffer.h"
%include "CIndexBuffer.h"
%include "IDynamicMeshBuffer.h"
%include "CDynamicMeshBuffer.h"
%include "CVertexBuffer.h"
%include "ECullingTypes.h"
%include "EDebugSceneTypes.h"
%include "ESceneNodeAnimatorTypes.h"
%include "ESceneNodeTypes.h"
%include "ETerrainElements.h"
%include "ITriangleSelector.h"
%include "IMetaTriangleSelector.h"
%include "ISceneNodeAnimator.h"
%include "ISceneNode.h"
%include "IMesh.h"
%include "IBoneSceneNode.h"
%include "IAnimatedMesh.h"
%include "IAnimatedMeshMD2.h"
%include "IAnimatedMeshMD3.h"
%include "IAnimatedMeshSceneNode.h"
%include "IBillboardSceneNode.h"
%include "IBillboardTextSceneNode.h"
%include "ICameraSceneNode.h"
%include "IDummyTransformationSceneNode.h"
%include "IDynamicMeshBuffer.h"
%include "IGeometryCreator.h"
%include "ILightSceneNode.h"
%include "IMesh.h"
%include "IMeshBuffer.h"
//%include "IMeshCache.h"
%include "IMeshLoader.h"
%include "IMeshManipulator.h"
%include "IMeshSceneNode.h"
%include "IMeshWriter.h"
%include "SParticle.h"
%include "IParticleEmitter.h"
%include "IParticleAffector.h"
%include "IParticleAnimatedMeshSceneNodeEmitter.h"
%include "IParticleAttractionAffector.h"
%include "IParticleBoxEmitter.h"
%include "IParticleCylinderEmitter.h"
%include "IParticleFadeOutAffector.h"
%include "IParticleGravityAffector.h"
%include "IParticleMeshEmitter.h"
%include "IParticleRingEmitter.h"
%include "IParticleRotationAffector.h"
%include "IParticleSphereEmitter.h"
%include "IParticleSystemSceneNode.h"
%include "ISceneCollisionManager.h"
%include "ISceneNodeAnimatorCameraFPS.h"
%include "ISceneNodeAnimatorCameraMaya.h"
%include "ISceneNodeAnimatorCollisionResponse.h"
%include "ISceneNodeAnimatorFactory.h"
%include "ISceneNodeFactory.h"
%include "ISceneUserDataSerializer.h"
%include "IShadowVolumeSceneNode.h"
%include "ITerrainSceneNode.h"
%include "ITextSceneNode.h"
%include "IVolumeLightSceneNode.h"
%include "SAnimatedMesh.h"
%include "SceneParameters.h"
%include "SMesh.h"
%include "SMeshBuffer.h"
%include "CMeshBuffer.h"
%include "SMeshBufferLightMap.h"
%include "SMeshBufferTangents.h"
%include "SSharedMeshBuffer.h"
%include "SSkinMeshBuffer.h"
%include "SViewFrustum.h"
%include "SSharedMeshBuffer.h"
%include "ISkinnedMesh.h"
%include "ISceneManager.h"
%include "ILightManager.h"
%include "IQ3LevelMesh.h"
%include "IQ3Shader.h"
%include "irrArray.h"

//////////////////////////////////////////////////////////////////////////////
// templates
//////////////////////////////////////////////////////////////////////////////
%template(tQ3EntityList) irr::core::array <irr::scene::quake3::IEntity >;

%template(SMeshBuffer) irr::scene::CMeshBuffer<irr::video::S3DVertex>;
%template(SMeshBufferLightMap) irr::scene::CMeshBuffer<irr::video::S3DVertex2TCoords>;
%template(SMeshBufferTangents) irr::scene::CMeshBuffer<irr::video::S3DVertexTangents>;

//////////////////////////////////////////////////////////////////////////////
// extends
//////////////////////////////////////////////////////////////////////////////
%extend irr::core::array<irr::scene::quake3::IEntity> {

irr::scene::quake3::IEntity get(int index){
    return (*$self)[index];
}

};

%extend irr::scene::ISceneManager {

irr::core::array<irr::scene::ISceneNode*> getSceneNodesFromType(irr::scene::ESCENE_NODE_TYPE t) {
    irr::core::array<irr::scene::ISceneNode*> buf;
    $self->getSceneNodesFromType(t, buf);
    return buf;
}

};

%extend irr::scene::IMeshSceneNode {

static IMeshSceneNode *cast(ISceneNode *node) {
    return (IMeshSceneNode*)node;
}

};

%extend irr::scene::ITerrainSceneNode {

static ITerrainSceneNode *cast(ISceneNode *node) {
    return (ITerrainSceneNode*)node;
}

};

%extend irr::scene::IQ3LevelMesh {

static IQ3LevelMesh *cast(IMesh *mesh) {
    return (IQ3LevelMesh*)mesh;
}

};

%extend irr::scene::CMeshBuffer<irr::video::S3DVertex> {

static irr::scene::CMeshBuffer<irr::video::S3DVertex> *cast(IMeshBuffer *meshBuffer) {
    return (irr::scene::CMeshBuffer<irr::video::S3DVertex>*)meshBuffer;
}

};

