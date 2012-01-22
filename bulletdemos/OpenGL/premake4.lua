	project "OpenGLSupport"
		
	kind "StaticLib"
	includedirs {
		".",
		"../../bullet"
	}
	configuration {"Windows"}
	includedirs {
		"../../freeglut/include"
	}
    defines {
        "FREEGLUT_STATIC",
    }
	configuration{}

	files {
		"**.cpp",
		"**.h"
	}
