-- A project defines one build target
-- from IrrlichtML 1.7.1
project "IrrlichtML"
--kind "WindowedApp"
kind "ConsoleApp"
--kind "SharedLib"
--kind "StaticLib"
language "C++"
files { 
    "*.cpp", "*.h",
}
includedirs {
    "../../../irrlicht/include",
    "../../../freetype/include",
}
links {
    "Irrlicht",
    "freetype", "z",
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

