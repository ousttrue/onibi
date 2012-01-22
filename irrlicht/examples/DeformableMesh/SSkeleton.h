// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __S_SKELETON_H_INCLUDED__
#define __S_SKELETON_H_INCLUDED__

#include "IReferenceCounted.h"
#include "SBone.h"

namespace irr
{
namespace scene
{
	struct SSkeleton : public IReferenceCounted
	{
        core::array<SBone*> Bones;

        u32 getBoneCount(){ return Bones.size(); }
        SBone* getBone(u32 index){ return Bones[index]; }
        SBone* getRootBone(){ return Bones[0]; }
        SBone* createBone(const core::stringc &name, const core::vector3df &pos){
            SBone *bone=new SBone(Bones.size(), name, pos);
            Bones.push_back(bone);
            return bone;
        }
	};

} // end namespace scene
} // end namespace irr

#endif

