solution "BulletSolution"

language "C++"
configurations {"Release", "Debug"}
configuration "Release"
do
    flags {
        "Optimize",
        "StaticRuntime",
        "NoMinimalRebuild",
        "FloatFast",
    }
end

configuration "Debug"
do
    flags {
        "Symbols",
        "StaticRuntime" ,
        "NoMinimalRebuild",
        "NoEditAndContinue" ,
        "FloatFast",
    }
end

platforms {"x32", "x64"}

configuration {"x64", "release"}
do
    targetdir "../release64"
    libdirs { "../release64" }
end
configuration {"x64", "debug"}
do
    targetdir "../debug64"
    libdirs { "../debug64" }
end
configuration {"x32", "release"}
do
    targetdir "../release"
    libdirs { "../release" }
end
configuration {"x32", "debug"}
do
    targetdir "../debug"
    libdirs { "../debug" }
end

configuration {"Windows"}
do
    defines { "_CRT_SECURE_NO_WARNINGS","_CRT_SECURE_NO_DEPRECATE"}
end

configuration {}
flags { "NoRTTI"}

-- Disable exception handling on MSVC 2008 and higher. MSVC 2005 without service pack has some linker issue (ConvexDecompositionDemo uses STL through HACD library)	
if _ACTION == "vs2010" or _ACTION=="vs2008" then
    flags { "NoExceptions"}
    defines { "_HAS_EXCEPTIONS=0" }
end

-- Multithreaded compiling
if _ACTION == "vs2010" then
    buildoptions { "/MP"  }
end 

configuration "Release"
do
    flags { "Optimize", "StaticRuntime", "NoMinimalRebuild", "FloatFast"}
end

configuration "Debug"
do
    flags { "Symbols", "StaticRuntime" , "NoMinimalRebuild", "NoEditAndContinue" ,"FloatFast"}
end

configuration {"Windows"}
do
    defines { "_CRT_SECURE_NO_WARNINGS","_CRT_SECURE_NO_DEPRECATE"}
end

include "LinearMath"	
include "BulletCollision"	
include "BulletDynamics"	
include "BulletSoftBody"	

