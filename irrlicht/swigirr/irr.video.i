%module(package="irr", directors="1") "video"
%{
#include "Irrlicht.h"
using namespace irr;
using namespace core;
using namespace video;
using namespace gui;
using namespace scene;
#include <vector>
#include <algorithm>
%}
%feature("director") irr::video::IShaderConstantSetCallBack;

%include "irr.common.i"
%import "irr.core.i"


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

%include "SColor.h"
%include "IImage.h"
%include "ITexture.h"
%include "EDriverTypes.h"
%include "EMaterialTypes.h"
%include "EMaterialFlags.h"
%include "SMaterialLayer.h"
%include "SMaterial.h"
%include "S3DVertex.h"
%include "SVertexIndex.h"
%include "EHardwareBufferFlags.h"
%include "EDriverFeatures.h"
%include "SExposedVideoData.h"
%include "IVideoDriver.h"
%include "IVideoModeList.h"
%include "IVertexBuffer.h"
%include "ECullingTypes.h"
%include "EDriverTypes.h"
%include "EMaterialFlags.h"
%include "EMaterialTypes.h"
%include "EShaderTypes.h"
%include "IGPUProgrammingServices.h"
%include "IImage.h"
%include "IImageLoader.h"
%include "IImageWriter.h"
%include "ILogger.h"
%include "IMaterialRenderer.h"
%include "IMaterialRendererServices.h"
%include "IShaderConstantSetCallBack.h"
%include "SLight.h"
%include "irrArray.h"
%include "EPrimitiveTypes.h"

//////////////////////////////////////////////////////////////////////////////
// templates
//////////////////////////////////////////////////////////////////////////////
%template(S3DVertexArray) irr::core::array<irr::video::S3DVertex>;
%extend irr::core::array<irr::video::S3DVertex> {
  irr::video::S3DVertex &__getitem__(irr::u16 i) {
    return (*$self)[i];
  };
};


//////////////////////////////////////////////////////////////////////////////
// extends
//////////////////////////////////////////////////////////////////////////////
%extend irr::video::SMaterial {

SMaterialLayer &getTextureLayer(int index) {
    return $self->TextureLayer[index];
}

};

%extend irr::video::S3DVertex2TCoords {

static S3DVertex2TCoords *cast(void* data) {
    return (S3DVertex2TCoords*)data;
}

};


