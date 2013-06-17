-- A solution contains projects, and defines the available configurations
solution "Irrlicht"
configurations { "Release", "Debug" }

flags {
    "Unicode",
    "NoIncrementalLink",
}

buildoptions {}

defines {
    "UNICODE",
    "_UNICODE",
    "NO_IRR_USE_NON_SYSTEM_ZLIB_",
    "NO_IRR_USE_NON_SYSTEM_BZLIB_",
    "NO_IRR_USE_NON_SYSTEM_LIB_PNG_",
    "NO_IRR_USE_NON_SYSTEM_JPEG_LIB_",
}

linkoptions {
}

includedirs {
    "include",
    "aesGladman/src",
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
    }
    includedirs {
        "$(DXSDK_DIR)/include",
    }
    libdirs {
        "$(DXSDK_DIR)/lib/x86",
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
    buildoptions { 
        "/wd4996",
        "/wd4005",
    }
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
include "aesGladman"

