#pragma once
#include "irrTypes.h"

namespace irr {

	class IReferenceCounted;

	extern "C" IRRLICHT_API u32 get_uid();
	extern "C" IRRLICHT_API void register_uid(u32 uid, IReferenceCounted *p);
	extern "C" IRRLICHT_API void unregister_uid(u32 uid);
	extern "C" IRRLICHT_API IReferenceCounted* get_from_uid(u32 uid);

	/*
    template<typename T>
    class IDGenerator
    {
		struct Deleter{
			unsigned int m_uid;

			Deleter(unsigned int uid): m_uid(uid){}
			~Deleter(){ remove_from_map(m_uid); }
		};
		Deleter m_deleter;
        unsigned int m_uid;

    public:
        IDGenerator():m_uid(generate_uid()), m_deleter(m_uid)
        {
            s_uid_map.set(m_uid, this);
        }

        unsigned int uid()const 
        {
            return m_uid;
        }

        ////////////////////
        // static
        ////////////////////
    private:
        static core::map<unsigned int, IDGenerator*> s_uid_map;
    public:
        static unsigned int generate_uid(){ 
	        static unsigned int next_uid=1;
            return next_uid++; 
        }

        static T* get_from_uid(unsigned int uid){
            return (T*)s_uid_map.find(uid);
        }

		static void remove_from_map(unsigned int uid){
            s_uid_map.remove(uid);
		}
    };
	template <typename T> core::map<unsigned int, IDGenerator<T>*> IDGenerator<T>::s_uid_map;
	*/
}
