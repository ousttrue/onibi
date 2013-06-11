++++++++++++++++
Irrlicht MMD拡張
++++++++++++++++
IrrlichtのIAnimatedMeshSceneNodeとしてPMDを読み込んでVMDモーションでアニメーションさせるコードです。
bullet+mmdの実験台として整備予定。

使い方
======
main.cppを参照。

依存ライブラリ
==============
irrlicht-1.7.3
bullet-2.79

ビルド方法
===========
premake4.lua内のirrlicht, bulletなどの場所を参照している箇所を修正する。

::
  > premake4.exe vs2010
  (premake4.4以降)
irrmmd.slnが生成されるのでvcでビルドする。

ToDo
====
* rigid廃止。LinearMathで置き換える
* マテリアル方面
* ベジェ補完
* 動画書き出し
* もうちっと使いやすくする
* モーションブレンドとか

内容
====
* premake4.lua
* README.rst
* main.cpp

* irrmmd/utility.cpp
* irrmmd/utility.h
* irrmmd/utility_linux.cpp
* irrmmd/utility_win32.cpp

ボーンインターフェースと実装
----------------------------
* irrmmd/IJoint.h
* irrmmd/CJoint.cpp
* irrmmd/CJoint.h
* irrmmd/btjoint.cpp(実験用。未使用)
* irrmmd/btjoint.h(実験用。未使用)

動画書き出し
------------
* irrmmd/CAviCreator.cpp(動画書き出し。未使用)
* irrmmd/CAviCreator.h(動画書き出し。未使用)

スキニング
----------
* CCurve.h
* CCustomSkinnedMesh.cpp(本体)
* CCustomSkinnedMesh.h
* CVMDCustomSkinMotion.cpp
* CVMDCustomSkinMotion.h
* SCurve.h
* SRotPosKey.h

ローダ
------
* CMQOMeshFileLoader.cpp
* CMQOMeshFileLoader.h
* CPMDMeshFileLoader.cpp
* CPMDMeshFileLoader.h

bullet
------
* irrbullet.cpp
* irrbullet.h
* IRigidBody.h
* CRigidBody.cpp
* CRigidBody.h
* IShape.h
* CShape.cpp
* CShape.h

irrlicht拡張
------------
* irrmmd.cpp
* irrmmd.h
* CSceneNodeAnimatorCameraRokuro.cpp
* CSceneNodeAnimatorCameraRokuro.h

libpolymesh
-----------
汎用の3Dフォーマット読み込みの作りかけ

* libpolymesh/bvhloader.cpp
* libpolymesh/bvhloader.h
* libpolymesh/core.h
* libpolymesh/libpolymesh.lua
* libpolymesh/mqoloader.cpp
* libpolymesh/mqoloader.h
* libpolymesh/pmdloader.cpp
* libpolymesh/pmdloader.h
* libpolymesh/premake4.lua
* libpolymesh/vmdloader.cpp
* libpolymesh/vmdloader.h
* libpolymesh/xloader.cpp
* libpolymesh/xloader.h

rigid
-----
剛体変換(回転+移動)の数学ライブラリ
Vector3やMatrix4を定義している。

* rigid/matrix.h
* rigid/premake4.lua
* rigid/quaternion.cpp
* rigid/quaternion.h
* rigid/rigid.cpp
* rigid/rigid.h
* rigid/rigid.lua
* rigid/rigid_test.cpp
* rigid/rigid_test.lua
* rigid/vec.h

history
=======
* 2010作成
* 20101026 vc2010向けに修正。github登録

