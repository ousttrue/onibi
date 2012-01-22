%module(package="irr") "io"
%{
#include "Irrlicht.h"
#include "IAttribute.h"
using namespace irr;
using namespace io;
using namespace core;
using namespace video;
using namespace gui;
using namespace scene;
%}

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
%include "path.h"
%include "IFileList.h"
//%include "IReadFile.h"
//%include "IXMLReader.h"
%include "IFileArchive.h"
%include "IFileSystem.h"
%include "IAttribute.h"
%include "IAttributes.h"
