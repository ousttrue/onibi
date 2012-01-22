project "glut32"
language "C"
kind "StaticLib"

files {
    "src/*.c",
}
includedirs {
    "include",
}
defines {
    'WIN32',
    '_WINDOWS',
    --'_USRDLL',
    --'FREEGLUT_EXPORTS',
    'FREEGLUT_STATIC',
}
links {
    "glu32",
    "opengl32",
    "gdi32",
    "winmm",
    "user32",
}

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

