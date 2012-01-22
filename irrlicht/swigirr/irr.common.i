//////////////////////////////////////////////////////////////////////////////
// wchar_t
//////////////////////////////////////////////////////////////////////////////
%typemap(in) const wchar_t * const {
   $1 = PyUnicode_AS_UNICODE($input);
}
%typemap(in) const wchar_t * {
   $1 = PyUnicode_AS_UNICODE($input);
}
%typemap(out) const wchar_t * {
   $result = PyUnicode_FromUnicode($1, wcslen($1));
}
%typemap(typecheck) const wchar_t * {
   $1 = PyUnicode_Check($input) ? 1 : 0;
}

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
// irr::core::string
// irr::core::stringc
// irr::io::path
// irr::core::stringw
//////////////////////////////////////////////////////////////////////////////
%ignore irr::core::string::operator+=;

%typemap(in) irr::core::stringc* (irr::core::stringc temp) {
    temp=irr::core::stringc(PyString_AS_STRING($input));
    $1=&temp;
}
%typemap(typecheck) irr::core::stringc* = const char *;

%typemap(in) const irr::io::path&(irr::io::path temp) {
   temp=irr::io::path(PyString_AS_STRING($input));
   $1 = &temp;
}
%typemap(typecheck) const irr::io::path & = const char *;

%typemap(in) irr::core::stringw const &(irr::core::stringw temp) {
    temp=irr::core::stringw(PyUnicode_AS_UNICODE($input));
    $1=&temp;
}
%typemap(typecheck) const irr::core::stringw& = const wchar_t *;

//////////////////////////////////////////////////////////////////////////////
// irr::core::array
//////////////////////////////////////////////////////////////////////////////
/*
%typemap(in) const irr::core::array<video::ITexture*>& textures(irr::core::array<video::ITexture*> temp) {
    if (PySequence_Check($input)) {
        temp.reallocate(PySequence_Size($input));
        if(temp.empty()){
            $1=0;
        }
        else{
            for (size_t i =0; i<temp.size(); ++i) {
                PyObject *o = PySequence_GetItem($input, i);
                irr::video::ITexture *t;
                if (SWIG_ConvertPtr(o, 
                (void **) &t, SWIGTYPE_p_irr__video__ITexture, SWIG_POINTER_EXCEPTION) == -1){
                    return NULL;
                }
                temp[i]=t;
            }
        }
        $1=&temp;
    }
    else {
        PyErr_SetString(PyExc_TypeError,"not a sequence");
        return NULL;
    }
}
*/

%typemap(in) (const void* vertices, irr::u32 vertexCount)(irr::core::array<irr::video::S3DVertex> temp){
    if (PySequence_Check($input)) {
        $2=PySequence_Size($input);
        if($2==0){
            $1=0;
        }
        else{
            temp.reallocate($2);
            for (size_t i =0; i<temp.size(); ++i) {
                PyObject *o = PySequence_GetItem($input, i);
                irr::video::S3DVertex *v;
                if (SWIG_ConvertPtr(o, 
                (void **) &v, SWIGTYPE_p_irr__video__S3DVertex, SWIG_POINTER_EXCEPTION) == -1){
                    return NULL;
                }
                temp[i]=*v;
            }
            $1=temp.pointer();
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError,"not a sequence");
        return NULL;
    }
}

%typemap(in) (const void* indexList, irr::u32 primCount)(irr::core::array<irr::u16> temp){
    if (PySequence_Check($input)) {
        $2=PySequence_Size($input);
        if($2==0){
            $1=0;
        }
        else{
            temp.reallocate($2);
            $2/=3;
            for (size_t i =0; i<temp.size(); ++i) {
                PyObject *o = PySequence_GetItem($input, i);
                temp[i]=PyLong_AsSsize_t(o);
            }
            $1=temp.pointer();
        }
    }
    else {
        PyErr_SetString(PyExc_TypeError,"not a sequence");
        return NULL;
    }
}

%typemap(out) irr::core::array<irr::scene::ISceneNode*> {
    irr::core::array<irr::scene::ISceneNode*> &src=$1;
    $result=PyList_New(src.size());
    for(size_t i=0; i<src.size(); ++i){
        PyList_SetItem($result, i,
                SWIG_NewPointerObj(src[i], $descriptor(irr::scene::ISceneNode*), 0));
    }
}

%typemap(out) irr::core::array<irr::SJoystickInfo> {
    irr::core::array<irr::SJoystickInfo> &src=$1;
    $result=PyList_New(src.size());
    for(size_t i=0; i<src.size(); ++i){
        irr::SJoystickInfo *p=new irr::SJoystickInfo();
        *p=src[i];
        PyList_SetItem($result, i,
                SWIG_NewPointerObj(p, $descriptor(irr::SJoystickInfo*), 1));
    }
}

//////////////////////////////////////////////////////////////////////////////
// irr::video::SColor
// irr::video::SColorf
//////////////////////////////////////////////////////////////////////////////
%typemap(typecheck) irr::video::SColorf const & {
void *ptr;
if (SWIG_ConvertPtr($input, (void **) &ptr, $descriptor(irr::video::SColorf *), 0) == -1
        && SWIG_ConvertPtr($input, (void **) &ptr, $descriptor(irr::video::SColor *), 0) == -1) {
    $1 = 0;
    PyErr_Clear();
} else {
    $1 = 1;
}
}
%typemap(in) irr::video::SColorf const &(irr::video::SColorf temp) {
void *ptr;
if (SWIG_ConvertPtr($input,(void **) &ptr, 
            $descriptor(irr::video::SColorf *),SWIG_POINTER_EXCEPTION) != -1){
    // OK
    $1 = (irr::video::SColorf *)ptr;
}
else if(SWIG_ConvertPtr($input,(void **) &ptr, 
            $descriptor(irr::video::SColor *),SWIG_POINTER_EXCEPTION) != -1){
    // convert to SColorf from SColor
    temp = irr::video::SColorf(*((irr::video::SColor *)ptr));
    $1 = &temp;
}
else {
    return NULL;
}
}


//////////////////////////////////////////////////////////////////////////////
// MinGW build
//////////////////////////////////////////////////////////////////////////////
#define __GNUC__

