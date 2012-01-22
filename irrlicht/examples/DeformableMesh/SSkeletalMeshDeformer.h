// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __S_SKELETAL_MESH_DEFORMER_H_INCLUDED__
#define __S_SKELETAL_MESH_DEFORMER_H_INCLUDED__

#include "IMeshDeformer.h"
#include "SBoneWeight.h"
#include "SSkeleton.h"
#include "SSkeletonMotion.h"
#include "SSkeletonMotionAnimator.h"

namespace irr
{
namespace scene
{

    //! skinning deformer for IDeformableMesh
    struct SSkeletalMeshDeformer : public IMeshDeformer
    {
        SSkeletalMeshDeformer(const core::array<SBoneWeight> &boneWeights, SSkeleton *skeleton) {
            BoneWeights=boneWeights;
            Skeleton=skeleton;
        }

        virtual EDM_TYPE getType()const{ return EDM_TWOWEIGHTED_SKELETON; }

        virtual void deform(IDeformableMesh *mesh, s32 frame){
            for(u32 i=0; i<Motions.size(); ++i){
                ISkeletonAnimator *skeletonAnimator=Motions[i];
                skeletonAnimator->update(frame);
            }
            for(u32 i=0; i<Motions.size(); ++i){
                ISkeletonAnimator *skeletonAnimator=Motions[i];
                if(i==0){
                    applyMatrices(
                            mesh->getDeformedBuffer()->Vertices,
                            mesh->getVertexBuffer()->Vertices,
                            skeletonAnimator->getBlend(), skeletonAnimator->getMatrices());
                }
                else{
                    applyMatrices(
                            mesh->getDeformedBuffer()->Vertices,
                            mesh->getDeformedBuffer()->Vertices,
                            skeletonAnimator->getBlend(), skeletonAnimator->getMatrices());
                }
            }
        }

        void addMotion(SSkeletonMotion *motion)
        {
            Motions.push_back(new SSkeletonMotionAnimator(Skeleton, motion));
        }

        u32 getFrameCount()
        {
            u32 frameCount=0;
            for(u32 i=0; i<Motions.size(); ++i){
                std::cout << "motion: " << Motions[i]->getFrameCount() << std::endl;
                frameCount=std::max(frameCount, Motions[i]->getFrameCount());
            }
            return frameCount;
        }

        SSkeleton *Skeleton;
        core::array <ISkeletonAnimator*> Motions;
        core::array<SBoneWeight> BoneWeights;

    private:
        void applyMatrices(
                core::array<video::S3DVertex> &dst,
                const core::array<video::S3DVertex> &src,
                const f32 blend, const core::array<core::matrix4> &matrices)
        {
            static const f32 EPSILON=1e-5f;

            core::vector3df transformed;
            core::vector3df v0;
            core::vector3df v1;
            for(u32 i=0; i<src.size(); ++i){
                SBoneWeight &boneWeight=BoneWeights[i];
                if(boneWeight.weight0>1.0f-EPSILON){
                    // use bone0
                    core::vector3df v0;
                    matrices[boneWeight.bone0].transformVect(
                            v0,
                            src[i].Pos);
                    transformed=v0*blend+src[i].Pos*(1.0-blend);
                }
                else if(boneWeight.weight0<EPSILON){
                    // use bone1
                    matrices[boneWeight.bone1].transformVect(
                            v1,
                            src[i].Pos);
                    transformed=v1*blend+src[i].Pos*(1.0-blend);
                }
                else{
                    // bone0
                    matrices[boneWeight.bone0].transformVect(
                            v0,
                            src[i].Pos);
                    // bone1
                    matrices[boneWeight.bone1].transformVect(
                            v1,
                            src[i].Pos);
                    // blend
                    transformed=(v0*boneWeight.weight0 + 
                            v1*(1.0f-boneWeight.weight0))*blend+src[i].Pos*(1.0-blend);
                }
                dst[i].Pos=transformed;
            }
        }

    };

} // end namespace scene
} // end namespace irr

#endif
