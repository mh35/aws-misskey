# EC2用ロール設定

このCloudFormationテンプレートをデプロイすると、Amazon SSMで管理され、Amazon CloudWatchに情報を送信可能なインスタンスのロールが作成可能である。

## 注意事項

IAMリソースを作成するので、CAPABILITY\_IAMを指定しないとスタックの作成に失敗する点に注意。