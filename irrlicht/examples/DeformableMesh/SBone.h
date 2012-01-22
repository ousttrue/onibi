// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __S_BONE_H_INCLUDED__
#define __S_BONE_H_INCLUDED__

namespace irr
{
namespace scene
{

    struct SBone
    {
        SBone(u32 index, const core::stringc &name, const core::vector3df &pos)
            :Index(index), Name(name), Position(pos), RelativeOffset(pos){}

        void addChild(SBone *child) {
            child->RelativeOffset=child->Position-Position;
            Children.push_back(child);
        }

        core::stringc getName(){ return Name; }

        u32 Index;
        core::stringc Name;
        core::vector3df Position;
        core::vector3df RelativeOffset;
        core::array<SBone*> Children;
    };

} // end namespace scene
} // end namespace irr

#endif
