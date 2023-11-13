# Misskey用VPC

このディレクトリは、VPCを作成するテンプレートファイルのためのものである。

## スタックのパラメータ

* VpcCidr - VPCのCIDR。/16のプライベートIPアドレスを指定する。デフォルトは10.1.0.0/16
* CreateNATGateway - NAT Gatewayの作り方。デフォルトはNone
  * EachAZ - 各AZに作成する。コストは高いが、AZ障害でインターネットアクセスが途絶することがなくなるため、高信頼度を求める場合に有用
  * OneAZ - 最初のAZに作成する。そこまで高信頼度は必要ないが、プライベートサブネットにコンテナなどを配置する場合に
  * None - NAT Gatewayを作成しない。パブリックサブネットにコンテナなどを配置し、パブリックIPアドレスを割り振るなら、このオプションを採用可
* CreateEc2MessagesEndpoint - EC2 MessagesのVPCエンドポイントを作成するか。デフォルトはfalse
* CreateSsmEndpoint - SSMのVPCエンドポイントを作成するか。デフォルトはfalse
* CreateSsmMessagesEndpoint - SSM MessagesのVPCエンドポイントを作成するか。デフォルトはfalse
* CreateKmsEndpoint - KMSのVPCエンドポイントを作成するか。デフォルトはfalse
* CreateCloudWatchLogsEndpoint - CloudWatch LogsのVPCエンドポイントを作成するか。デフォルトはfalse
* CreateEcrDockerEndpoint - ECRのDocker用VPCエンドポイントを作成するか。デフォルトはfalse
* CreateEcrApiEndpoint - ECRのAPI用VPCエンドポイントを作成するか。デフォルトはfalse