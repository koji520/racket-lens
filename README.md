# racket-lens

## コマンド

### 仮想環境 activate

```
source .venv/bin/activate
```

### パッケージのインストール

```
uv sync --frozen
```

### AIモデルのダウンロード

```
python scripts/download_model.py
```

### 開発サーバー起動

```
python app/manage.py runserver
```

### 本番用サーバー起動

```
gunicorn --chdir ./app --bind 0.0.0.0:8080 app.wsgi:application
```
