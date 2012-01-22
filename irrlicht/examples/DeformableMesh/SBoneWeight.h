// Copyright (C) 2011 ousttrue
// This file is a append file of the "Irrlicht Engine".
// For conditions of distribution and use, see copyright notice in irrlicht.h

#ifndef __S_BONE_WEIGHT_H_INCLUDED__
#define __S_BONE_WEIGHT_H_INCLUDED__


namespace irr
{
namespace scene
{
    class ISkeleton;

    struct SBoneWeight
    {
        u32 bone0;
        u32 bone1;
        f32 weight0;

        SBoneWeight()
            : bone0(0), bone1(0), weight0(0)
        {
        }

        SBoneWeight(u32 b0, u32 b1, f32 w0)
            : bone0(b0), bone1(b1), weight0(w0)
        {
        }
    };

}
}

#endif
