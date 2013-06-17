-- A solution contains projects, and defines the available configurations
solution "Dependencies"
configurations { "Release", "Debug" }
configuration "gmake Debug"
do
    buildoptions { "-g" }
    linkoptions { "-g" }
end

configuration "gmake"
do
    buildoptions { 
        "-Wall", 
        "-U__CYGWIN__", 
    }
end

configuration "vs*"
do
    --linkoptions { "/NODEFAULTLIB:LIBCMT" }
    buildoptions { 
        "/wd4996",
    }
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
    targetdir "debug"
end

configuration "Release"
do
    defines { "NDEBUG" }
    flags { "Optimize" }
    targetdir "release"
end

configuration {}

-- freetype
include "freetype"

-- opengl
include "glew"
include "freeglut"

-- irrlicht
include "zlib"
include "lzma"
include "jpeglib"
include "libpng"
include "bzip2"

-- msgpack
include "msgpack"

-- mqo, pmd loading
include "meshio"

