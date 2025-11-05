# Azure Voice Chatbot

Azureの音声サービスとagent-frameworkを組み合わせた音声対話型チャットボットのハンズオン

## 概要

このハンズオンでは、Azureの音声系サーバーレスシステムとagent-frameworkを組み合わせて、
音声で対話できるインテリジェントなチャットボットを構築します。

## 学習内容

- Azure Speech Servicesの使い方
- 音声認識（Speech-to-Text）の実装
- 音声合成（Text-to-Speech）の実装
- agent-frameworkとの統合
- リアルタイム音声対話の実装

## 前提条件

- Python 3.11以上
- agent-framework 1.0.0b251104以上
- Azureサブスクリプション
- Azure Speech Servicesのリソース

## 必要なAzureリソース

- Azure Speech Services
- Azure Functions（オプション）
- Azure Storage（オプション）

## セットアップ

```bash
# 仮想環境の有効化
source .venv/bin/activate

# Azure SDKのインストール（必要に応じて）
# uv pip install azure-cognitiveservices-speech
```

## 実装予定の機能

1. 音声入力の認識と処理
2. agent-frameworkによる応答生成
3. 音声出力の合成と再生
4. リアルタイム対話フローの実装

---

**Azure AI Agent ハンズオンプロジェクト**
