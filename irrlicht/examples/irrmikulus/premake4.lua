-- A project defines one build target
project "irrmikulus"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "*.cpp", "*.h",
    "../HMDIrrlicht/CSceneNodeAnimatorCameraOculusOnFPS.*",
    "../HMDIrrlicht/HMDStereoRender.*",
    "../../../bullet/LinearMath/btVector3.cpp",
}
includedirs {
    "../HMDIrrlicht",
    "../../../../../_oculus/TinyRoom/LibOVR/include",

    "../../../bullet",
    "../../../irrmmd/irrmmd",
    "../../../irrmmd/libpolymesh",
    "../../../irrmmd/rigid",
    "../../../glew/include",
    "../../../freeglut/include",
}
libdirs {
    "../../../../../_oculus/TinyRoom/debug",
}
links {
    "Irrlicht",
    "OVR",
    "setupapi",
    "winmm",

	"vfw32", "glew32",
    "glut32",
	"irrmmd", "libpolymesh",
    "BulletCollision", 
    "BulletDynamics", 
    "LinearMath",
}

