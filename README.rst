==============================
[鬼火]オープンソース詰め合わせ
==============================
| Irrlichtが独語で鬼火らしいので直訳。
| IrrlichtとBulletを中心に3D用途で使うライブラリをMinGWでビルドしやすいようにpremake4を使って編成しました。

* Irrlicht-1.8
* bullet-2.81
* freetype
* glew
* freeglut
など

| Windows+(mingw|vc2010 express edition)で楽にビルドできるようにpremake4.luaで構成しています。
| ライセンスついては、各ライブラリに準拠してください。

.. contents:: Table of Contents
_
URL
===
* https://github.com/ousttrue/onibi

ToDo
====
* msgpack-rpc経由でシーンを構築するUIをなんか作る(pyQTとか？)
* IrrlichtMLのfreetypeフォントを再マージする？

更新
====
2013-06-16
----------
* msgpackとmsgpack-rpc-asioを追加

2013-06-12
----------
* irrmmdと合体。とりあえずvc2010で全部ビルドするところまで
* bullet-2.81に更新。_maxdot_largeがリンクできぬ。謎
* irrlicht-1.8に更新
* swig関連除去

2013-06-11
----------
* vs2010でビルドしてみた

2012-01-22
----------
* githubに引越し

2011-11-21
----------
* Irrlichtにbulletが入ってしまったり構成がよろしくないのでirrmmdを取り除いた

ディレクトリ構成
================
freetype
--------

freetype-2.4.6。The FreeType License。

bullet
------

bullet-2.79のsrcディレクトリ。zlibライセンス。

* swigでラップする都合で少し改造してある(クラス内で定義されたものを外に出すなど)。

bullet/swigbullet
-----------------

bulletのswigによるラッパ。

bulletdemos
-----------

bullet-2.79のDEMOS。
    
irrlicht
--------

Irrlicht-1.72のincludeとsrcディレクトリzlibライセンス。

* swigでラップする都合で少し改造してある(クラス内で定義されたものを外に出すなど)。
* IrrlichtMLとマージ済み

irrlicht/siwgirr
----------------

Irrlichtのswigによるラッパ。

bzip2
-----

Irrlicht-1.72のsrc/Irrlicht/bzip2ディレクトリ。

jpeglib
-------

Irrlicht-1.72のsrc/Irrlicht/jpeglibディレクトリ。

libpng
------

Irrlicht-1.72のsrc/Irrlicht/libpngディレクトリ。

lzma
----

Irrlicht-1.72のsrc/Irrlicht/lzmaディレクトリ。

zlib
----

Irrlicht-1.72のsrc/Irrlicht/zlibディレクトリ。

glew
----

glew-1.7.0。BSDライセンス。

freeglut
--------

Freeglut 2.6.0。X-Consortiumライセンス。bulletdemosが使う。

msgpack
-------

msgpack 0.5.7

premake4.exe
------------

* http://industriousone.com/premake

各ディレクトリのpremake4.luaはpremake4向けのプロジェクト定義です。

ビルド環境
==========
1) mingw-get-inst-20111118.exeでC:/MinGWにMinGWとmsysをインストールする。
2) C:/MinGW/msys/1.0/msys.batでshellに入る
3) 環境変数::

   export LANG=C
   export PATH=/mingw/bin:$PATH

ビルド方法
==========

依存ライブラリのスタティックライブラリをビルド
----------------------------------------------
::

    > cd onibi
    > ./premake4 gmake
    > make

Irrlichtのdllをビルド
---------------------
::

    > cd onibi/irrlicht
    > ../premake4 gmake
    > make

bulletのビルド
--------------
::

    > cd onibi/bullet
    > ../premake4 gmake
    > make

irrmmdのビルド
--------------
::

    > cd onibi/irrmmd
    > ../premake4 gmake
    > make

Irrlicht examplesのビルド
-------------------------
::

    > cd onibi/irrlicht/examples
    > ../../premake4 gmake
    > make

| メディア置き場が"../../media"になっているので、実行時に
| ../../mediaにIrrlicht/mediaをコピーする必要があります。

bulletdemosのビルド
-------------------
::

    > cd onibi/bulletdemos
    > ../premake4 gmake
    > make

