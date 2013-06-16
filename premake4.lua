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
  buildoptions { "-Wall", "-U__CYGWIN__", }
end

configuration "vs*"
do
    --linkoptions { "/NODEFAULTLIB:LIBCMT" }
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

