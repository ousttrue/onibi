#include "vmdloader.h"
#include <algorithm>


namespace polymesh { namespace vmd {


template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, Bone &b)
    {
        b.name=reader.getString(15);
        reader
            >> b.frame
            >> b.pos
            >> b.q
            ;
        reader.getBytes(b.cInterpolationX, 16);
        reader.getBytes(b.cInterpolationY, 16);
        reader.getBytes(b.cInterpolationZ, 16);
        reader.getBytes(b.cInterpolationRot, 16);
        return reader;
    }


template<typename T>
    BinaryReader<T> &operator>>(BinaryReader<T> &reader, Morph &m)
    {
        m.name=reader.getString(15);
        reader
            >> m.frame
            >> m.influence
            ;
        return reader;
    }


class Implementation
{
    std::string &version;
    std::string &name;
    std::map<std::string, BoneBuffer::Ptr> &boneMap;
    std::map<std::string, MorphBuffer::Ptr> &morphMap;

public:
    Implementation(Loader *l)
        : version(l->version), name(l->name), 
        boneMap(l->boneMap), morphMap(l->morphMap)
        {}

    template<class READ>
        bool parse(READ &read)
        {
            BinaryReader<READ> reader(read);
            // check header
            std::string line=reader.getString(30);
            if(line=="Vocaloid Motion Data file"){
                version="1";
                name=reader.getString(10);
                return parseBody(reader);
            }
            else if(line=="Vocaloid Motion Data 0002"){
                version="2";
                name=reader.getString(20);
                return parseBody(reader);
            }
            else{
                //std::cout << "unknown header:" << line << std::endl;
                return false;
            }
        }


private:
    template<class READER>
        bool parseBody(READER &reader)
        {
            if(!parseFrame(reader)){
                return false;
            }
            sortBoneBuffer();
            if(!parseMorph(reader)){
                return false;
            }
            sortMorphBuffer();
            // light...
            // camera...
            return true;
        }

    void
        sortBoneBuffer()
        {
            typedef std::pair<std::string, BoneBuffer::Ptr> bonePair;
            for(auto it=boneMap.begin(); it!=boneMap.end(); ++it) {
                std::sort(
                        it->second->bones.begin(),
                        it->second->bones.end()
                        );
            }
        }

    void
        sortMorphBuffer()
        {
            typedef std::pair<std::string, MorphBuffer::Ptr> morphPair;
            for(auto it=morphMap.begin(); it!=morphMap.end(); ++it) {
                std::sort(
                        it->second->morphs.begin(),
                        it->second->morphs.end()
                        );
            }
        }

    template<class READER>
        bool parseMorph(READER &reader)
        {
            unsigned int count;
            reader >> count;
            //morphs.resize(count);
            for(unsigned int i=0; i<count; ++i){
                //morphs[i].read(reader);
                Morph m;
                reader >> m;
                if(morphMap.find(m.name)==morphMap.end()){
                    // not found
                    morphMap.insert(std::make_pair(
                                m.name, MorphBuffer::Ptr(new MorphBuffer)));
                }
                morphMap[m.name]->push(m);
            }
            return true;
        }

    template<class READER>
        bool parseFrame(READER &reader)
        {
            unsigned int count;
            reader >> count;
            //std::cout << count << "frames" << std::endl;
            //bones.resize(count);
            for(unsigned int i=0; i<count; ++i){
                //bones[i].read(reader);
                Bone b;
                reader >> b;
                if(boneMap.find(b.name)==boneMap.end()){
                    // not found
                    boneMap.insert(std::make_pair(
                                b.name, BoneBuffer::Ptr(new BoneBuffer)));
                }
                boneMap[b.name]->push(b);
            }
            return true;
        }
};


bool 
Loader::parse(char *buf, unsigned int size)
{
    BufferRead reader(buf, size);
    return Implementation(this).parse(reader);
}


}}
