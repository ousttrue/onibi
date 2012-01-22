%module(package="irr", directors="1") "gui"
%{
#include "Irrlicht.h"
using namespace irr;
using namespace core;
using namespace video;
using namespace gui;
using namespace scene;
%}

%include "irr.common.i"
%import "irr.core.i"
%import "irr.video.i"

//////////////////////////////////////////////////////////////////////////////
// warning
//////////////////////////////////////////////////////////////////////////////
#pragma SWIG nowarn=312
#pragma SWIG nowarn=325
#pragma SWIG nowarn=362
#pragma SWIG nowarn=389
#pragma SWIG nowarn=401
#pragma SWIG nowarn=503

//////////////////////////////////////////////////////////////////////////////
// Irrlicht headers
//////////////////////////////////////////////////////////////////////////////
%include "IrrCompileConfig.h"
%include "IrrTypes.h"

%include "EGUIAlignment.h"
%include "EGUIElementTypes.h"
%include "EGUIElementTypes.h"
%include "IGUIElement.h"
%include "IGUIElementFactory.h"
%include "IGUISkin.h"
%include "IGUIEnvironment.h"
%include "IGUIButton.h"
%include "IGUICheckBox.h"
%include "IGUIColorSelectDialog.h"
%include "IGUIComboBox.h"
%include "IGUIContextMenu.h"
%include "IGUIEditBox.h"
%include "IGUIFileOpenDialog.h"
%include "IGUIFont.h"
%include "IGUIFontBitmap.h"
%include "IGUIImage.h"
%include "IGUIInOutFader.h"
%include "IGUIListBox.h"
%include "IGUIMeshViewer.h"
%include "IGUIScrollBar.h"
%include "IGUISpinBox.h"
%include "IGUISpriteBank.h"
%include "IGUIStaticText.h"
%include "IGUITabControl.h"
%include "IGUITable.h"
%include "IGUIToolbar.h"
%include "IGUIWindow.h"
%include "IGUITreeView.h"
%include "ICursorControl.h"

//////////////////////////////////////////////////////////////////////////////
// extends
//////////////////////////////////////////////////////////////////////////////
%extend irr::gui::IGUIScrollBar {

static IGUIScrollBar *cast(IGUIElement *element) {
    return (IGUIScrollBar*)element;
}

};

%extend irr::gui::IGUIContextMenu {

static IGUIContextMenu *cast(IGUIElement *element) {
    return (IGUIContextMenu*)element;
}

};

%extend irr::gui::IGUIStaticText {

static IGUIStaticText *cast(IGUIElement *element) {
    return (IGUIStaticText*)element;
}

};

