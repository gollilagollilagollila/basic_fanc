# Basic Functionalities 
GoogleのCloud Speech-to-Text APIを利用した質問応答プログラムになります。


### Environment
Ubuntu 16.04.5
Python3.5.2(virtualenv使用)
ROS kinetic


### Install
Google CloudのSDKをインストール
~~~
$ curl https://sdk.cloud.google.com | bash
$ exec -l $SHELL
$ gcloud version

$ sudo pip install --upgrade google-cloud-speech
$ gcloud auth application-default login
~~~
APIキーを設定
~~~
$ export GOOGLE_APPLICATION_CREDENTIALS=鍵の(Full)PATH
~~~
virtualenvのインストールとセットアップ
~~~
$ pip install --upgrade virtualenv
$ cd [your-project]
$ virtualenv --python python3 env
~~~
仮想環境に入る
~~~
$ cd [your-project]
$ source env/bin/activate
~~~
**(注意)対話モードでpythonのバージョンが3系になっていることを確認すること**

モジュールのインストール
~~~
$ pip install --upgrade google-cloud-speech
$ pip install pyaudio
$ pip install rospkg
$ pip install python-levenshtein
~~~

### RosTopic
- 対話のON/OFF
   - 型はBool
~~~
conversation/start
conversation/stop
~~~
**<注意>**
Falseで実行,Trueで待機になります。ややこしいね、ごめんね。:bow:

### Run
~~~
$ cd [your-project]
$ source env/bin/activate
$ rosrun [project_name] transcribe.py
~~~

### Error
- `'https' scheme not supported in proxy URI` が出た時
~~~
export https_proxy=$http_proxy
~~~
