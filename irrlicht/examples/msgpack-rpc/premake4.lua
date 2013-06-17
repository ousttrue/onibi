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

