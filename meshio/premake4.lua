-- A project defines one build target
project "meshio"
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
}
linkoptions {}
libdirs {}
links {}

configuration "gmake"
do
  buildoptions { "-Wall", "-std=c++0x", "-U__STRICT_ANSI_", }
end

configuration "vs*"
do
  buildoptions { "/wd4996" }
end

configuration "windows"
do
    defines {
        "WIN32",
        "_WINDOWS",
    }
end

configuration "Debug"
do
  defines { "DEBUG" }
  flags { "Symbols" }
  targetdir "../debug"
end

configuration "Release"
do
  defines { "NDEBUG" }
  flags { "Optimize" }
  targetdir "../release"
end

