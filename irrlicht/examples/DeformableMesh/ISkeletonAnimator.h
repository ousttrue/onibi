// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __I_SKELETON_ANIMATOR_H_INCLUDED__
#define __I_SKELETON_ANIMATOR_H_INCLUDED__

#include "IReferenceCounted.h"

namespace irr
{
namespace scene
{
	//! Interface for an mesh deformer. implement bone skinning and morphing.
	class ISkeletonAnimator : public IReferenceCounted
	{
	public:
		//! Deform a mesh.
        virtual void update(s32 frame)=0;
        virtual f32 getBlend()const=0;
        virtual const core::array<core::matrix4> &getMatrices()const=0;
        virtual u32 getFrameCount()const=0;
	};

} // end namespace scene
} // end namespace irr

#endif

