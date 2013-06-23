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
    "../../../irrlicht/include"
}
links {
    "Irrlicht"
}

