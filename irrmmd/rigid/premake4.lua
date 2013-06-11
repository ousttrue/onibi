-- A project defines one build target
project "rigid"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C++"
files { "**.h", "**.cpp" }
excludes { "main.cpp" }
flags {}
buildoptions {}
defines {}
linkoptions {}
libdirs {}

