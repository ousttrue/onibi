-- A project defines one build target
project "IrrlichtVideo"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C++"
includedirs {
    "$(DXSDK_DIR)/include",
}
files {
    "../include/*.h",
    "include/*.h",
    "src/*.cpp", "src/*.h",
}

