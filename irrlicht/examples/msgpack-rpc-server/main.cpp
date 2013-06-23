#include "RenderLoop.h"


int main()
{
    const static int PORT=8070;

    // renderer
    RenderLoop app;

    // server
    boost::asio::io_service server_io;
    msgpack::rpc::asio::server server(server_io, [&app](
                const msgpack::object &msg, 
                std::shared_ptr<msgpack::rpc::asio::session> session)
            {
            app.enqueue(msg, session);
            });
    server.listen(boost::asio::ip::tcp::endpoint(boost::asio::ip::tcp::v4(), PORT));
    boost::thread server_thread([&server_io](){ server_io.run(); });

    // blocking
    app.run();

    server_io.stop();
    server_thread.join();

	return 0;
}

