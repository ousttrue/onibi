// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __S_DEFORMABLE_MESH_H_INCLUDED__
#define __S_DEFORMABLE_MESH_H_INCLUDED__

#include "IDeformableMesh.h"
#include "IMeshDeformer.h"
#include "SSkeletalMeshDeformer.h"
#include <assert.h>

namespace irr
{
namespace scene
{

	//! implementation of the IDeformableMesh interface.
	struct SDeformableMesh : public IDeformableMesh
	{
        //! constructor
        SDeformableMesh(SMeshBuffer* vertexBuffer) 
            : IDeformableMesh(),
            VertexBuffer(vertexBuffer), DeformedBuffer(new SMeshBuffer), 
            SkeltalMeshDeformer(0),
            Type(EAMT_UNKNOWN)
        {
			#ifdef _DEBUG
			setDebugName("SDeformableMesh");
			#endif

            // copy vertices from VertexBuffer to DeformedBuffer
            size_t vertexCount=VertexBuffer->Vertices.size();
            DeformedBuffer->Vertices.set_used(vertexCount);
            for(size_t i=0; i<vertexCount; ++i){
                DeformedBuffer->Vertices[i]=VertexBuffer->Vertices[i];
            }
		}


		//! destructor
		virtual ~SDeformableMesh()
		{
            VertexBuffer->drop();
            VertexBuffer=0;
            DeformedBuffer->drop();
            DeformedBuffer=0;
            for(u32 i=0; i<IndexBuffers.size(); ++i){
                IndexBuffers[i]->drop();
            }
            IndexBuffers.clear();
		}


		//! Gets the frame count of the animated mesh.
		/** \return Amount of frames. If the amount is 1, it is a static, non animated mesh. */
		virtual u32 getFrameCount() const
		{
            if(SkeltalMeshDeformer){
                return SkeltalMeshDeformer->getFrameCount();
            }
			return 1;
		}


		//! Returns the IMesh interface for a frame.
		/** \param frame: Frame number as zero based index. The maximum frame number is
		getFrameCount() - 1;
		\param detailLevel: Level of detail. 0 is the lowest,
		255 the highest level of detail. Most meshes will ignore the detail level.
		\param startFrameLoop: start frame
		\param endFrameLoop: end frame
		\return The animated mesh based on a detail level. */
		virtual IMesh* getMesh(s32 frame, s32 detailLevel, s32 startFrameLoop=-1, s32 endFrameLoop=-1)
		{
std::cout << frame << std::endl;
            deform(frame);
            // not use frame system ?
            setDirty(EBT_VERTEX_AND_INDEX);
			return this;
		}


		//! Returns an axis aligned bounding box of the mesh.
		/** \return A bounding box of this mesh is returned. */
		virtual const core::aabbox3d<f32>& getBoundingBox() const
		{
			return Box;
		}


		//! set user axis aligned bounding box
		virtual void setBoundingBox(const core::aabbox3df& box)
		{
			Box = box;
		}

		//! Recalculates the bounding box.
		void recalculateBoundingBox()
		{
            DeformedBuffer->recalculateBoundingBox();
            Box=DeformedBuffer->getBoundingBox();
		}


		//! Returns the type of the animated mesh.
		virtual E_ANIMATED_MESH_TYPE getMeshType() const
		{
			return Type;
		}


		//! returns amount of mesh buffers.
		virtual u32 getMeshBufferCount() const
		{
			return IndexBuffers.size();
		}


		//! returns pointer to a mesh buffer
		virtual IMeshBuffer* getMeshBuffer(u32 nr) const
		{
            return IndexBuffers[nr];
		}


		//! Returns pointer to a mesh buffer which fits a material
		/** \param material: material to search for
		\return Returns the pointer to the mesh buffer or
		NULL if there is no such mesh buffer. */
		virtual IMeshBuffer* getMeshBuffer( const video::SMaterial &material) const
		{
			for (u32 i=0; i<IndexBuffers.size(); ++i){
                IMeshBuffer *buffer=IndexBuffers[i];
                if(buffer->getMaterial()==material){
                    return buffer;
                }
            }
            return 0;
		}


		//! Set a material flag for all meshbuffers of this mesh.
		virtual void setMaterialFlag(video::E_MATERIAL_FLAG flag, bool newvalue)
		{
            /* ToDo
			for (u32 i=0; i<IndexBuffers.size(); ++i)
				IndexBuffers[i]->setMaterialFlag(flag, newvalue);
                */
		}

		//! set the hardware mapping hint, for driver
		virtual void setHardwareMappingHint( E_HARDWARE_MAPPING newMappingHint, E_BUFFER_TYPE buffer=EBT_VERTEX_AND_INDEX )
		{
            // fixed
		}

		//! flags the meshbuffer as changed, reloads hardware buffers
		virtual void setDirty(E_BUFFER_TYPE buffer=EBT_VERTEX_AND_INDEX)
		{
			for (u32 i=0; i<IndexBuffers.size(); ++i)
				IndexBuffers[i]->setDirty(buffer);
		}


        virtual void addDeformer(IMeshDeformer *meshDeformer)
        {
            if(meshDeformer->getType()==EDM_TWOWEIGHTED_SKELETON){
                SkeltalMeshDeformer=(SSkeletalMeshDeformer*)meshDeformer;
            }
        }

        virtual SSharedMeshBuffer* createIndexBuffer()
        {
            SSharedMeshBuffer* meshBuffer=new SSharedMeshBuffer(&DeformedBuffer->Vertices);
            //meshBuffer->setHardwareMappingHint(EHM_NEVER);
            IndexBuffers.push_back(meshBuffer);
            return meshBuffer;
        }

        void deform(s32 frame)
        {
            if(SkeltalMeshDeformer){
                SkeltalMeshDeformer->deform(this, frame);
            }
			recalculateBoundingBox();
        }

        virtual u32 getDeformerCount()const{ return 1; }
        virtual IMeshDeformer* getDeformer(u32 index)const{ 
            switch(index)
            {
                case 0: return SkeltalMeshDeformer ? SkeltalMeshDeformer : 0; 
                default: return 0;
            }
        }

        virtual SMeshBuffer* getVertexBuffer(){ return VertexBuffer; }
        virtual SMeshBuffer* getDeformedBuffer(){ return DeformedBuffer; }

        SSkeletalMeshDeformer* getSkeletalMeshDeformer(){ return SkeltalMeshDeformer; }

        //! original vertices
        SMeshBuffer* VertexBuffer;
        //! deformed vertices
        SMeshBuffer* DeformedBuffer;
		//! extepcted SharedMeshBuffer
        core::array<IMeshBuffer*> IndexBuffers;

        //!  deformers
        SSkeletalMeshDeformer *SkeltalMeshDeformer;

		//! The bounding box of this mesh
		core::aabbox3d<f32> Box;

		//! Tyhe type fo the mesh.
		E_ANIMATED_MESH_TYPE Type;
	};


} // end namespace scene
} // end namespace irr

#endif

