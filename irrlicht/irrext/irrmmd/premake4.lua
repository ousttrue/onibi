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
includedirs {
    "../libpolymesh",
    "../rigid",
	"../../include",
	"../../include/scene",
	"../../include/io",
	"../../include/video",
    "../../../bullet",
    "../../../freeglut/include",
    "../../../glew/include",
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

