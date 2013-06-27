#include "pmdloader.h"

namespace polymesh { namespace pmd {

// 38bytes
template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, Vertex &v)
    {
        reader 
            >> v.pos
            >> v.normal
            >> v.uv
            >> v.bone0
            >> v.bone1
            >> v.weight0
            >> v.edge_flag
            ;
        return reader;
    }

// 70bytes
template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, Material &m)
    {
        reader
            >> m.diffuse_color
            >> m.alpha
            >> m.specular
            >> m.specular_color
            >> m.mirror_color
            >> m.toon_index
            >> m.flag
            >> m.vertex_count
            ;
        m.texture=reader.getString(20);
        return reader;
    }

// 39bytes
template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, Bone &b)
    {
        b.name=reader.getString(20);
        reader
            >> b.parent_index
            >> b.tail_index
            ;
        reader.getEnum<BONE_TYPE, unsigned char>(b.type);
        reader
            >> b.ik_index
            >> b.pos
            ;
        return reader;
    }

template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, IK &ik)
    {
        // 11bytes
        reader
            >> ik.index
            >> ik.target
            >> ik.length
            >> ik.iterations
            >> ik.weight
            ;
        // 2 x length bytes
        ik.children.resize(ik.length);
        reader >> ik.children;
        return reader;
    }

template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, Morph &m)
    {
        // 25bytes
        m.name=reader.getString(20);
        reader >> m.vertex_count;
        reader >> m.type;
        // 12 x vertex_count bytes
        m.indices.resize(m.vertex_count);
        m.pos_list.resize(m.vertex_count);
        for(unsigned short i=0; i<m.vertex_count; ++i){
            reader 
                >> m.indices[i]
                >> m.pos_list[i]
                ;
        }
        return reader;
    }

template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, RigidBody &r)
    {
        r.name=reader.getString(20);
        reader
            >> r.boneIndex
            >> r.group
            >> r.target
            ;
        reader.getEnum<RIGID_TYPE, unsigned char>(r.rigidType);
        reader
            >> r.w
            >> r.h
            >> r.d
            >> r.position
            >> r.rotation
            >> r.weight
            >> r.posAttenuation
            >> r.rotAttenuation
            >> r.recoile
            >> r.friction
            ;
        reader.getEnum<PROCESS_TYPE, unsigned char>(r.processType);
        return reader;
    }

template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, Joint &j)
    {
        j.name=reader.getString(20);
        reader
            >> j.rigidA
            >> j.rigidB
            >> j.pos
            >> j.rot
            >> j.constraintPosA
            >> j.constraintPosB
            >> j.constraintRotA
            >> j.constraintRotB
            >> j.springPos
            >> j.springRot
            ;
        return reader;
    }


class Impl
{
    Loader &l;
public:
    Impl(Loader &loader)
        : l(loader)
        {}

    template<typename READ>
        bool parse(READ read)
        {
            BinaryReader<READ> reader(read);
            if(!parseHeader(reader)){
                return false;
            }
            unsigned char byte=0;
            unsigned short word=0;
            unsigned int dword=0;
            parseVector(reader, dword, l.vertices);
            parseVector(reader, dword, l.indices);
            parseVector(reader, dword, l.materials);
            parseVector(reader, word, l.bones);
            parseVector(reader, word, l.ik_list);
            parseVector(reader, word, l.morph_list);
            {
                unsigned char count;
                reader >> count;
                for(unsigned int i=0; i<count; ++i){
                    unsigned short facepos;
                    reader >> facepos;
                }
            }
            {
                unsigned char count;
                reader >> count;
                l.bone_name_list.resize(count);
                for(unsigned int i=0; i<count; ++i){
                    l.bone_name_list[i]=reader.getString(50);
                }
            }
            parseVector(reader, dword, l.bone_list);
            if(reader.eof()){
                return true;
            }

            ////////////////////////////////////////////////////////////
            // extended data
            ////////////////////////////////////////////////////////////
#ifdef DEBUG
            std::cout << "has extended data" << std::endl;
#endif
            // english
            ////////////////////////////////////////////////////////////
            unsigned char extend;
            reader >> extend;
            if(extend){
                l.english_mdoel_name=reader.getString(20);
                l.english_comment=reader.getString(256);
                l.english_bones.resize(l.bones.size());
                for(size_t i=0; i<l.english_bones.size(); ++i){
                    l.english_bones[i]=reader.getString(20);
                }
                l.english_morphs.resize(l.morph_list.size()-1);
                for(size_t i=0; i<l.english_morphs.size(); ++i){
                    l.english_morphs[i]=reader.getString(20);
                }
                l.english_bone_name_list.resize(l.bone_name_list.size());
                for(size_t i=0; i<l.english_bone_name_list.size(); ++i){
                    l.english_bone_name_list[i]=reader.getString(50);
                }
            }
            if(reader.eof()){
                return true;
            }

            // toone texture
            ////////////////////////////////////////////////////////////
            for(size_t i=0; i<10; ++i){
                std::string toon_texture=reader.getString(100);
            }
            if(reader.eof()){
                return true;
            }

            // physics
            ////////////////////////////////////////////////////////////
            parseVector(reader, dword, l.rigids);
            parseVector(reader, dword, l.joints);

            // end
            assert(reader.eof());

            return true;
        }

private:
    template<typename READER, typename COUNTER, typename OUTVECTOR>
        void parseVector(READER &reader, COUNTER count, OUTVECTOR &vector)
        {
            reader >> count;
            vector.resize(count);
            reader >> vector;
        }

    template<typename READER>
        bool parseHeader(READER &reader)
        {
            if(reader.getString(3)!="Pmd"){
                //std::cout << "invalid pmd" << std::endl;
                return false;
            }
            reader >> l.version;
            if(l.version!=1.0){
                std::cout << "invalid vesion: " << l.version <<std::endl;
                return false;
            }
            l.name=reader.getString(20);
            l.comment=reader.getString(256);

            return true;
        }
};


////////////////////////////////////////////////////////////
// Loader
////////////////////////////////////////////////////////////
Loader::Loader()
    : version(0)
    {}

bool Loader::parse(char *buf, unsigned int size)
{
    Impl impl(*this);
    BufferRead reader(buf, size);
    if(!impl.parse(reader)){
        return false;
    }
    if(!validate_()){
        return false;
    }
    return true;
}

bool Loader::validate_()
{
    if(!morph_list.empty()){
        // validate morph
        assert(morph_list[0].type==MORPH_BASE);
        // check base
        Morph &base=morph_list[0];
        for(size_t i=0; i<base.vertex_count; ++i){
            assert(vertices[base.indices[i]].pos==base.pos_list[i]);
        }
        // check each face
        for(size_t i=1; i<morph_list.size(); ++i){
            Morph &m=morph_list[i];
            assert(m.type!=MORPH_BASE);
        }
    }
    return true;
}


} // namespace
} // namespace
