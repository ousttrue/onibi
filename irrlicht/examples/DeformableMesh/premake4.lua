-- A project defines one build target
project "DeformableMesh"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "*.cpp", "*.h",
}
includedirs {
    "../../../irrlicht/include",
    "../../../meshio",
}
links {
    "Irrlicht",
    "meshio",
}

configuration "windows"
do
    defines {
        "WIN32",
        "_WINDOWS",
    }
end

configuration "gmake"
do
    buildoptions { 
        "-Wall", "-std=c++0x", "-U__STRICT_ANSI__", 
        "-Wno-unused-variable", 
        "-Wno-deprecated-declarations",
        "-Wno-switch",
    }
end

configuration "vs*"
do
  buildoptions { "/wd4996" }
end

configuration "Debug"
do
  defines { "DEBUG" }
  flags { "Symbols" }
  targetdir "../../../debug"
  libdirs {
      "../../../debug"
  }
end

configuration "Release"
do
  defines { "NDEBUG" }
  flags { "Optimize" }
  targetdir "../../../release"
  libdirs {
      "../../../release"
  }
end

