#!/usr/bin/env python

import os
import shutil
from setuptools import setup, Extension
from distutils.dir_util import mkpath

PY_MODULE_DIR='build/lib.win32-2.7/irr'

# copy to current
def remove_if_eixsts(f):
    if os.path.exists(f):
        shutil.rmtree(f, True)
def copy_if_not_exists(f):
    if not os.path.exists(f):
        shutil.copy('../'+f, f)
copy_if_not_exists('irr.common.i')
copy_if_not_exists('irr.core.i')
copy_if_not_exists('irr.video.i')
copy_if_not_exists('irr.io.i')
copy_if_not_exists('irr.scene.i')
copy_if_not_exists('irr.gui.i')
copy_if_not_exists('irr.__init__.i')
mkpath(PY_MODULE_DIR)

include_dirs=[
        '../../include',
        '../../include/io',
        '../../include/video',
        '../../include/scene',
        '../../include/gui',
        ]

def sub_module(name):
    return Extension('irr._'+name,
                           sources=['irr.'+name+'.i'],
                           swig_opts=['-I'+d for d in include_dirs]+[
                               '-module', name,
                               '-c++',
                               '-fastdispatch',
                               '-outdir', PY_MODULE_DIR,
                               '-DSWIG_TYPE_TABLE=irr',
                               '-DUNICODE',
                               '-D_UNICODE',
                               '-D_IRR_COMPILE_WITH_GUI_',
                               '-D_IRR_WCHAR_FILESYSTEM',
                               '-D_IRR_IMPROVE_UNICODE',
                               '-D_IRR_USE_INPUT_METHOD',
                               '-D_IRR_COMPILE_WITH_CGUITTFONT_',
                               ],
                           include_dirs=include_dirs,
                           extra_compile_args=[
                               '-Wno-unused-parameter',
                               '-Wno-unused-but-set-variable',
                               '-g',
                               ],
                           define_macros=[
                               ('UNICODE', 1),
                               ('_UNICODE', 1),
                               ('_IRR_IMPROVE_UNICODE', 1),
                               ],
                           library_dirs=['../../../release'],
                           #library_dirs=['../../../debug'],
                           libraries=['Irrlicht'],
                           extra_link_args=[
                               '-g',
                               ]
                           )

setup (name = 'irr',
        version = '0.1',
        author      = "ousttrue",
        description = """Irrlicht python binding""",
        ext_modules = [
            sub_module('core'),
            sub_module('video'),
            sub_module('scene'),
            sub_module('gui'),
            sub_module('io'),
            sub_module('__init__'),
            ]
        )

