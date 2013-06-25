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
}
includedirs {
    "../HMDIrrlicht",
    "../../../../../_oculus/TinyRoom/LibOVR/include",
}
libdirs {
    "../../../../../_oculus/TinyRoom/debug",
}
links {
    "Irrlicht",
    "OVR",
    "setupapi",
    "winmm",
}

