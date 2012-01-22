project "BulletDynamics"

language "C++"
kind "StaticLib"
includedirs {
    "..",
}
files {
    "**.cpp",
    "**.h"
}
