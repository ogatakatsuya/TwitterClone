# YUZURIHA　インターン　成果物

## 完成画面
![image](https://github.com/user-attachments/assets/92853e4a-1a38-4624-8aec-a86556619e6e)

## 機能
- 認証機能(ログイン・サインアップ・ログアウト)
- ツイート機能
- リプライ機能
- フォロー機能
- いいね機能
- プロフィール機能
- プロフィール編集機能
- 画像アップロード機能(アイコン・投稿)

## 開発環境
![image](https://github.com/user-attachments/assets/9ec00a9b-9f51-4aab-8fa8-27fc32485ef6)

## インフラ
![image](https://github.com/user-attachments/assets/5117961d-4579-4d8e-b9d9-8e2c4f2e4952)

## CI
- ruffによるformatとlint
- pytestによる、単体テストと統合テストの実施
  - 記事を書きました（ https://qiita.com/Katsuya_Ogata/items/bf722219c2aa454bb0eb ）

## CD
- CodePipelineとCodeDeployによるCDの実現
  - mainにpushされるとEC2インスタンスにS3を介してコードがアップロードされる
  - appspec.ymlを実行し、依存関係のインストールとビルドを実行
  - systemdを用いてdaemon化してあるため、自動で起動

