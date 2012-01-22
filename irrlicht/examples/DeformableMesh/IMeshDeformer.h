// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __I_MESH_DEFORMER_H_INCLUDED__
#define __I_MESH_DEFORMER_H_INCLUDED__

#include "IReferenceCounted.h"
#include "IDeformableMesh.h"

namespace irr
{
namespace scene
{
    enum EDM_TYPE
    {
        EDM_INDEXED_OFFSET,
        EDM_TWOWEIGHTED_SKELETON,
    };

	//! Interface for an mesh deformer. implement bone skinning and morphing.
	class IMeshDeformer : public IReferenceCounted
	{
	public:
        virtual EDM_TYPE getType()const=0;
		//! Deform a mesh.
        virtual void deform(IDeformableMesh *mesh, s32 frame)=0;
	};

} // end namespace scene
} // end namespace irr

#endif

