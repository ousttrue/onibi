-- A project defines one build target
project "freetype"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C"
files {
  "builds/win32/ftdebug.c",
  "src/autofit/autofit.c",
  "src/bdf/bdf.c",
  "src/cff/cff.c",
  "src/base/ftbase.c",
  "src/base/ftbitmap.c",
  "src/cache/ftcache.c",
  "src/base/ftfstype.c",
  "src/base/ftgasp.c",
  "src/base/ftglyph.c",
  "src/gzip/ftgzip.c",
  "src/base/ftinit.c",
  "src/lzw/ftlzw.c",
  "src/base/ftstroke.c",
  "src/base/ftsystem.c",
  "src/smooth/smooth.c",
  "src/base/ftbbox.c",
  "src/base/ftmm.c",
  "src/base/ftpfr.c",
  "src/base/ftsynth.c",
  "src/base/fttype1.c",
  "src/base/ftwinfnt.c",
  "src/pcf/pcf.c",
  "src/pfr/pfr.c",
  "src/psaux/psaux.c",
  "src/pshinter/pshinter.c",
  "src/psnames/psmodule.c",
  "src/raster/raster.c",
  "src/sfnt/sfnt.c",
  "src/truetype/truetype.c",
  "src/type1/type1.c",
  "src/cid/type1cid.c",
  "src/type42/type42.c",
  "src/winfonts/winfnt.c",
}
flags { "StaticRuntime", }
buildoptions {}
defines {
  "_CRT_SECURE_NO_WARNINGS",
  "_CRT_SECURE_NO_DEPRECATE",
  "FT2_BUILD_LIBRARY",
}
includedirs {
  "./include",
}
linkoptions {}
libdirs {}
links {}

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
  defines { 
    "DEBUG",
    "FT_DEBUG_LEVEL_ERROR",
    "FT_DEBUG_LEVEL_TRACE",
  }
  flags { "Symbols" }
  targetdir "../debug"
end

configuration "Release"
do
  defines { "NDEBUG" }
  flags { "Optimize" }
  targetdir "../release"
end

