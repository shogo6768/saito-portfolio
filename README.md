# ポートフォリオ紹介
https://plusit-1.com/ <br><br>
『Plus IT（プラスイット）』はPCスキルUPをテーマに、コンテンツ学習のためのWebアプリケーションです。

お試しするにあたって、ログインが必要な機能がいくつかございます。
ゲストログイン機能も実装していますのでぜひログイン状態でご確認いただけると幸いです。

スマホ利用も想定しているのでモバイルからも気軽にお試し下さい！

なお以降は以下の立て付けについて解説しています。

* Plus ITの概要
* 実装機能について
* 使用技術について

# Plus ITの概要

### テーマ
PCスキルUPのためのコンテンツ学習サイト

### テーマ選定の背景
テーマ選定では、身近な課題を解決するための内容をテーマにしようと考え、"PCスキル"にしました。
なぜ"PCスキル"かというと、前職での経験としてPCスキルについては、かなり個人差があったからです。
またコロナの影響もあり、在宅勤務の機会が増えていたため、Officeのような基本的なPCスキルからZoom等の電話会議までカバーできるようなコンテンツサイトがあればいいと思い、今回のテーマ選定に至りました。

### こだわりポイント
"ユーザー目線"を意識して実装機能を選定しました。具体的には、コンテンツ記事の閲覧に加えて、各ユーザーに対しオススメ記事を表示する"リコメンド機能"や、よりピンポイントでユーザーの課題解決ができるよう
ユーザー同士による"Q&A機能"を実装しています。またUIについては、私の友人等の意見をもらいながら完成させています。具体的な内容については以降で解説していますのでご確認いただけると幸いです。

# 実装機能について

実装機能は大きく分けて３つあります。

## ①ブログ機能（記事の閲覧）

#### ◆コンテンツをカテゴリー別、ランキング順に表示
![ランキング](https://user-images.githubusercontent.com/73920107/109258703-23de2a80-783e-11eb-9717-b12e4e2a703e.gif)

#### ◆コンテンツの検索が可能
![検索](https://user-images.githubusercontent.com/73920107/109258776-44a68000-783e-11eb-939d-2acb265c8dd7.gif)

#### ◆ご意見箱の設置（コンタクトフォーム）
![コンタクトフォーム ](https://user-images.githubusercontent.com/73920107/109259483-a74c4b80-783f-11eb-8f77-fc813d75bc24.gif)

#### ◆Wordpressのようなエディタ　※記事投稿は管理者以外使えない設定
![ckeditor](https://user-images.githubusercontent.com/73920107/109257700-0f009780-783c-11eb-8035-54bc6ea017b1.gif)

## ②ユーザー機能　※ログイン要

#### ◆基本的な認証機能（新規登録、ログイン、ログアウトetc）
![認証](https://user-images.githubusercontent.com/73920107/109255102-aa8f0980-7836-11eb-8e6d-f8a445adfb7f.gif)

#### ◆閲覧履歴に応じてリコメンド記事を表示
![リコメンド](https://user-images.githubusercontent.com/73920107/109258732-32c4dd00-783e-11eb-81c9-2f816ecb022e.gif)


#### ◆お好みの記事をお気に入りに登録できる
![お気に入り](https://user-images.githubusercontent.com/73920107/109258684-1628a500-783e-11eb-9d15-6ad7b6320bc4.gif)


## ③ユーザー同士のQ&A機能　※ログイン要

#### ◆ログイン要のためログインしてない場合はログイン画面に遷移
![アクセス制限](https://user-images.githubusercontent.com/73920107/109258662-07da8900-783e-11eb-9751-6436f18fde02.gif)


#### ◆質問内容は"新着"や"未回答"等でソート可能
![質問ソート](https://user-images.githubusercontent.com/73920107/109258841-63a51200-783e-11eb-92b5-7f1e9d9d1ac8.gif)


#### ◆質問投稿
![質問](https://user-images.githubusercontent.com/73920107/109258791-4d975180-783e-11eb-8996-40de47728289.gif)


#### ◆回答
![回答](https://user-images.githubusercontent.com/73920107/109258756-3ce6db80-783e-11eb-8e01-24a85dd7bc8e.gif)


#### ◆質問編集/削除機能（回答編集/削除機能もあり） ※質問者 と編集者が一致する場合のみ編集可能
![質問の編集](https://user-images.githubusercontent.com/73920107/109257816-496a3480-783c-11eb-89e5-07b46e3f9ed2.gif)

## その他特徴　レスポンシブ対応
![レスポンシブ](https://user-images.githubusercontent.com/73920107/109257801-4707da80-783c-11eb-895e-af010286f4f2.gif)

ぜひ実際にお試しください！

https://plusit-1.com/

# 使用技術について

#### ◆フロントエンド
* HTML/CSS（マークアップ）
* Javascript （フロントエンド）

#### ◆バックエンド
* Python（バックエンド）
* Django（フレームワーク）
* Pillow（画像処理）
* CKEditor（WYSIWYGエディタ）
* SendGrid（メール送信）
* environ（シークレット変数の取り扱い）
* PostgreSQL（データベース）

#### ◆テスト
* Unit テスト（django views.py. models.py, forms.py）

#### ◆インフラ
* AWS VPC（ネットワーク）
* AWS EC2（仮想サーバー）
* AWS Route53（ドメインとの紐付け）
* Gunicorn（Webアプリ起動）
* Nginx（Webサーバー）
* Github（バージョン管理）









