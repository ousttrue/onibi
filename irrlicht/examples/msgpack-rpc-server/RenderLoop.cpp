#include "RenderLoop.h"
#include <boost/thread.hpp>
#include <irrlicht.h>
#include <iostream>


struct Message
{
    msgpack::object object;
    std::shared_ptr<msgpack::rpc::asio::session> session;

    Message(const msgpack::object &o, std::shared_ptr<msgpack::rpc::asio::session> s)
        : object(o), session(s)
        {}
};


class MessageQueue
{
    irr::core::list<std::shared_ptr<Message>> m_queue;
    boost::mutex m_mutex;

public:
    void enqueue(std::shared_ptr<Message> msg)
    {
        boost::mutex::scoped_lock(m_mutex);
        m_queue.push_back(msg);
    }

    std::shared_ptr<Message> dequeue()
    {
        boost::mutex::scoped_lock(m_mutex);
        if(m_queue.empty()){
            return 0;
        }
        auto front=m_queue.begin();
        auto item=*front;
        m_queue.erase(front);
        return item;
    }
};


namespace msgpack {
    // pack
    template <typename Stream, typename HasUID>
        inline packer<Stream>& operator<< (packer<Stream>& o, HasUID *v)
        {
			if(v==0){
				o.pack(0);	
			}
			else{
				o.pack(v->uid());
			}
            return o;
        }

    // unpack
		template<typename HasUID>
    inline HasUID *& operator>> (
            object o, HasUID *&v)
    {
        unsigned int uid;
        o.convert(&uid);
		auto p=irr::get_from_uid(uid);
		v=dynamic_cast<HasUID*>(p);
        return v;
    }

    // irr::io::path
    // unpack
    inline irr::core::string<wchar_t>& operator>> (
            object o, irr::core::string<wchar_t>& v)
    {
        if(o.type != type::RAW) { throw type_error(); }

        // for only 7bit ascii
        std::vector<wchar_t> buf(o.via.raw.size);
        auto d=buf.begin();
        auto end=o.via.raw.ptr+o.via.raw.size;
        for(const char *p=o.via.raw.ptr; p!=end; ++p, ++d)
        {
            *d=*p;
        }
        v=irr::core::string<wchar_t>(&buf[0], buf.size());
        return v;
    }

    // irr::io::path
    // unpack
    inline irr::core::string<char>& operator>> (
            object o, irr::core::string<char>& v)
    {
        if(o.type != type::RAW) { throw type_error(); }
        v=irr::core::string<char>(o.via.raw.ptr, o.via.raw.size);
        return v;
    }

    // irr::core::position2d<s32>
    // unpack

    // irr::core::rect<s32>
    // unpack
    inline irr::core::rect<irr::s32>& operator>> (
            object o, irr::core::rect<irr::s32>& v)
    {
        if(o.type != type::ARRAY) { throw type_error(); }
        if(o.via.array.size!=4){ throw type_error(); }

        object* p = o.via.array.ptr;
        p->convert(&v.UpperLeftCorner.X);
        ++p;
        p->convert(&v.UpperLeftCorner.Y);
        ++p;
        p->convert(&v.LowerRightCorner.X);
        ++p;
        p->convert(&v.LowerRightCorner.Y);

        return v;
    }

    // irr::core::vector3df
    // pack
    template <typename Stream>
        inline packer<Stream>& operator<< (packer<Stream>& o, const irr::core::vector3df &v)
        {
            o.pack_array(3);
            o.pack(v.X);
            o.pack(v.Y);
            o.pack(v.Z);
            return o;
        }

    // unpack
    inline irr::core::vector3df& operator>> (
            object o, irr::core::vector3df& v)
    {
        if(o.type != type::ARRAY) { throw type_error(); }
        if(o.via.array.size!=3){ throw type_error(); }

        object* p = o.via.array.ptr;
        p->convert(&v.X);
        ++p;
        p->convert(&v.Y);
        ++p;
        p->convert(&v.Z);

        return v;
    }
}


RenderLoop::RenderLoop()
	: m_loop(false), m_device(0), m_ready(false), m_queue(new MessageQueue)
{
}

RenderLoop::~RenderLoop()
{
    if(m_device){
        m_device->drop();
        m_device=0;
    }
}

void RenderLoop::enqueue(const msgpack::object &obj, std::shared_ptr<msgpack::rpc::asio::session> session)
{
    m_queue->enqueue(std::make_shared<Message>(obj, session));
}

void RenderLoop::run()
{
    m_ready=initialize();
    if(!m_ready){
        return;
    }
    loop();
}

bool RenderLoop::initialize()
{
    if(m_device){
        return false;
    }
    m_device=irr::createDevice( 
            irr::video::EDT_SOFTWARE, 
            irr::core::dimension2d<irr::u32>(640, 480), 
            16,
            false, false, false, 0);
    if(!m_device){
        return false;
    }

    auto driver = m_device->getVideoDriver();
    auto smgr = m_device->getSceneManager();
    auto guienv = m_device->getGUIEnvironment();

    // register functions
    m_dispatcher.add_handler("scene_getmesh", [smgr](
                const irr::io::path& path
                )->irr::scene::IAnimatedMesh*
            {
            return smgr->getMesh(path);
            });

    m_dispatcher.add_handler("scene_add_animatedmesh_scenenode", [smgr](
                irr::scene::IAnimatedMesh* mesh
                )->irr::scene::IAnimatedMeshSceneNode*
            {
            return smgr->addAnimatedMeshSceneNode(mesh);
            });

    m_dispatcher.add_handler("scene_add_camerascenenode", [smgr](
                irr::scene::ISceneNode *parent,
                const irr::core::vector3df &position,
                const irr::core::vector3df &lookat
                )->irr::scene::ICameraSceneNode*
            {
            return smgr->addCameraSceneNode(parent, position, lookat);
            });

    m_dispatcher.add_handler("driver_get_texture", [driver](
                const irr::io::path& path
                )->irr::video::ITexture*
            {
            return driver->getTexture(path);
            });

    m_dispatcher.add_handler("scenenode_set_material_texture", [](
        irr::scene::ISceneNode* node,
        irr::u32 textureLayer,
        irr::video::ITexture* texture)
    {
        if(node){
            node->setMaterialTexture(textureLayer, texture);
        }
    });


    return true;
}

void RenderLoop::loop()
{
    if(!m_device){
        return;
    }

    m_loop=true;
    auto driver = m_device->getVideoDriver();
    auto smgr = m_device->getSceneManager();
    auto guienv = m_device->getGUIEnvironment();
    while(m_loop)
    {
        // consume event
        while(true){
            auto msg=m_queue->dequeue();
            if(!msg){
                break;
            }
            m_dispatcher.dispatch(msg->object, msg->session);
        }

        if(!m_device->run()){
            break;
        }

        driver->beginScene(true, true, 
                irr::video::SColor(255,100,101,140));

        smgr->drawAll();
        guienv->drawAll();

        driver->endScene();
    }
}

