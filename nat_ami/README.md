# NAT AMI作成

これは、NATインスタンスのAMIを作成する。なお、このうち、InstallCloudWatchAgentComponentは後でほかでも使うので、ここで構築することをお勧めする。

ここで構築しない場合は、このドキュメントをもとに手作業で作るなどの作業をおすすめする。

## パラメータの説明

* SubnetId - 必須。サブネットIDを指定する。パブリックサブネットである必要あり
* SecurityGroupIds - 必須。セキュリティグループIDを指定する。1つ指定すればよいため、コンテナ用のセキュリティグループを使うとよい