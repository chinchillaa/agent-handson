# PROJECT_HISTORY.md

## 目的
- 本プロジェクトの作成・変更履歴を、意思決定の背景とともに追跡する。
- コミットログ（技術的事実）に加え、意図・合意・次アクション（文脈）を一元化する。

## 更新ルール
- 追記方式（新しいエントリを上に追加）。
- 日付は ISO 形式（YYYY-MM-DD）。
- 各エントリは「カテゴリ／概要／詳細／関連ファイル／コミット・PR／作成者／承認／メモ／次アクション」を含める。
- 自動・半自動の変更でも、ユーザー承認の有無を明記する。

## 記録テンプレート
```
### YYYY-MM-DD カテゴリ: <カテゴリ>
- 概要: <1行サマリ>
- 詳細:
  - <箇条書きで決定事項・背景>
- 関連ファイル: <相対パス, ...>
- コミット/PR: <ハッシュ or URL / PR番号 等>
- 作成者: <人/AI>
- 承認: <y/n と承認者>
- メモ: <任意>
- 次アクション: <任意>
```

---

### 2025-11-06 カテゴリ: Docs/Documentation
- 概要: README.mdを実装完了内容に合わせて全面更新
- 詳細:
  - **ルートREADME.md**
    - クイックスタートガイドを追加（git clone → 実行まで5ステップ）
    - プロジェクト概要を詳細化（実装状況を✅/🚧で明示）
    - 01_multi-llm-reasoningの説明を拡充（17種類のツール、4エージェント詳細）
    - 環境要件を必須・推奨に分類
    - プロジェクト構造を詳細化（各ファイルの役割を明記）
    - 使用方法セクションを拡充（基本/詳細/サンプル）
  - **01_multi-llm-reasoning/README.md**（全面書き直し）
    - 目次を追加（全セクションへのリンク付き）
    - システムアーキテクチャの図解と説明（4エージェントのフロー）
    - 詳細なセットアップ手順（git cloneから実行までの全手順）
    - 環境変数の設定ガイド（Azure CLI認証とAPI Key認証の両方を説明）
    - 各エージェントの詳細説明（役割、使用モデル、搭載ツールのリスト）
    - カスタムツール17種類の完全リスト（Web検索4個、データ分析5個、整形8個）
    - トラブルシューティングセクション（認証エラー、環境変数エラーなど）
    - 使用方法の拡充（全コマンドラインオプションの説明）
    - 関連ドキュメントへのリンク
- 関連ファイル:
  - `README.md`
  - `01_multi-llm-reasoning/README.md`
- コミット/PR: `5658ac4` docs: README.mdを実装完了内容に合わせて全面更新
- 作成者: AI assistant (Claude Code)
- 承認: y（ユーザー）
- メモ:
  - git cloneから環境構築・実行までの手順を明確化
  - Azure環境が準備できればすぐに再現できる状態に
  - 各機能・ツールの詳細を網羅
  - ユーザー要望「git cloneして、README.mdの指示に従って環境設定すればすぐに再現できるようにしたい」に対応
- 次アクション: Githubにpush、Azure環境準備後に動作確認

---

### 2025-11-06 カテゴリ: Feature/Implementation
- 概要: Multi-LLM Reasoning システムの完全実装（Phase 1-4）
- 詳細:
  - **Phase 1: カスタムツール実装**
    - Web検索支援ツール（Researcher用）: extract_key_information, summarize_search_results, organize_information, validate_sources
    - データ分析ツール（Analyzer用）: calculate_statistics, compare_data, extract_numbers_from_text, analyze_trend, categorize_data
    - テキスト整形ツール（Summarizer用）: format_as_markdown, create_bullet_list, structure_as_json, create_summary_table, highlight_key_points, format_conclusion, clean_text, add_metadata
  - **Phase 2: エージェントへのツール統合**
    - Researcher Agent: HostedWebSearchTool + カスタムWeb検索ツール4個を統合
    - Analyzer Agent: HostedCodeInterpreterTool + カスタム分析ツール5個を統合
    - Summarizer Agent: カスタム整形ツール8個を統合
    - 各エージェントのINSTRUCTIONSにツール利用ガイドを追加
  - **Phase 3: マルチエージェントワークフロー実装**
    - MultiAgentWorkflowクラスで4エージェント（Coordinator→Researcher→Analyzer→Summarizer）を順次実行
    - 並列エージェント初期化による高速化
    - 各エージェント間でのコンテキスト共有機能
    - 実行履歴の記録とログ出力
  - **Phase 4: メインアプリケーションと実行例**
    - main.py: コマンドライン引数対応のエントリーポイント
      - インタラクティブモード対応
      - --verbose オプション（各エージェント詳細出力）
      - --save-output オプション（結果のMarkdownファイル保存）
    - .env.example: 詳細な環境変数設定ガイド（Azure CLI認証/API Key認証の説明を含む）
    - examples/simple_query.py: シンプルな質問の実行例
    - examples/complex_reasoning.py: 複雑な推論を要する質問の実行例
- 関連ファイル:
  - `01_multi-llm-reasoning/tools/web_tools.py`
  - `01_multi-llm-reasoning/tools/analysis_tools.py`
  - `01_multi-llm-reasoning/tools/formatting_tools.py`
  - `01_multi-llm-reasoning/tools/__init__.py`
  - `01_multi-llm-reasoning/agents/researcher.py`
  - `01_multi-llm-reasoning/agents/analyzer.py`
  - `01_multi-llm-reasoning/agents/summarizer.py`
  - `01_multi-llm-reasoning/workflow.py`
  - `01_multi-llm-reasoning/main.py`
  - `01_multi-llm-reasoning/examples/simple_query.py`
  - `01_multi-llm-reasoning/examples/complex_reasoning.py`
  - `01_multi-llm-reasoning/examples/__init__.py`
  - `.env.example`
- コミット/PR:
  - `d38a9a8` feat(Phase 1): カスタムツールを実装
  - `637acf0` feat(Phase 2): 各エージェントにツール機能を統合
  - `52749aa` feat(Phase 3): マルチエージェントワークフローを実装
  - `b639005` feat(Phase 4): メインアプリケーションと実行例を実装
  - Github push完了
- 作成者: AI assistant (Claude Code)
- 承認: y（ユーザー）
- メモ:
  - agent-frameworkの組み込みツール（HostedWebSearchTool, HostedCodeInterpreterTool）を活用
  - 各Phase完了ごとにこまめにコミット・push（ユーザー要望に対応）
  - DESIGN.mdの実装計画に沿って段階的に開発
- 次アクション: 動作確認とテスト実施

---

### 2025-11-06 カテゴリ: Docs/Improvement
- 概要: CLAUDE.md のパッケージ管理セクションを改善（uv add を優先に）
- 詳細:
  - `uv add` を新規パッケージ追加の標準コマンドとして明記
  - `uv pip install` は一時的な用途のみと位置づけ
  - `uv sync` での依存関係同期を追加
  - `uv pip freeze` は通常不要と説明（uv.lock が真のソース）
  - 別環境での依存関係再現手順を追加
- 関連ファイル: `CLAUDE.md`
- コミット/PR: 未コミット
- 作成者: AI assistant (Claude Code)
- 承認: y（ユーザー）
- メモ: uvのベストプラクティスに沿った正確な記述に改善
- 次アクション: 変更をGitコミット

### 2025-11-06 カテゴリ: Bugfix/Encoding
- 概要: README.md および CLAUDE.md の文字化け修正（UTF-8エンコーディングで再作成）
- 詳細:
  - README.md と CLAUDE.md が文字化けしていることを確認（エンコーディング問題）
  - `.backup/` フォルダを作成し、文字化けファイルをバックアップ
  - `.gitignore` に `.backup/` を追加してgit追跡外に設定
  - README.md と CLAUDE.md を UTF-8 エンコーディングで再作成
  - CLAUDE.md にはプロジェクト固有の開発ルール（PROJECT_HISTORY.md への記録、uvの使用徹底など）を記載
- 関連ファイル: `README.md`, `CLAUDE.md`, `.gitignore`, `.backup/`
- コミット/PR: 未コミット
- 作成者: AI assistant (Claude Code)
- 承認: y（ユーザー）
- メモ: バックアップファイルは `.backup/README.md.20251106_131828`, `.backup/CLAUDE.md.20251106_131828` として保存
- 次アクション: 変更をGitコミット

### 2025-11-05 カテゴリ: Docs/Policy
- 概要: AI運用規範 `AGENTS.md` を追加し、`.gitignore` に除外設定を反映
- 詳細:
  - 提示された運用原則・環境方針・ワークフロー・出力体裁を `AGENTS.md` として追加。
  - リポジトリ追跡対象から外すため、`.gitignore` に `AGENTS.md` を追記。
  - `.gitignore` 変更を `master` にコミットし、`origin` に push。
- 関連ファイル: `AGENTS.md`, `.gitignore`
- コミット/PR: `5c8f075 chore: ignore AGENTS.md in git`（push 済）
- 作成者: AI assistant（Codex CLI）
- 承認: y（ユーザー）
- メモ: `AGENTS.md` は意図的に未追跡。必要時のみバージョン管理に含める方針。
- 次アクション: `README.md` から `AGENTS.md` への参照リンク追加（要確認）

