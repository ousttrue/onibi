-- A solution contains projects, and defines the available configurations
solution "Dependencies"
configurations { "Release", "Debug" }

flags {
  --"StaticRuntime",
  "Unicode",
}

buildoptions {}

defines {
    "UNICODE",
    "_UNICODE",
}

linkoptions {
  --"/NODEFAULTLIB:libci.lib",
}

includedirs {
    "include",
    "include/io",
    "include/aesGladman",
    "include/video",
    "include/scene",
    "include/gui",

    "../freetype/include", 
    "../zlib",
    "../libpng",
    "../jpeglib",
    "../bzip2",
    "../lzma",
}

configuration "windows"
do
    defines {
        "WIN32",
        "_WINDOWS",
        "IRRLICHT_EXPORTS",
        --"_IRR_WCHAR_FILESYSTEM",
    }
end

configuration "gmake"
do
  buildoptions { "-Wall", "-std=c++0x", "-U__STRICT_ANSI__",}
end

configuration "gmake"
do
  buildoptions { "-Wall", "-std=c++0x", "-U__STRICT_ANSI__",}
end

configuration "gmake Debug"
do
    buildoptions { "-g" }
    linkoptions { "-g" }
end

configuration "vs*"
do
    linkoptions { "/NODEFAULTLIB:LIBCMT" }
    defines {
        "_CRT_SECURE_NO_DEPRECATE",
    }
    buildoptions { "/wd4996" }
end

configuration "Debug"
do
  --defines { "DEBUG" }
  flags { "Symbols" }
  targetdir "../debug"
  libdirs {
    "../debug",
  }
end

configuration "Release"
do
  defines { "NDEBUG" }
  flags { "Optimize" }
  targetdir "../release"
  libdirs {
    "../release",
  }
end

------------------------------------------------------------------------------
configuration {}

include "io"
include "aesGladman"
include "video"
include "scene"
include "gui"
------------------------------------------------------------------------------

-- A project defines one build target
project "Irrlicht"
--kind "WindowedApp"
--kind "ConsoleApp"
kind "SharedLib"
--kind "StaticLib"
language "C++"
files {
    "include/*.h",
    "src/*.cpp", "src/*.h",
}
linkoptions {
}
links {
    "IrrlichtVideo",
    "IrrlichtGui",
    "IrrlichtScene", 
    "IrrlichtIO", 
    "aesGladman",

    "freetype",
    "winmm", "gdi32", "shlwapi", "vfw32", "imm32",
    "png", "jpeg", "bzip2", "lzma", "z",
    "opengl32",
}

