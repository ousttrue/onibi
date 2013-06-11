-- A solution contains projects, and defines the available configurations
solution "Irrlicht"
configurations { "Release", "Debug" }

flags {
  --"StaticRuntime",
  "Unicode",
  "NoIncrementalLink",
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

configuration "gmake Debug"
do
    buildoptions { "-g" }
    linkoptions { "-g" }
end

configuration "vs*"
do
    --linkoptions { "/NODEFAULTLIB:LIBCMT" }
    defines {
        "_CRT_SECURE_NO_DEPRECATE",
        "NOMINMAX",
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

configuration {}

dofile "Irrlicht.lua"
include "io"
include "aesGladman"
include "video"
include "scene"
include "gui"

