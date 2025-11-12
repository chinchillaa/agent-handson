# テストケース別 API 利用料金 概算

このテストスイートは外部APIを呼び出さない設計（mock/スタブ）であり、テスト実行時の実コストは0円です。

## サマリ

- ユニットテスト（tools, config, CLI）: 0円（外部呼び出しなし）
- 統合テスト（workflow）: 現状 skip。将来、Fake Agentでの検証→0円、ライブ実行→下記式で算出

## ライブ実行時の見積り方法（参考）

1回の問い合わせあたり、以下の4エージェントを順次呼び出す前提:

- Coordinator: GPT-5
- Researcher: GPT-5-mini
- Analyzer: GPT-5
- Summarizer: GPT-5

コスト計算式（1ケースあたり）:

```
総コスト(USD) = Σ [ (入力トークン数 / 1000) * 単価_in + (出力トークン数 / 1000) * 単価_out ]
```

モデルごとに単価が異なるため、実際の単価を適用してください（Azure OpenAIの価格ページを参照）。

### 仮定トークン例（シナリオの複雑さに応じて調整）

- Coordinator: in=600, out=400
- Researcher: in=800, out=600
- Analyzer: in=900, out=700
- Summarizer: in=700, out=600

> 注: これらは概算用の仮数値です。各テストシナリオでプロンプト/出力の長さをもとに見直してください。

### 単価の挿入例（ダミー値。実価格で置換）

- GPT-5: in=$X/1K tok, out=$Y/1K tok
- GPT-5-mini: in=$x/1K tok, out=$y/1K tok

### テンプレート（実コスト算出）

| ケース | モデル | 入力tok | 出力tok | in単価 | out単価 | 小計(USD) |
|---|---|---:|---:|---:|---:|---:|
| Coordinator | GPT-5 | 600 | 400 | X | Y | `600/1000*X + 400/1000*Y` |
| Researcher | GPT-5-mini | 800 | 600 | x | y | `800/1000*x + 600/1000*y` |
| Analyzer | GPT-5 | 900 | 700 | X | Y | `900/1000*X + 700/1000*Y` |
| Summarizer | GPT-5 | 700 | 600 | X | Y | `700/1000*X + 600/1000*Y` |
| 合計 |  |  |  |  |  | Σ小計 |

## 次のアクション

- 価格の自動取得: 開発環境でネットワークアクセスを許可いただければ、Azure OpenAI (GPT-5/GPT-5-mini) の in/out 単価を公式ページから取得し、本ファイルに反映します。

---

## 実単価とJPY換算（USD→JPY=150）

前提（USD/1K tokens に正規化）

- GPT-5 Global: 入力 X = $0.00125、出力 Y = $0.01000
- GPT-5-mini Global: 入力 x = $0.00025、出力 y = $0.00200
- 換算レート: 1 USD = 150 JPY
- ワークフローのモデル割当: Coordinator/Analyzer/Summarizer=GPT-5、Researcher=GPT-5-mini

ケース別（1問い合わせあたりの概算）

| ケース | USD (per query) | JPY (per query) |
|---|---:|---:|
| Case A（軽量） | $0.01245 | 約 1.87 円 |
| Case B（中～重度） | $0.02115 | 約 3.17 円 |
| Case C（重度/長文） | $0.03135 | 約 4.70 円 |

注記
- 上記は通常の入力/出力単価を用いた概算です（キャッシュ入力は未考慮）。
- リージョン/通貨: 米国東部 / USD。提示値は Global の価格に基づきます。
- Data Zone/Pro/Codex など別SKUを用いる場合は単価に合わせて再計算してください。
