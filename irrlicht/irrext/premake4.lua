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
    buildoptions { 
        "-Wall",
        "-std=c++0x",
        "-U__STRICT_ANSI__",
    }
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

--dofile "libpolymesh/rigid_test.lua"
include "irrmmd"
include "libpolymesh"

