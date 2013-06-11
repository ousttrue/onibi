-- A project defines one build target
project "libpolymesh"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C++"
files { "**.h", "**.cpp" }
excludes { "*_test.cpp" }
flags {}
buildoptions {}
defines {}
includedirs {
  "../rigid",
}
linkoptions {}
libdirs {}
links {}

