# Basic Functionalities 
---
GoogleのCloud Speech-to-Text APIを利用した質問応答プログラムになります。


### 実行環境
---
Ubuntu 16.04.5
Python3.5.2(virtualenv使用)
ROS kinetic


### Install
---
virtualenvのインストールとセットアップを行う。

```
$ pip install --upgrade virtualenv
$ cd [your-project]
$ virtualenv --python python3 env
```

その後、モジュールのインストールを行うが、

```
$ cd [your-project]
$ source env/bin/activate
```
を実行した後、仮想環境に入っていること、対話モードでpythonのバージョンが3系になっていることを確認する。

確認が取れたら、クライアントライブラリやrospyを仮想環境上にインストールする。

```
$ pip install --upgrade google-cloud-speech
$ pip install pyaudio
$ pip install rospkg
$ pip install python-levenshtein
```


### RosTopic
---
- 対話のON/OFF

```
conversation/start
conversation/stop
```
Bool型のtopicを扱っています。
**<注意>**
Falseでstart,Trueでstopになります。 ややこしいね、ごめんね。


### 実行
---
```
$ cd [your-project]
$ source env/bin/activate
$ rosrun [project_name] transcribe.py
```
