-- A project defines one build target
project "PmdAndVmd"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "main.cpp",
}
flags { 
    --"StaticRuntime", 
    "Unicode", 
}
buildoptions {}

configuration "windows"
do
    defines {
        "WIN32",
        "_WINDOWS",
    }
end

includedirs {
    "../../../irrlicht/include",
    "../../../glew/include",
}
links {
    "Irrlicht",
}

configuration "gmake"
do
    buildoptions { "-Wall", "-std=c++0x", "-U__STRICT_ANSI__", "-g",}
    linkoptions { "-g", }
end

configuration "vs*"
do
    defines {
        "_CRT_SECURE_NO_DEPRECATE",
    }
    buildoptions { "/wd4996" }
end

configuration "Debug"
do
    defines { "DEBUG" }
    flags { "Symbols" }
    libdirs {
        "../../../debug",
    }
    targetdir "../../../debug"
end

configuration "Release"
do
  defines { "NDEBUG" }
  flags { "Optimize" }
  targetdir "../../../release"
  libdirs {
    "../../../release",
  }
end

