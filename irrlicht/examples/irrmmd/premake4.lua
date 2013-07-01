------------------------------------------------------------------------------
-- sample
------------------------------------------------------------------------------
-- A project defines one build target
project "irrmmd_sample"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "*.h", "*.cpp",
    "../../../bullet/LinearMath/btVector3.cpp",
}
flags {
	"NoIncrementalLink",
    "FloatFast",
}
defines {
    'FREEGLUT_STATIC',
}
includedirs {
    "../../irrext/irrmmd",
    "../../irrext/libpolymesh",
    "../../irrext/rigid",
    "../../../bullet",
    "../../../glew/include",
    "../../../freeglut/include",
}
defines {
	"NOMINMAX",
}
linkoptions {
}
libdirs {
}
links {
	"irrmmd", "libpolymesh",
    "BulletDynamics", "BulletCollision", "LinearMath",
    "Irrlicht",
    "glew32", "glut32", "OPENGL32",
    "Shlwapi", "gdi32", "winmm",
}

