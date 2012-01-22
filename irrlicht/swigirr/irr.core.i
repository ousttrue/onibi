%module(package="irr") "core"
%{
#include "Irrlicht.h"
using namespace irr;
using namespace core;
using namespace video;
using namespace gui;
using namespace scene;
%}

%feature("ref")   irr::IReferenceCounted "$this->grab();"
%feature("unref") irr::IReferenceCounted "$this->drop();"

%include "irr.common.i"
%import "irr.gui.i"

%ignore irr::core::string::operator+=;
%fragment("SWIG_AsVal_wchar_t", "header", fragment="<wchar.h>") {
    SWIGINTERN int SWIG_AsVal_wchar_t(PyObject* p, wchar_t* c) {
        return SWIG_OK;
    }
}
%fragment("SWIG_From_wchar_t", "header", fragment="<wchar.h>") {
    SWIGINTERNINLINE PyObject* SWIG_From_wchar_t(wchar_t c) {
        return SWIG_Py_Void();
    }
}

//////////////////////////////////////////////////////////////////////////////
// Irrlicht headers
//////////////////////////////////////////////////////////////////////////////
%include "IrrCompileConfig.h"
%include "IReferenceCounted.h"
%include "irrTypes.h"
%include "aabbox3d.h"
%include "rect.h"
%include "irrMath.h"
%include "dimension2d.h"
%include "matrix4.h"
%include "irrArray.h"
%include "plane3d.h"
%include "position2d.h"
%include "triangle3d.h"
%include "irrAllocator.h"
%include "fast_atof.h"
%include "heapsort.h"
%include "vector3d.h"
%include "vector2d.h"
%include "line2d.h"
%include "line3d.h"
%include "triangle3d.h"
%include "rect.h"
%include "matrix4.h"
%include "quaternion.h"
%include "plane3d.h"
%include "triangle3d.h"
%include "irrString.h"
%include "irrList.h"
%include "irrMap.h"
%include "line2d.h"

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
// templates
//////////////////////////////////////////////////////////////////////////////
%template(dimension2df) irr::core::dimension2d<float>;
%template(dimension2di) irr::core::dimension2d<int>;
%template(dimension2du) irr::core::dimension2d<unsigned int>;
%template(recti) irr::core::rect<int>;
%template(_stringc) irr::core::string<char>;
%template(_stringw) irr::core::string<wchar_t>;
%template(vector3df) irr::core::vector3d<float>;
%template(aabbox3df) irr::core::aabbox3d<float>;
%template(position2di) irr::core::position2d<int>;
%template(position2df) irr::core::position2d<float>;
%template(line3di) irr::core::line3d<int>;
%template(line3df) irr::core::line3d<float>;
%template(triangle3di) irr::core::triangle3d<int>;
%template(triangle3df) irr::core::triangle3d<float>;
%template(matrix4) irr::core::CMatrix4<float>;
%template(plane3di) irr::core::plane3d<int>;
%template(plane3df) irr::core::plane3d<float>;
%template(U16Array) irr::core::array<irr::u16>;
%extend irr::core::array<irr::u16> {
  void __setitem__(irr::u32 i, irr::u16 v) {
    (*$self)[i]=v;
  };
};

