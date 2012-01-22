// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __I_DEFORMABLE_MESH_H_INCLUDED__
#define __I_DEFORMABLE_MESH_H_INCLUDED__

#include "scene/IAnimatedMesh.h"

namespace irr
{
namespace scene
{
    class IMeshDeformer;

	//! Interface for an deformable mesh.
	class IDeformableMesh : public IAnimatedMesh
	{
	public:
        virtual void addDeformer(IMeshDeformer *deformer)=0;
        virtual SSharedMeshBuffer *createIndexBuffer()=0;

        virtual u32 getDeformerCount()const=0;
        virtual IMeshDeformer* getDeformer(u32 index)const=0;

        virtual SMeshBuffer* getVertexBuffer()=0;
        virtual SMeshBuffer* getDeformedBuffer()=0;

	};

} // end namespace scene
} // end namespace irr

#endif

