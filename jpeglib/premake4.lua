-- A project defines one build target
project "jpeg"
--kind "WindowedApp"
--kind "ConsoleApp"
--kind "SharedLib"
kind "StaticLib"
language "C"
files { 
    "cderror.h",
    "jaricom.c",
    "jcapimin.c",
    "jcapistd.c",
    "jcarith.c",
    "jccoefct.c",
    "jccolor.c",
    "jcdctmgr.c",
    "jchuff.c",
    "jchuff.h",
    "jcinit.c",
    "jcmainct.c",
    "jcmarker.c",
    "jcmaster.c",
    "jcomapi.c",
    "jconfig.h",
    "jcparam.c",
    "jcprepct.c",
    "jcsample.c",
    "jctrans.c",
    "jdapimin.c",
    "jdapistd.c",
    "jdarith.c",
    "jdatadst.c",
    "jdatasrc.c",
    "jdcoefct.c",
    "jdcolor.c",
    "jdct.h",
    "jddctmgr.c",
    "jdhuff.c",
    "jdhuff.h",
    "jdinput.c",
    "jdmainct.c",
    "jdmarker.c",
    "jdmaster.c",
    "jdmerge.c",
    "jdpostct.c",
    "jdsample.c",
    "jdtrans.c",
    "jerror.c",
    "jerror.h",
    "jfdctflt.c",
    "jfdctfst.c",
    "jfdctint.c",
    "jidctflt.c",
    "jidctfst.c",
    "jidctint.c",
    "jinclude.h",
    "jmemmgr.c",
    "jmemnobs.c",
    "jmemsys.h",
    "jmorecfg.h",
    "jpegint.h",
    "jpeglib.h",
    "jquant1.c",
    "jquant2.c",
    "jutils.c",
    "jversion.h",
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

