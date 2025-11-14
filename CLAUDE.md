# Agent Handson プロジェクト開発・運営ガイド

このファイルは、`agent-handson`プロジェクトにおける**開発時の注意点とルール**、および**ハンズオン主催者向けの運営ガイド**を記載しています。

---

## 📚 目次

- [ハンズオン主催者向けガイド](#-ハンズオン主催者向けガイド)
  - [事前準備](#事前準備)
  - [ハンズオン当日の進行](#ハンズオン当日の進行)
  - [参加者サポートのヒント](#参加者サポートのヒント)
  - [よくあるトラブルと対処法](#よくあるトラブルと対処法)
- [開発者向けガイド](#-開発者向けガイド)
  - [開発記録の管理](#-開発記録の管理)
  - [Python環境管理](#-python環境管理)
  - [開発ワークフロー](#-開発ワークフロー)

---

## 🎓 ハンズオン主催者向けガイド

### 事前準備

#### 1. Azureリソースの準備

**必要なAzureリソース**:
- Azure OpenAI Service
  - GPT-5 デプロイメント
  - GPT-5-mini デプロイメント
- Azure Speech Service
  - 音声認識（Speech-to-Text）
  - 音声合成（Text-to-Speech）

**推奨設定**:
- リージョン: Japan East または East US 2
- 価格レベル: Standard（Free F0はデモには不十分）
- デプロイメント名: `gpt-5`, `gpt-5-mini`（.env.exampleと統一）

詳細: [.azure/azure_settings.md](./.azure/azure_settings.md)

#### 2. API Keyの準備

**配布用API Keyの作成**:
```bash
# Azure OpenAI Service
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your_generated_api_key

# Azure Speech Service
AZURE_SPEECH_API_KEY=your_speech_api_key
AZURE_SPEECH_REGION=japaneast
```

**セキュリティ対策**:
- ✅ ハンズオン専用のAPI Keyを発行
- ✅ 使用期限を設定（ハンズオン終了後に無効化）
- ✅ レート制限を適切に設定
- ✅ コスト上限アラートを設定

#### 3. 参加者向け資料の準備

**必須資料**:
1. **API Key配布シート**: 各参加者に固有のAPI Keyを配布
2. **HANDSON_QUICKSTART.mdの印刷版**: セットアップ手順の紙資料
3. **トラブルシューティングチートシート**: よくある問題と解決策

**推奨資料**:
- Azureの魅力を伝えるスライド
- ユースケース紹介資料
- 継続学習の案内

#### 4. 動作確認

**ハンズオン開始前に必ず確認**:
```bash
# 1. git cloneとセットアップ
git clone https://github.com/chinchillaa/agent-handson.git
cd agent-handson
cp .env.example .env
# .envにAPI Keyを設定

# 2. 依存関係のインストール
uv sync

# 3. 01_multi-llm-reasoningの動作確認
cd 01_multi-llm-reasoning
uv run python main.py "テスト質問"

# 4. 02_azure-voice-chatbotの動作確認
cd ../02_azure-voice-chatbot
uv run python main.py
# マイクで「こんにちは」と話しかけて確認
```

---

### ハンズオン当日の進行

#### タイムスケジュール例（2時間）

**0:00-0:10 (10分): オープニング**
- Azureの紹介
- ハンズオンの目的と流れ
- API Key配布

**0:10-0:25 (15分): セットアップ**
- HANDSON_QUICKSTART.mdに従ってセットアップ
- 参加者のサポート

**0:25-0:30 (5分): 01_multi-llm-reasoning デモ**
- 主催者によるデモ実演
- 4エージェントの協調動作を説明

**0:30-0:50 (20分): 01_multi-llm-reasoning ハンズオン**
- 参加者が各自で実行
- 様々な質問を試してもらう

**0:50-0:55 (5分): 02_azure-voice-chatbot デモ**
- 主催者によるデモ実演
- 音声認識・合成の高精度さを強調

**0:55-1:20 (25分): 02_azure-voice-chatbot ハンズオン**
- 参加者が音声対話を体験
- Phase 3機能（音声コマンド）も試してもらう

**1:20-1:40 (20分): Azureの魅力とビジネス活用**
- 実用例の紹介（コールセンター、アシスタント）
- コスト試算とROI
- 他のAzure AIサービスの紹介

**1:40-2:00 (20分): Q&A・まとめ**
- 質疑応答
- 継続学習の案内
- アンケート回収

---

### 参加者サポートのヒント

#### よくある質問と回答

**Q1: 「Python/uvがインストールされていません」**
```bash
# Pythonの確認
python --version  # 3.11以上が必要

# uvのインストール（Linux/Mac）
curl -LsSf https://astral.sh/uv/install.sh | sh

# uvのインストール（Windows）
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Q2: 「環境変数エラーが出ます」**
- `.env`ファイルの場所を確認（プロジェクトルートに配置）
- API Keyのコピペミスを確認（スペースや改行に注意）
- `.env.example`と`.env`を間違えていないか確認

**Q3: 「マイクが認識されません」**
- マイク接続を確認
- OSのマイク権限を確認
- 他のアプリ（Zoom等）がマイクを使用していないか確認

**Q4: 「音声認識の精度が低いです」**
- 静かな環境で試してもらう
- マイクを口に近づける（15-30cm）
- USB接続のマイクを推奨

**Q5: 「処理が遅いです」**
- ネットワーク接続を確認
- Azure APIのレート制限を確認
- 同時実行数を調整

#### サポート体制

**推奨体制**:
- メイン講師: 1名（進行担当）
- サポートスタッフ: 参加者10名あたり1名
- 技術担当: 1名（トラブル対応専任）

**サポート時の注意**:
- ✅ エラーメッセージを必ず確認
- ✅ `.env`ファイルの内容は画面共有させない（機密情報）
- ✅ 同じエラーが複数人に出たら全体共有
- ✅ 解決できない場合は代替デモを用意

---

### よくあるトラブルと対処法

#### トラブル1: uv syncが失敗する

**症状**:
```
error: Failed to download distributions
```

**対処法**:
```bash
# キャッシュをクリア
uv cache clean

# 再試行
uv sync

# それでも失敗する場合
uv sync --no-cache
```

#### トラブル2: Azure認証エラー

**症状**:
```
Error: AZURE_OPENAI_ENDPOINT is not set
```

**対処法**:
1. `.env`ファイルがプロジェクトルートにあるか確認
2. `.env`ファイルの内容を確認（KEY=VALUE形式）
3. API Keyが正しいか確認
4. エンドポイントURLが正しいか確認

#### トラブル3: 音声が出力されない

**症状**:
- 音声認識は動くが、応答音声が聞こえない

**対処法**:
1. スピーカー/ヘッドフォンの接続確認
2. システムの音量設定確認
3. 他のアプリケーションが音声デバイスを使用していないか確認
4. `examples/test_speech.py`で基本動作確認

#### トラブル4: APIレート制限

**症状**:
```
Error: Rate limit exceeded
```

**対処法**:
- 短時間に多くのリクエストが発生している
- 参加者に一斉実行を避けてもらう
- Azure Portalでレート制限を確認・調整

---

## 💻 開発者向けガイド

### 📝 開発記録の管理

#### PROJECT_HISTORY.mdへの記録

- **重要**: すべての開発作業は `PROJECT_HISTORY.md` に記録すること
- 記録すべき内容：
  - 新機能の追加
  - バグ修正
  - 依存パッケージの追加・更新
  - 設定ファイルの変更
  - リファクタリング
  - その他重要な変更

#### 記録フォーマット

```markdown
## YYYY-MM-DD

### 実装内容
- [機能名/修正内容]

### 変更ファイル
- `path/to/file.py`

### 備考
- 特記事項があれば記載
```

---

### 🐍 Python環境管理

#### 仮想環境

- プロジェクトルートに `.venv` ディレクトリが存在します
- 作業前に必ず仮想環境を有効化すること：

```bash
source .venv/bin/activate
```

#### パッケージ管理

**❌ 絶対に使用禁止**

- `pip install`
- `pip uninstall`
- その他の直接的なpipコマンド

**✅ 必ず使用**

- **新規パッケージの追加**: `uv add <package>`
  - pyproject.tomlとロックファイルに自動記録
- **依存関係の同期**: `uv sync`
  - pyproject.toml・uv.lockに基づいて環境を再現
- **パッケージ一覧**: `uv pip list`
  - 現在の環境にインストール済みパッケージ一覧を表示

**⚠️ 通常は不要（参考情報）**

- 一時的なパッケージインストール: `uv pip install <package>`
  - プロジェクト管理外のインストール（pip互換）。推奨されない
- 依存関係の出力: `uv pip freeze`
  - requirements.txt形式で出力。uv lockが依存関係の真のソースなので通常不要

#### 依存関係の管理

- 新しいパッケージを追加した場合：
  1. `uv add <package-name>` を使用
  2. `pyproject.toml` と `uv.lock` が自動更新されることを確認
  3. `PROJECT_HISTORY.md` に追加したパッケージを記録

- 別の環境で依存関係を再現する場合：
  - `uv sync` を実行（pyproject.toml・uv.lockから環境を構築）

---

### 📂 プロジェクト構造

```
agent-handson/
├── 01_multi-llm-reasoning/    # マルチLLM推論プロジェクト
├── 02_azure-voice-chatbot/     # Azure音声チャットボット
├── .venv/                      # Python仮想環境
├── pyproject.toml              # プロジェクト設定・依存関係
├── uv.lock                     # 依存関係ロックファイル
├── PROJECT_HISTORY.md          # 開発履歴（必ず更新）
├── HANDSON_QUICKSTART.md       # ハンズオン参加者向けガイド
├── CLAUDE.md                   # このファイル（開発・主催者向け）
└── README.md                   # プロジェクト概要
```

---

### 🔧 開発ワークフロー

1. **作業開始前**
   - 仮想環境の有効化を確認
   - 最新のコードをpull（チーム開発の場合）

2. **開発中**
   - 適切なディレクトリで作業
   - コードにコメントを記載（日本語）
   - テストを適宜実行

3. **作業完了後**
   - `PROJECT_HISTORY.md` に変更内容を記録
   - Gitコミット（意味のあるメッセージを記載）
   - こまめにプッシュ

---

### 🚨 開発時の注意事項

#### 環境変数

- `.env.example` を参考に `.env` ファイルを作成
- `.env` ファイルには機密情報を含むため、**絶対にコミットしない**
- 新しい環境変数を追加した場合は `.env.example` も更新

#### コーディング規約

- Python: PEP 8に準拠
- コメント: 日本語で記載
- 変数名・関数名: 英語（わかりやすい命名を心がける）

#### Git運用

- コミットメッセージは日本語でOK
- 意味のある単位でコミット
- 大きな変更の前にブランチを切ることを推奨
- **こまめにコミット・プッシュ**

---

## 📚 参考資料

### ハンズオン参加者向け
- プロジェクト概要: `README.md`
- クイックスタート: `HANDSON_QUICKSTART.md`
- プロジェクト詳細:
  - `01_multi-llm-reasoning/README.md`
  - `02_azure-voice-chatbot/README.md`

### 開発者・主催者向け
- 開発履歴: `PROJECT_HISTORY.md`
- Azure設定ガイド: `.azure/azure_settings.md`
- 設計ドキュメント:
  - `01_multi-llm-reasoning/DESIGN.md`
  - `02_azure-voice-chatbot/DESIGN.md`

---

## 🎯 ハンズオン成功のコツ

### 参加者のモチベーション維持

1. **すぐに動くことを体験させる**: 5分セットアップの重要性
2. **Azureの強みを実感させる**: 高精度な音声認識、GPT-5の推論能力
3. **ビジネス活用例を示す**: 身近なユースケースで関心を引く
4. **継続学習の道筋を示す**: ハンズオン後の学習リソース提供

### トラブル最小化

1. **事前の動作確認**: 必ず本番環境で動作確認
2. **バックアップ計画**: デモ動画、スクリーンショット等を用意
3. **サポート体制**: 十分なサポートスタッフ配置
4. **時間配分**: 余裕を持ったスケジュール

### Azureの購買意欲向上

1. **ROIを示す**: コスト試算、効率化の具体例
2. **競合との比較**: Azureの優位性を説明
3. **無料枠の活用**: まず小さく始められることを強調
4. **成功事例**: 実際の導入事例を紹介

---

**最終更新**: 2025-11-14
**対象者**: 開発者・ハンズオン主催者
