// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __S_SKELETON_MOTION_H_INCLUDED__
#define __S_SKELETON_MOTION_H_INCLUDED__

#include "IReferenceCounted.h"
#include "SRotPosKey.h"

namespace irr
{
namespace scene
{
    struct SSkeletonMotion
    {
        u32 getFrameCount()const{ return FrameCount; }
        bool load(const io::path &path);

        SRotPosLinearCurve* getCurve(const core::stringc &name)
        {
            core::map<core::stringc, SRotPosLinearCurve*>::Node *found=
                BoneCurveMap.find(name); 
            if(found){
                return found->getValue();
            }
            else{
                return 0;
            }
        }

        SRotPosLinearCurve* addCurve(const core::stringc &name)
        {
            SRotPosLinearCurve *curve=new SRotPosLinearCurve(name);
            BoneCurveMap.insert(name, curve);
            return curve;
        }

    private:
        u32 FrameCount;
        core::map<core::stringc, SRotPosLinearCurve*> BoneCurveMap;
    };
    
}
}

#endif
