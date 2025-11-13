# 🚀 ハンズオン参加者向けクイックスタート

**所要時間: 5分**

このガイドは、主催者から配布されたAPI Keyを使って、すぐにハンズオンを開始するための最短手順です。

---

## ✅ 事前確認

以下がインストール済みであることを確認してください：

- [ ] Python 3.11以上
- [ ] uvパッケージマネージャー（[インストール](https://github.com/astral-sh/uv)）
- [ ] 主催者から配布されたAPI Keyを受領済み

---

## 📝 セットアップ手順

### ステップ1: リポジトリをクローン（1分）

```bash
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson
```

### ステップ2: 環境ファイルを作成（30秒）

```bash
cp .env.example .env
```

### ステップ3: API Keyを設定（2分）

エディタで`.env`ファイルを開きます：

```bash
nano .env
# または
vim .env
# または
code .env  # VS Code
```

**配布された値を以下の形式で記入**:

```bash
# ========================================
# Azure OpenAI Service 設定
# ========================================
AZURE_OPENAI_ENDPOINT=配布されたエンドポイント
AZURE_OPENAI_API_KEY=配布されたOpenAI_API_Key
AZURE_OPENAI_DEPLOYMENT_GPT5=gpt-5
AZURE_OPENAI_DEPLOYMENT_GPT5_MINI=gpt-5-mini

# ========================================
# Azure Speech Service 設定
# ========================================
AZURE_SPEECH_API_KEY=配布されたSpeech_API_Key
AZURE_SPEECH_REGION=japaneast
AZURE_SPEECH_LANGUAGE=ja-JP
AZURE_SPEECH_VOICE_NAME=ja-JP-NanamiNeural
```

保存して閉じます（`Ctrl+X` → `Y` → `Enter` for nano）

### ステップ4: 依存パッケージをインストール（1分）

```bash
uv sync
```

完了まで待ちます...

### ステップ5: 動作確認（30秒）

**01_multi-llm-reasoningを試す**:

```bash
cd 01_multi-llm-reasoning
uv run python main.py "量子コンピューターとは何ですか？"
```

回答が表示されたら成功！

**02_azure-voice-chatbotを試す**:

```bash
cd ../02_azure-voice-chatbot
uv run python main.py
```

マイクに向かって「こんにちは」と話しかけてみてください。

---

## 🔐 セキュリティ注意事項

⚠️ **重要**: 配布されたAPI Keyは機密情報です！

- ❌ GitHub等にpushしない
- ❌ SNSで共有しない
- ❌ スクリーンショットに含めない
- ✅ ハンズオン終了後は`.env`ファイルを削除

---

## ❓ トラブルシューティング

### Q1: 環境変数エラーが出る

```
❌ エラー: AZURE_OPENAI_ENDPOINTが設定されていません
```

**解決方法**:
1. `.env`ファイルが`agent-handson/`ディレクトリ（プロジェクトルート）にあるか確認
2. API Keyが正しく記載されているか確認（スペースや改行に注意）

```bash
# 現在のディレクトリを確認
pwd
# 出力: /path/to/agent-handson

# .envファイルの存在確認
ls -la .env
```

### Q2: Python/uvが見つからない

```
❌ command not found: python
❌ command not found: uv
```

**解決方法**: 主催者または近くの参加者にサポートを依頼してください。

### Q3: マイクが認識されない

**解決方法**:
- マイクが接続されているか確認
- ブラウザ/OSのマイク権限を確認
- 他のアプリがマイクを使用していないか確認

### Q4: その他のエラー

主催者に質問してください。エラーメッセージをコピーしておくとスムーズです。

---

## 📚 次のステップ

### プロジェクト1: 01_multi-llm-reasoning

**マルチLLM推論システム**

4つのAIエージェントが協調して複雑な質問に答えます。

```bash
cd 01_multi-llm-reasoning
uv run python main.py "あなたの質問"
```

**サンプル**:
```bash
uv run python examples/simple_query.py
uv run python examples/complex_reasoning.py
```

### プロジェクト2: 02_azure-voice-chatbot

**音声対話AIチャットボット**

音声で対話できるAIアシスタント（Phase 3: 音声コマンド対応）

```bash
cd 02_azure-voice-chatbot
uv run python main.py
```

**音声コマンドを試してみよう**:
- 「要約して」 - 会話の要約を表示
- 「音声を変更して」 - 音声を切り替え（5種類）
- 「速く話して」 - 話速を速く
- 「ゆっくり話して」 - 話速を遅く
- 「音声をリセット」 - デフォルトに戻す

**Phase 3デモ**:
```bash
uv run python examples/advanced_chat.py
```

---

## 📖 詳細ドキュメント

もっと詳しく知りたい方は以下を参照：

- **Azure設定ガイド**: `.azure/azure_settings.md`
- **プロジェクト1詳細**: `01_multi-llm-reasoning/README.md`
- **プロジェクト2詳細**: `02_azure-voice-chatbot/README.md`
- **開発履歴**: `PROJECT_HISTORY.md`

---

## 🎓 ハンズオン終了後

### 継続学習したい方へ

ハンズオン終了後、自分のAzureアカウントで継続学習したい場合：

1. **Azureアカウントを作成**: https://azure.microsoft.com/free/
2. **Azure CLIをインストール**: `.azure/azure_settings.md`の「共通設定」参照
3. **自分のリソースを作成**: `.azure/azure_settings.md`の各プロジェクト設定を参照

### ハンズオン用API Keyについて

- ハンズオン終了後、配布されたAPI Keyは無効化されます
- `.env`ファイルは削除してOKです

---

**ハンズオンを楽しんでください！** 🎉

質問があれば主催者または近くの参加者に気軽に声をかけてください。

---

**作成日**: 2025-11-13
**対象**: ハンズオン参加者
**所要時間**: 5分
