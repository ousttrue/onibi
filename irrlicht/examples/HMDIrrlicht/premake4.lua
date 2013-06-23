-- A project defines one build target
project "HMDIrrlicht"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "*.cpp", "*.h",
}
includedirs {
    "../../../../../_oculus/TinyRoom/LibOVR/include",
}
libdirs {
    "../../../../../_oculus/TinyRoom/debug",
}
links {
    "Irrlicht",
    "LibOVR",
    "setupapi",
    "winmm",
}

