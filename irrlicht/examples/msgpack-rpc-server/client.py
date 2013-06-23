#!/usr/bin/env python

import tornado_msgpack
import tornado.ioloop
import threading


if __name__=="__main__":
    port=8070

    def starter(target):
        def func():
            print("{0} start".format(target))
            target.start()
            print("{0} finished".format(target))
        return func

    # client
    client_loop=tornado.ioloop.IOLoop()
    client_thread=threading.Thread(target=starter(client_loop))
    client=tornado_msgpack.Client(client_loop)
    def on_status_changed(session, status):
        print(status)
    client.session.attach_status_callback(on_status_changed)
    client.session.connect("localhost", port)
    client_thread.start()

    def on_receive(result):
        print("on_receive:{0}".format(result))

    future=client.call_async_with_callback(on_receive, "scene_getmesh", "../../media/sydney.md2")
    future.join()
    mesh=future.message[3]

    future=client.call_async_with_callback(on_receive, "scene_add_animatedmesh_scenenode", mesh)
    future.join()
    node=future.message[3]

    future=client.call_async_with_callback(on_receive, "scene_add_camerascenenode", 0, 
            [0.0, 30.0, -40.0], 
            [0.0, 5.0, 0.0])
    future.join()
    camera=future.message[3]

    future=client.call_async_with_callback(on_receive, "driver_get_texture", "../../media/sydney.bmp")
    future.join()
    texture=future.message[3]
    
    future=client.call_async_with_callback(on_receive, "scenenode_set_material_texture", node, 0, texture);
    future.join()

    client_loop.stop()
    client_thread.join()

