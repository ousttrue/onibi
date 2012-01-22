-- A project defines one build target
project "bzip2"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C++"
files { 
    "blocksort.c",
    "bzcompress.c",
    "bzlib.c",
    "bzlib.h",
    "bzlib_private.h",
    "crctable.c",
    "decompress.c",
    "huffman.c",
    "randtable.c",
}

configuration "windows"
do
    defines {
        "WIN32",
        "_WINDOWS",
    }
end

configuration "gmake"
do
  buildoptions { "-Wall" }
end

configuration "vs*"
do
  buildoptions { "/wd4996" }
end

configuration "Debug"
do
  defines { "DEBUG" }
  flags { "Symbols" }
  targetdir "../debug"
end

configuration "Release"
do
  defines { "NDEBUG" }
  flags { "Optimize" }
  targetdir "../release"
end

