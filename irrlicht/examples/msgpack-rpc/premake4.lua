-- A project defines one build target
project "msgpack-rpc_sample"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
BOOST_DIR=os.getenv("BOOST_DIR")
files { 
    "main.cpp",
}
includedirs {
    BOOST_DIR,
    "../../../irrlicht/include",
    "../../../msgpack/src",
    "../../../msgpack-rpc-asio/include",
}
libdirs {
    BOOST_DIR.."/stage/lib",
}

configuration "gmake Debug"
do
    defines {
        "BOOST_THREAD_USE_LIB",
    }
    links { 
        "boost_chrono-mgw47-mt-d-1_54",
        "boost_thread-mgw47-mt-d-1_54",
        "boost_timer-mgw47-mt-d-1_54",
        "boost_exception-mgw47-mt-d-1_54",
        "boost_system-mgw47-mt-d-1_54",
    }
end

configuration {}
links {
    "msgpack",
    "Irrlicht",
    "Mswsock", "ws2_32",
}

