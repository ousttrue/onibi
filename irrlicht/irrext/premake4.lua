-- A solution contains projects, and defines the available configurations
solution "irrmmd"
configurations { "Debug", "Release" }

configuration "Debug"
do
    defines { "DEBUG" }
    flags { "Symbols" }
    targetdir "../../debug"
end

configuration "Release"
do
    defines { "NDEBUG" }
    flags { "Optimize" }
    targetdir "../../release"
end

configuration "gmake"
do
    buildoptions { "-Wall" }
end

configuration "vs*"
do
    defines {
        "NOMINMAX", 
        "_USE_MATH_DEFINES",
    }
    buildoptions { 
        "/wd4996",
        "/wd4738",
    }
end

configuration {}

include "irrmmd"
include "libpolymesh"
include "rigid"

