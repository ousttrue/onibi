-- A project defines one build target
project "aesGladman"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C++"
files {
    "src/*",
}

