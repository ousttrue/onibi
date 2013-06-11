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
files { "*.h", "*.cpp" }
flags {
	"NoIncrementalLink",
}
buildoptions {
	"/wd4996",
}
defines {
    'FREEGLUT_STATIC',
}
includedirs {
    "../../../bullet",
    "../../../irrmmd/irrmmd",
    "../../../irrmmd/libpolymesh",
    "../../../irrmmd/rigid",
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
    "Irrlicht",
	"vfw32", "glew32",
    "glut32",
	"irrmmd", "libpolymesh",
    "BulletCollision", 
    "BulletDynamics", 
    "LinearMath",
}

