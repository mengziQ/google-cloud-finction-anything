# Google Cloud Functionを導入する  
## 参考レポジトリ  
https://github.com/GINK03/google-cloud-function-pythonic

## 注意  
Linux Debianだとうまくpypy3が動作しない可能性あり  
メモ：  
自分のGCPアカウントでうまく動作しなかったため、最終的にはyuriでGCFを実行した  

## 導入の流れ  
- Google Cloud SDKを導入  
- gcloudをインストール  
- PyPy3を導入  
- GCFを作成  
- 作成したGCFにPyPy3のファイルを入れる  
- GCFをデプロイする  
- URLにアクセスしてGCFを起動させる  


## 1. gcloudの導入  
### 1-1. gcloudとは  
GCPをコマンドラインで操作できるツール。  
Google Cloud SDKとかいうものの一部であるため、gcloudを使うにはGoogle Cloud SDKをインストール&初期化する必要がある。  

### 1-2. gcloud導入理由  
GCFをコマンドラインでデプロイするため。  

### 1-3. 導入方法  
GoogleからSDKのファイルをダウンロードする。
```
$ wget https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-170.0.1-linux-x86_64.tar.gz
```
SDKのtarファイルを展開する。  
※オプション  
z:gzipを通して処理する  
x:書庫からファイルを取り出す  
v:処理したファイルの一覧を詳細に表示する  
f:指定した書庫ファイルまたはデバイスを使用する  
```
$ tar zxvf google-cloud-sdk-170.0.1-linux-x86_64.tar.gz?hl=ja
```
SDKディレクトリの中の、インストール用シェルスクリプトを実行する  
```
$ ./google-cloud-sdk/install.sh
```
gcloudの初期設定的な？
```
$ ./google-cloud-sdk/bin/gcloud init
```
.bashrcにこの記述を追加し、相対パスを入力しなくても使えるようにする  
```
PATH=$HOME/google-cloud-sdk/bin:$PATH
```
gcloudのインストール  
```
$ gcloud components update beta && gcloud components install
```
補足：GCPにバケットを作るコマンド  
```
$ gsutil mb gs://{YOUR_STAGING_BUCKET_NAME}
```

## 2. PyPy3導入  
### 1-1. PyPy3とは  
pythonで書かれたpython言語。  
様々なLinux環境で動作するように調整され、コンパイル済みで環境依存が少ない。  

### 2-2. PyPy3導入理由  
GCFはnode.jsでしか動作しないが、pythonでスクリプトを記述したいから。  

### 2-3. 導入方法  
pypy3のbzipファイルを解凍し、tarファイルを展開する
```  
$ bzip2 -d pypy3-v5.9.0-linux64.tar.bz2  
$ tar xvf pypy3-v5.9.0-linux64.tar  
```
作成したGCFの中にpypy3を移動させる    
```
$ mv pypy3-v5.9.0-linux64 {YOUR_GOOGLE_CLOUD_FUNCTION_DIR}  
```
pypy3の中の、pipの機能を有効化するスクリプトを実行する  
```
./pypy3-v5.9.0-linux64/bin/pypy3 -m ensurepip
```

## 3. 関数を作ったら、デプロイする  
### 3-1. デプロイ方法  
メモ:  
nard-treeさんのレポジトリの場合、deploy.shを「sh deploy.sh」で実行する  
```
$ gcloud beta functions deploy ${YOUR_CLOUD_FUNCTION_NAME} --stage-bucket ${YOUR_STAGING_BUCKET} --trigger-http
```

## 4. デプロイした関数を動かす  
コードをデプロイするとapiのURLが標準出力に表示されるので、そのURLにアクセスする  
メモ:  
nard-treeさんのレポジトリの場合、queryが実行された時にURLにアクセスしている。  
google-cloud-function-pythonicの場合、GCFが起動したときに最初に実行されるindex.js内で、queryを実行している。    
```
$ curl https://us-central1-machine-learning-173502.cloudfunctions.net/pycall
```

## 補足：GCFのコンソールを確認    
GCFがデプロイされたか、などはコンソールからも確認できる。  

