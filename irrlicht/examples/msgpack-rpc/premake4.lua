-- A project defines one build target
project "msgpack-rpc_sample"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "main.cpp",
}
includedirs {
    "../../../irrlicht/include",
    "../../../boost",
    "../../../msgpack/src",
    "../../../msgpack-rpc-asio/include",
}
libdirs {
    "../../../boost/lib",
}
links {
    "msgpack",
    "Irrlicht",
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
  targetdir "../../../debug"
  libdirs {
      "../../../debug"
  }
end

configuration "Release"
do
  defines { "NDEBUG" }
  flags { "Optimize" }
  targetdir "../../../release"
  libdirs {
      "../../../release"
  }
end

