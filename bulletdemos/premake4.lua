solution "BulletSolution"

language "C++"
configurations {"Release", "Debug"}
configuration "Release"
do
    flags {
        "Optimize",
        --"StaticRuntime",
        "NoMinimalRebuild",
        "FloatFast",
    }
end

configuration "Debug"
do
    flags {
        "Symbols",
        --"StaticRuntime" ,
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

include "OpenGL"

function createDemos( demos, incdirs, linknames)
    for _, name in ipairs(demos) do

        project ( "App_" .. name )

        kind "ConsoleApp"

        includedirs {incdirs}
        --defines { 'FREEGLUT_EXPORTS' }
        defines { 'FREEGLUT_STATIC' }

        configuration { "Windows" }
        do
            links { "OpenGLSupport", "glut32","glew32","glu32","opengl32","gdi32","winmm",}
            includedirs{	"../freeglut/include"	}
            files   { "bullet.rc" }
        end

        configuration {"MaxOSX"}
        do
            --print "hello"
            linkoptions { "-framework Carbon -framework OpenGL -framework AGL -framework Glut" } 
        end

        configuration {"not Windows", "not MacOSX"}
        do
            links {"GL","GLU","glut"}
        end

        configuration {}
        links { 
            linknames
        }

        files     { 
            "./" .. name .. "/*.cpp" ,
            "./" .. name .. "/*.h"
        }

    end
end


-- the following demos require custom include or link settings

-- "CharacterDemo", fixme: it includes BspDemo files
createDemos({
    "BasicDemo",
    "Box2dDemo",
    "BspDemo",
    "CcdPhysicsDemo",
    "CollisionDemo",
    "CollisionInterfaceDemo",
    "ConcaveConvexcastDemo",
    "ConcaveDemo",
    "ConcaveRaycastDemo",
    "ConstraintDemo",
    "ContinuousConvexCollision",
    "ConvexHullDistance",
    "DynamicControlDemo",
    "EPAPenDepthDemo",
    "ForkLiftDemo",
    "FractureDemo",
    "GenericJointDemo",
    "GimpactTestDemo",
    "GjkConvexCastDemo",
    "HelloWorld",
    "InternalEdgeDemo",
    "MovingConcaveDemo",
    "MultiMaterialDemo",
    "RagdollDemo",
    "Raytracer",
    "SimplexDemo",
    "SliderConstraintDemo",
    "TerrainDemo",
    "UserCollisionAlgorithm",
    "VehicleDemo"
},
{
    "../bullet",
    "OpenGL",
},
{
    "BulletDynamics",
    "BulletCollision",
    "LinearMath",
}
)

--[[
createDemos({"ConvexDecompositionDemo"},
{
"../Extras/HACD",
"../Extras/ConvexDecomposition",
"../src",
"OpenGL",
},
{
"OpenGLSupport",
"BulletDynamics",
"BulletCollision",
"LinearMath",
"HACD",
"ConvexDecomposition",
}
)

createDemos({"SoftDemo"},
{
"../src",
"OpenGL",
},
{
"OpenGLSupport",
"BulletSoftBody",
"BulletDynamics",
"BulletCollision",
"LinearMath",
}
)

createDemos({"SerializeDemo"},
{
"../Extras/Serialize/BulletFileLoader",
"../Extras/Serialize/BulletWorldImporter",
"../src",
"OpenGL",
},
{
"OpenGLSupport",
"BulletSoftBody",
"BulletDynamics",
"BulletCollision",
"LinearMath",
"BulletFileLoader",
"BulletWorldImporter",
}
)
--]]

