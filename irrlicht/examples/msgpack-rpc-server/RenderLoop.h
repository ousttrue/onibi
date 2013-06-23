#include <msgpack/rpc/asio.h>
#include <memory>

namespace irr {
	class IrrlichtDevice;
}

class MessageQueue;
class RenderLoop
{
    irr::IrrlichtDevice *m_device;
    volatile bool m_loop;
    volatile bool m_ready;
    const static int PORT=8070;

    std::unique_ptr<MessageQueue> m_queue;
    msgpack::rpc::asio::dispatcher m_dispatcher;

public:
    RenderLoop();
   ~RenderLoop();
    bool ready()const{ return m_ready; }
    void enqueue(const msgpack::object &obj, std::shared_ptr<msgpack::rpc::asio::session> session);
    void stop(){ m_loop=false; }
    void run();

private:
    bool initialize();
    void loop();
};

