-- A project defines one build target
project "irrmmd"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C++"
files { "*.h", "*.cpp" }
flags {
	"Unicode",
}
defines {
    'FREEGLUT_STATIC',
}
buildoptions {
	"/wd4996",
}
includedirs {
	"../../irrlicht/include",
	"../../irrlicht/include/scene",
	"../../irrlicht/include/io",
	"../../irrlicht/include/video",
    "../../bullet",
    "../../freeglut/include",
    "../../glew/include",
    "../libpolymesh",
    "../rigid",
}
defines {
	"NOMINMAX",
}
linkoptions {
}
libdirs {
}
links {
}

