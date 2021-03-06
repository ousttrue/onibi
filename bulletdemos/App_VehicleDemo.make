# GNU Make project makefile autogenerated by Premake
ifndef config
  config=release32
endif

ifndef verbose
  SILENT = @
endif

ifndef CC
  CC = gcc
endif

ifndef CXX
  CXX = g++
endif

ifndef AR
  AR = ar
endif

ifeq ($(config),release32)
  OBJDIR     = obj/x32/Release/App_VehicleDemo
  TARGETDIR  = ../release
  TARGET     = $(TARGETDIR)/App_VehicleDemo.exe
  DEFINES   += -D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE -DFREEGLUT_STATIC
  INCLUDES  += -I../bullet -IOpenGL -I../freeglut/include
  CPPFLAGS  += -MMD -MP $(DEFINES) $(INCLUDES)
  CFLAGS    += $(CPPFLAGS) $(ARCH) -O2 -ffast-math -m32
  CXXFLAGS  += $(CFLAGS) 
  LDFLAGS   += -s -m32 -L/usr/lib32 -L../release
  LIBS      += -lOpenGLSupport -lglut32 -lglew32 -lglu32 -lopengl32 -lgdi32 -lwinmm -lBulletDynamics -lBulletCollision -lLinearMath
  RESFLAGS  += $(DEFINES) $(INCLUDES) 
  LDDEPS    += ../release/libOpenGLSupport.a
  LINKCMD    = $(CXX) -o $(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(ARCH) $(LIBS)
  define PREBUILDCMDS
  endef
  define PRELINKCMDS
  endef
  define POSTBUILDCMDS
  endef
endif

ifeq ($(config),debug32)
  OBJDIR     = obj/x32/Debug/App_VehicleDemo
  TARGETDIR  = ../debug
  TARGET     = $(TARGETDIR)/App_VehicleDemo.exe
  DEFINES   += -D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE -DFREEGLUT_STATIC
  INCLUDES  += -I../bullet -IOpenGL -I../freeglut/include
  CPPFLAGS  += -MMD -MP $(DEFINES) $(INCLUDES)
  CFLAGS    += $(CPPFLAGS) $(ARCH) -g -ffast-math -m32
  CXXFLAGS  += $(CFLAGS) 
  LDFLAGS   += -m32 -L/usr/lib32 -L../debug
  LIBS      += -lOpenGLSupport -lglut32 -lglew32 -lglu32 -lopengl32 -lgdi32 -lwinmm -lBulletDynamics -lBulletCollision -lLinearMath
  RESFLAGS  += $(DEFINES) $(INCLUDES) 
  LDDEPS    += ../debug/libOpenGLSupport.a
  LINKCMD    = $(CXX) -o $(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(ARCH) $(LIBS)
  define PREBUILDCMDS
  endef
  define PRELINKCMDS
  endef
  define POSTBUILDCMDS
  endef
endif

ifeq ($(config),release64)
  OBJDIR     = obj/x64/Release/App_VehicleDemo
  TARGETDIR  = ../release64
  TARGET     = $(TARGETDIR)/App_VehicleDemo.exe
  DEFINES   += -D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE -DFREEGLUT_STATIC
  INCLUDES  += -I../bullet -IOpenGL -I../freeglut/include
  CPPFLAGS  += -MMD -MP $(DEFINES) $(INCLUDES)
  CFLAGS    += $(CPPFLAGS) $(ARCH) -O2 -ffast-math -m64
  CXXFLAGS  += $(CFLAGS) 
  LDFLAGS   += -s -m64 -L/usr/lib64 -L../release64
  LIBS      += -lOpenGLSupport -lglut32 -lglew32 -lglu32 -lopengl32 -lgdi32 -lwinmm -lBulletDynamics -lBulletCollision -lLinearMath
  RESFLAGS  += $(DEFINES) $(INCLUDES) 
  LDDEPS    += ../release64/libOpenGLSupport.a
  LINKCMD    = $(CXX) -o $(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(ARCH) $(LIBS)
  define PREBUILDCMDS
  endef
  define PRELINKCMDS
  endef
  define POSTBUILDCMDS
  endef
endif

ifeq ($(config),debug64)
  OBJDIR     = obj/x64/Debug/App_VehicleDemo
  TARGETDIR  = ../debug64
  TARGET     = $(TARGETDIR)/App_VehicleDemo.exe
  DEFINES   += -D_CRT_SECURE_NO_WARNINGS -D_CRT_SECURE_NO_DEPRECATE -DFREEGLUT_STATIC
  INCLUDES  += -I../bullet -IOpenGL -I../freeglut/include
  CPPFLAGS  += -MMD -MP $(DEFINES) $(INCLUDES)
  CFLAGS    += $(CPPFLAGS) $(ARCH) -g -ffast-math -m64
  CXXFLAGS  += $(CFLAGS) 
  LDFLAGS   += -m64 -L/usr/lib64 -L../debug64
  LIBS      += -lOpenGLSupport -lglut32 -lglew32 -lglu32 -lopengl32 -lgdi32 -lwinmm -lBulletDynamics -lBulletCollision -lLinearMath
  RESFLAGS  += $(DEFINES) $(INCLUDES) 
  LDDEPS    += ../debug64/libOpenGLSupport.a
  LINKCMD    = $(CXX) -o $(TARGET) $(OBJECTS) $(LDFLAGS) $(RESOURCES) $(ARCH) $(LIBS)
  define PREBUILDCMDS
  endef
  define PRELINKCMDS
  endef
  define POSTBUILDCMDS
  endef
endif

OBJECTS := \
	$(OBJDIR)/main.o \
	$(OBJDIR)/VehicleDemo.o \

RESOURCES := \
	$(OBJDIR)/bullet.res \

SHELLTYPE := msdos
ifeq (,$(ComSpec)$(COMSPEC))
  SHELLTYPE := posix
endif
ifeq (/bin,$(findstring /bin,$(SHELL)))
  SHELLTYPE := posix
endif

.PHONY: clean prebuild prelink

all: $(TARGETDIR) $(OBJDIR) prebuild prelink $(TARGET)
	@:

$(TARGET): $(GCH) $(OBJECTS) $(LDDEPS) $(RESOURCES)
	@echo Linking App_VehicleDemo
	$(SILENT) $(LINKCMD)
	$(POSTBUILDCMDS)

$(TARGETDIR):
	@echo Creating $(TARGETDIR)
ifeq (posix,$(SHELLTYPE))
	$(SILENT) mkdir -p $(TARGETDIR)
else
	$(SILENT) mkdir $(subst /,\\,$(TARGETDIR))
endif

$(OBJDIR):
	@echo Creating $(OBJDIR)
ifeq (posix,$(SHELLTYPE))
	$(SILENT) mkdir -p $(OBJDIR)
else
	$(SILENT) mkdir $(subst /,\\,$(OBJDIR))
endif

clean:
	@echo Cleaning App_VehicleDemo
ifeq (posix,$(SHELLTYPE))
	$(SILENT) rm -f  $(TARGET)
	$(SILENT) rm -rf $(OBJDIR)
else
	$(SILENT) if exist $(subst /,\\,$(TARGET)) del $(subst /,\\,$(TARGET))
	$(SILENT) if exist $(subst /,\\,$(OBJDIR)) rmdir /s /q $(subst /,\\,$(OBJDIR))
endif

prebuild:
	$(PREBUILDCMDS)

prelink:
	$(PRELINKCMDS)

ifneq (,$(PCH))
$(GCH): $(PCH)
	@echo $(notdir $<)
	-$(SILENT) cp $< $(OBJDIR)
	$(SILENT) $(CXX) $(CXXFLAGS) -o "$@" -c "$<"
endif

$(OBJDIR)/bullet.res: bullet.rc
	@echo $(notdir $<)
	$(SILENT) windres $< -O coff -o "$@" $(RESFLAGS)
$(OBJDIR)/main.o: VehicleDemo/main.cpp
	@echo $(notdir $<)
	$(SILENT) $(CXX) $(CXXFLAGS) -o "$@" -c "$<"
$(OBJDIR)/VehicleDemo.o: VehicleDemo/VehicleDemo.cpp
	@echo $(notdir $<)
	$(SILENT) $(CXX) $(CXXFLAGS) -o "$@" -c "$<"

-include $(OBJECTS:%.o=%.d)
