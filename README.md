# Google Cloud Functionを使う  
参考レポジトリ：[google-cloud-function-pythonic](https://github.com/GINK03/google-cloud-function-pythonic)  
仕事で、EC2を定期的にシャットダウンするためにGoogle Cloud FunctionとLambdaを使いました。  
なんでGoogleCloud Function使ったんだろう？笑  

## 仕組み その１「定期実行」  
lambdaでGCFを起動させて、GCFでEC2をシャットダウンする。  
元々はGCFだけで実装予定だったけど、定期実行の仕組みがGCFになかったっぽいので、GCFの起動のためだけにlambda関数を作成した。  

## 実装でハマったポイント  
- GCPではDebianのインスタンスを作成して、そこで上記作業をしていたが、pypyがうまく動かなかった。ubuntu(yuri)で動かしたら動いた。  
- AWSのIAMユーザーにアタッチするポリシーは「AdministratorAccess」でないと動かない。  
- 「AdministratorAccess」のポリシーを付与しても、別のポリシーでIP制限されると起動しなくなる。この時、Lambdaは起動しているぽい(GCFが起動しているので)。
- なので、IP制限しているポリシーから「Lambda」のグループをデタッチしたけど当然動かない。  
- とにかく、Lambdaは起動するが、起動したからといってEC2にアクセスできるのかは分からない。まだ試してない。  
- Lambda関数の関数コードはzipファイルをアップロードしたが、この時、zipファイルの作成方法が特殊。ディレクトリごと圧縮してはいけない。aws_lambda_driverの中身のみを圧縮する。コマンドは以下のイメージ。  
```
$ cd aws_lambda_driver
$ zip -r ../ec2_onoff.zip .
```

## 仕組み その2「スマホのショートカットから実行」  
GCFだけで実装。  
実装後は、スマホのショートカット機能でGCFのトリガーとなるURLを登録する。  
GCPからGCFを起動する関係か、GCPの認証を通す必要がある。  

## 実装でハマったポイント  
- GCFを使うための認証を通すには、「サービスアカウントキー」が必要。「APIとサービス」→「認証情報」→「認証情報の作成」→「サービスアカウントキー」→「新しいサービスアカウント」→「サービスアカウント名」を適当につける→役割「Compute Engine」の「Compute Admin」→「キーのタイプ」はJSONで作成  



