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

