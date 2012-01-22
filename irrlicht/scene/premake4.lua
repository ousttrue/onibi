-- A project defines one build target
project "IrrlichtScene"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C++"
files {
    "../include/*.h",
    "include/*.h",
    "src/*.cpp", "src/*.h",
}

