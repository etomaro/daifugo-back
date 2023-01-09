# ローカル環境構築

参考

[https://zenn.dev/sawao/articles/15a9cf0e3360a7](https://zenn.dev/sawao/articles/15a9cf0e3360a7)

流れ

1. reactのプロジェクト作成
2. APIを使用するためのライブラリをReactにインストール(axios)
3. ローカル環境に仮想環境を作成(venv)
4. 仮想環境にfastapiとサーバー(uvicorn)をインストール


1. reactのプロジェクト作成

※npm(またはnpx)が入ってなかったのでRemote containerを起動する必要あり

↓

docker内でpipが使えなかったのでコンテナ外でやることにした。その影響でyarnではなくnpmにする必要がある箇所もある

```bash
npx create-react-app daifugo-front
```

1. APIを使用するためのライブラリをReactにインストール(axios)

```bash
cd daifugo-front
yarn add axios
```

1. ローカル環境に仮想環境を作成(venv)
2. 仮想環境にfastapiとサーバー(uvicorn)をインストール

```bash
cd ..
mkdir daifugo-back
cd daifugo-back

python3 -m venv env  # docker内ではvenv使えないので気を付ける
. env/bin/activate

pip install fastapi uvicorn  # install
```

uvicorn main:app --reload  # ローカルサーバーを起動する

ローカルサーバーが起動しているか確認する

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)
にアクセス

![Untitled](https://s3-us-west-2.amazonaws.com/secure.notion-static.com/056e7c80-0068-4ce2-bc79-5a5423e20c1c/Untitled.png)

[http://127.0.0.1:8000/](http://127.0.0.1:8000/)docs

とするとAPIの設計情報が見れる

1. reactからapiを叩く処理を追加

```bash
# 参考資料を見てapp.jsxに処理をコピペする

yarn start  
```

[http://localhost:3000](http://localhost:3000/)

にアクセスするとfastapiとreactが連携されているのが確認できる


# -------------------------------------------------#
開発環境と本番環境では、
バックエンドとフロントエンドの通信用のurlを変える必要あり(直書き)