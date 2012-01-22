-- A project defines one build target
project "13.RenderToTexture"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "main.cpp",
}
includedirs {
    "../../../irrlicht/include"
}
links {
    "Irrlicht"
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
  buildoptions { "-Wall" }
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

