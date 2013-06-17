#include "IDGenerator.h"
#include "IReferenceCounted.h"
#include "irrMap.h"

namespace irr {

	extern "C" IRRLICHT_API u32 get_uid()
	{
		static u32 uid=1;
		return uid++;
	}

	static core::map<u32, IReferenceCounted*> g_map;

	extern "C" IRRLICHT_API void register_uid(u32 uid, IReferenceCounted *p)
	{
		g_map.set(uid, p);
	}

	extern "C" IRRLICHT_API void unregister_uid(u32 uid)
	{
		auto found=g_map.remove(uid);
	}

	extern "C" IRRLICHT_API IReferenceCounted* get_from_uid(u32 uid)
	{
		auto found=g_map.find(uid);
		if(!found){
			return 0;
		}
		return found->getValue();
	}
}

