# 一括画像トリミングツール

このツールは、指定したフォルダ内の画像を自動で処理し、

- **透明部分のトリミング**
- **指定サイズへのリサイズ（比率維持）**
- **中央配置**

を行います。

## インストール
このスクリプトは Python で動作し、`Poetry` を使用して依存関係を管理します。

まず、`Poetry` をインストールしてください（未インストールの場合）。

```sh
brew install poetry
```

その後、以下のコマンドで必要なライブラリをインストールできます。

```sh
poetry install
```

## 使い方

### 基本的な使用方法
```sh
python trim.py <input_dir>
```

このコマンドを実行すると、

- `<input_dir>` 内の画像 (`.png`, `.jpg`, `.jpeg`) を処理
- `<input_dir>_trimmed` フォルダに出力

### 出力フォルダを指定する
```sh
python trim.py <input_dir> --output_folder <output_dir>
```
`<output_dir>` を指定すると、そのフォルダに出力されます。

### 画像サイズを指定する
```sh
python trim.py <input_dir> --size 幅 高さ
```
例:
```sh
python trim.py images --size 512 512
```

この場合、すべての画像は **512×512 ピクセル** に調整されます（アスペクト比は維持）。

### 詳細な処理ログを表示する
```sh
python trim.py <input_dir> --verbose
```
処理中の詳細情報が表示されます。

## コードフォーマット（Lint）
このプロジェクトでは `black` を使用してコードをフォーマットします。
`black` は `poetry install` 実行時に自動でインストールされます。

コードを整形するには、以下のコマンドを実行してください。

```sh
poetry run black .
```

## 注意点
- 透明部分のない画像（RGBA でない画像）はスキップされます。
- 透明部分のみの画像はスキップされます。
- `--size` を指定しない場合、元の画像サイズが維持されます。

## ライセンス
MIT License

