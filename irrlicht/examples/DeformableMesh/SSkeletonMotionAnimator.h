// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __S_SKELETON_ANIMATOR_H_INCLUDED__
#define __S_SKELETON_ANIMATOR_H_INCLUDED__

#include "ISkeletonAnimator.h"
#include <algorithm>

namespace irr
{
namespace scene
{
    // fix core::quaternion.getMatrix
    inline core::matrix4 getMatrix(const core::quaternion &rot)
    {
        float xx=rot.X*rot.X;
        float yy=rot.Y*rot.Y;
        float zz=rot.Z*rot.Z;

        float xy=rot.X*rot.Y;
        float yz=rot.Y*rot.Z;
        float zx=rot.Z*rot.X;

        float wx=rot.W*rot.X;
        float wy=rot.W*rot.Y;
        float wz=rot.W*rot.Z;

        core::matrix4 m(core::matrix4::EM4CONST_IDENTITY);

        m[0]=1-2*(yy+zz);
        m[1]=2*(xy+wz);
        m[2]=2*(zx-wy);
        m[4]=2*(xy-wz);
        m[5]=1-2*(xx+zz);
        m[6]=2*(yz+wx);
        m[8]=2*(zx+wy);
        m[9]=2*(yz-wx);
        m[10]=1-2*(xx+yy);

        return m;
    }

	class SSkeletonMotionAnimator : public ISkeletonAnimator
	{
	public:
        SSkeletonMotionAnimator(SSkeleton *skeleton, SSkeletonMotion *motion)
            : Skeleton(skeleton), Frame(0), LastFrame(0), Blend(1.0f)
        {
            skeleton->grab();

            // mapping curve
            u32 boneCount=skeleton->getBoneCount();
            Curves.set_used(boneCount);
            CurrentKeys.set_used(boneCount);
            Matrices.set_used(boneCount);
            for(u32 i=0; i<boneCount; ++i){
                SBone *bone=skeleton->getBone(i);
                SRotPosLinearCurve *curve=motion->getCurve(bone->getName());
                if(curve){
                    Curves[i]=curve;
                    LastFrame=std::max(LastFrame, curve->getFrameCount());
                }
                else{
                    Curves[i]=0;
                }
                CurrentKeys[i].Position=core::vector3df(0, 0, 0);
                CurrentKeys[i].Rotation=core::quaternion(0.0f, 0.0f, 0.0f, 1.0f);
            }
        }

        virtual void update(s32 frame){
            Frame+=frame;
            if(Frame>LastFrame){
                Frame=Frame % LastFrame;
            }
            // set current frame
            for(u32 i=0; i<Curves.size(); ++i){
                SRotPosLinearCurve *curve=Curves[i];
                if(curve){
                    CurrentKeys[i]=curve->getKey(Frame);
                }
            }
            // calc matrices
            accumulate(Skeleton->getRootBone(), core::matrix4(core::matrix4::EM4CONST_IDENTITY));
            for(u32 i=0; i<Matrices.size(); ++i){
                core::matrix4 offset(core::matrix4::EM4CONST_IDENTITY);
                offset.setTranslation(-Skeleton->getBone(i)->Position);
                Matrices[i]*=offset;
            }
        }

        virtual u32 getFrameCount()const
        {
            return LastFrame;
        }

        virtual f32 getBlend()const
        {
            return Blend;
        };

        virtual const core::array<core::matrix4> &getMatrices()const
        {
            return Matrices;
        };

        SSkeleton *Skeleton;
        u32 Frame;
        u32 LastFrame;
        f32 Blend;
        core::array<SRotPosLinearCurve*> Curves;
        core::array<SRotPosKey> CurrentKeys;
        core::array<core::matrix4> Matrices;
    private:
        void accumulate(const SBone *bone, const core::matrix4 &m){
            u32 index=bone->Index;
            SRotPosKey &key=CurrentKeys[index];

            // translation
            core::matrix4 translation(core::matrix4::EM4CONST_IDENTITY);
            translation.setTranslation(key.Position+bone->RelativeOffset);

            // rotation
            //Matrices[index]=m * translation * getMatrix(key.Rotation);
            Matrices[index]=m * translation;

            for(u32 i=0; i<bone->Children.size(); ++i){
                accumulate(bone->Children[i], Matrices[index]);
            }
        }

	};

} // end namespace scene
} // end namespace irr

#endif

