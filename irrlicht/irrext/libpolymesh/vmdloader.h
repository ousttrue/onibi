#ifndef MMD_VMD_LOADER_H
#define MMD_VMD_LOADER_H

#include "core.h"
#include <map>
#include <memory>

namespace polymesh {

  namespace vmd {

    typedef rigid::Vector3 Vector3;
    typedef rigid::Quaternion Quaternion;

    ////////////////////////////////////////////////////////////
    // Bone
    ////////////////////////////////////////////////////////////
    struct Bone
    {
      std::string name;
      unsigned int frame;
      Vector3 pos;
      Quaternion q;
      char cInterpolationX[16];
      char cInterpolationY[16];
      char cInterpolationZ[16];
      char cInterpolationRot[16];
     bool operator<(const Bone &rhs)const{ return frame<rhs.frame; }
    };
    inline std::ostream& operator<<(std::ostream &os, const Bone &rhs)
    {
      os
        << "<Bone "
        << '"' << rhs.name << '"' 
        << " " << rhs.frame << rhs.pos << rhs.q
        << ">"
        ;
      return os;
    }

    struct BoneBuffer
    {
      typedef std::shared_ptr<BoneBuffer> Ptr; 
      std::vector<Bone> bones;

      void push(const Bone &b){ bones.push_back(b); }
    };

    ////////////////////////////////////////////////////////////
    // Morph
    ////////////////////////////////////////////////////////////
    struct Morph
    {
      std::string name;
      unsigned int frame;
      float influence;

      bool operator<(const Morph &rhs)const{ return frame<rhs.frame; }
    };

    struct MorphBuffer
    {
      typedef std::shared_ptr<MorphBuffer> Ptr; 
      std::vector<Morph> morphs;

      void push(const Morph &m){ morphs.push_back(m); }
    };

    ////////////////////////////////////////////////////////////
    // Loader
    ////////////////////////////////////////////////////////////
    class Loader
    {
      public:
        std::string version;
        std::string name;
        typedef std::map<std::string, BoneBuffer::Ptr> BoneMap;
        BoneMap boneMap;
        typedef std::map<std::string, MorphBuffer::Ptr> MorphMap;
        MorphMap morphMap;

        bool parse(char *buf, unsigned int size);
    };

    inline std::ostream& operator<<(std::ostream &os, const Loader &rhs)
    {
      os
        << "<VMD " << rhs.name << std::endl
        << "[bones] " << rhs.boneMap.size() << std::endl
        << "[morphs] " << rhs.morphMap.size() << std::endl
        << ">"
        ;
      return os;
    }

  }

}

#endif // VMD_LOADER_H
