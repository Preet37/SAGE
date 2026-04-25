# Source: https://docs.anthropic.com/ja/docs/agents-and-tools/tool-use/fine-grained-tool-streaming
# Title: Fine-grained tool streaming - Anthropic Docs
# Fetched via: jina
# Date: 2026-04-10

Title: きめ細かいツールストリーミング


# きめ細かいツールストリーミング - Claude API Docs

[](https://docs.anthropic.com/docs/ja/home)

Messages

*   [ビルド](https://docs.anthropic.com/docs/ja/intro)
*   [管理](https://docs.anthropic.com/docs/ja/build-with-claude/administration-api)
*   [モデルと料金](https://docs.anthropic.com/docs/ja/about-claude/models/overview)
*   [クライアントSDK](https://docs.anthropic.com/docs/ja/api/client-sdks)
*   [APIリファレンス](https://docs.anthropic.com/docs/ja/api/overview)

日本語[Log in](https://docs.anthropic.com/login?returnTo=%2Fdocs%2Fja%2Fagents-and-tools%2Ftool-use%2Ffine-grained-tool-streaming)

Search...

⌘K

はじめに

[Claudeの概要](https://docs.anthropic.com/docs/ja/intro)[クイックスタート](https://docs.anthropic.com/docs/ja/get-started)

Claudeで構築する

[機能概要](https://docs.anthropic.com/docs/ja/build-with-claude/overview)[Messages APIの使用](https://docs.anthropic.com/docs/ja/build-with-claude/working-with-messages)[停止理由の処理](https://docs.anthropic.com/docs/ja/build-with-claude/handling-stop-reasons)

モデルの機能

[拡張思考](https://docs.anthropic.com/docs/ja/build-with-claude/extended-thinking)[適応的思考](https://docs.anthropic.com/docs/ja/build-with-claude/adaptive-thinking)[エフォート](https://docs.anthropic.com/docs/ja/build-with-claude/effort)[高速モード（ベータ：リサーチプレビュー）](https://docs.anthropic.com/docs/ja/build-with-claude/fast-mode)[構造化出力](https://docs.anthropic.com/docs/ja/build-with-claude/structured-outputs)[引用](https://docs.anthropic.com/docs/ja/build-with-claude/citations)[ストリーミングメッセージ](https://docs.anthropic.com/docs/ja/build-with-claude/streaming)[バッチ処理](https://docs.anthropic.com/docs/ja/build-with-claude/batch-processing)[検索結果](https://docs.anthropic.com/docs/ja/build-with-claude/search-results)[ストリーミング拒否](https://docs.anthropic.com/docs/ja/test-and-evaluate/strengthen-guardrails/handle-streaming-refusals)[多言語サポート](https://docs.anthropic.com/docs/ja/build-with-claude/multilingual-support)[埋め込み](https://docs.anthropic.com/docs/ja/build-with-claude/embeddings)

ツール

[概要](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/overview)[ツール使用の仕組み](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/how-tool-use-works)[ウェブ検索ツール](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/web-search-tool)[ウェブフェッチツール](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/web-fetch-tool)[コード実行ツール](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/code-execution-tool)[メモリツール](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/memory-tool)[Bashツール](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/bash-tool)[コンピューター使用ツール](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/computer-use-tool)[テキストエディタツール](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/text-editor-tool)

ツールインフラ

[ツール検索](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/tool-search-tool)[プログラムによるツール呼び出し](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/programmatic-tool-calling)[細粒度ツールストリーミング](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/fine-grained-tool-streaming)

コンテキスト管理

[コンテキストウィンドウ](https://docs.anthropic.com/docs/ja/build-with-claude/context-windows)[コンパクション](https://docs.anthropic.com/docs/ja/build-with-claude/compaction)[コンテキスト編集](https://docs.anthropic.com/docs/ja/build-with-claude/context-editing)[プロンプトキャッシュ](https://docs.anthropic.com/docs/ja/build-with-claude/prompt-caching)[トークンカウント](https://docs.anthropic.com/docs/ja/build-with-claude/token-counting)

ファイルの操作

[Files API](https://docs.anthropic.com/docs/ja/build-with-claude/files)[PDFサポート](https://docs.anthropic.com/docs/ja/build-with-claude/pdf-support)[画像とビジョン](https://docs.anthropic.com/docs/ja/build-with-claude/vision)

スキル

[概要](https://docs.anthropic.com/docs/ja/agents-and-tools/agent-skills/overview)[クイックスタート](https://docs.anthropic.com/docs/ja/agents-and-tools/agent-skills/quickstart)[ベストプラクティス](https://docs.anthropic.com/docs/ja/agents-and-tools/agent-skills/best-practices)[エンタープライズ向けスキル](https://docs.anthropic.com/docs/ja/agents-and-tools/agent-skills/enterprise)[APIのスキル](https://docs.anthropic.com/docs/ja/build-with-claude/skills-guide)

MCP

[リモートMCPサーバー](https://docs.anthropic.com/docs/ja/agents-and-tools/remote-mcp-servers)[MCPコネクター](https://docs.anthropic.com/docs/ja/agents-and-tools/mcp-connector)

プロンプトエンジニアリング

[概要](https://docs.anthropic.com/docs/ja/build-with-claude/prompt-engineering/overview)[プロンプトのベストプラクティス](https://docs.anthropic.com/docs/ja/build-with-claude/prompt-engineering/claude-prompting-best-practices)[Consoleプロンプトツール](https://docs.anthropic.com/docs/ja/build-with-claude/prompt-engineering/prompting-tools)

テストと評価

[成功の定義と評価の構築](https://docs.anthropic.com/docs/ja/test-and-evaluate/develop-tests)[ConsoleでのEvaluation Toolの使用](https://docs.anthropic.com/docs/ja/test-and-evaluate/eval-tool)[レイテンシの削減](https://docs.anthropic.com/docs/ja/test-and-evaluate/strengthen-guardrails/reduce-latency)

ガードレールの強化

[幻覚の低減](https://docs.anthropic.com/docs/ja/test-and-evaluate/strengthen-guardrails/reduce-hallucinations)[出力の一貫性向上](https://docs.anthropic.com/docs/ja/test-and-evaluate/strengthen-guardrails/increase-consistency)[ジェイルブレイクの軽減](https://docs.anthropic.com/docs/ja/test-and-evaluate/strengthen-guardrails/mitigate-jailbreaks)[プロンプトリークの低減](https://docs.anthropic.com/docs/ja/test-and-evaluate/strengthen-guardrails/reduce-prompt-leak)

リソース

[用語集](https://docs.anthropic.com/docs/ja/about-claude/glossary)

ユースケース

Agent SDK

リリースノート

[Claude Platform](https://docs.anthropic.com/docs/ja/release-notes/overview)

[Console](https://docs.anthropic.com/)

[Log in](https://docs.anthropic.com/login)

ツールインフラ 細粒度ツールストリーミング

ツールインフラ

# きめ細かいツールストリーミング

Copy page

レイテンシに敏感なアプリケーションのために、ツール入力を1文字ずつストリーミングします。

Copy page

This feature is eligible for [Zero Data Retention (ZDR)](https://docs.anthropic.com/docs/en/build-with-claude/api-and-data-retention). When your organization has a ZDR arrangement, data sent through this feature is not stored after the API response is returned.

きめ細かいツールストリーミングは、すべてのモデルおよびすべてのプラットフォームで一般提供されています。バッファリングやJSON検証なしにツール使用パラメータ値の[ストリーミング](https://docs.anthropic.com/docs/ja/build-with-claude/streaming)を可能にし、大きなパラメータの受信開始までのレイテンシを削減します。

きめ細かいツールストリーミングを使用する場合、無効または不完全なJSON入力を受け取る可能性があります。コード内でこれらのエッジケースを考慮するようにしてください。

## きめ細かいツールストリーミングの使い方

きめ細かいツールストリーミングは、すべてのモデルおよびすべてのプラットフォーム（Claude API、Amazon Bedrock、Google Vertex AI、Microsoft Foundry）で利用可能です。使用するには、きめ細かいストリーミングを有効にしたいユーザー定義ツールで`eager_input_streaming`を`true`に設定し、リクエストでストリーミングを有効にします。

APIでのきめ細かいツールストリーミングの使用例を以下に示します：

Shell

```
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 65536,
    "tools": [
      {
        "name": "make_file",
        "description": "Write text to a file",
        "eager_input_streaming": true,
        "input_schema": {
          "type": "object",
          "properties": {
            "filename": {
              "type": "string",
              "description": "The filename to write text to"
            },
            "lines_of_text": {
              "type": "array",
              "description": "An array of lines of text to write to the file"
            }
          },
          "required": ["filename", "lines_of_text"]
        }
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "Can you write a long poem and make a file called poem.txt?"
      }
    ],
    "stream": true
  }'
```

この例では、きめ細かいツールストリーミングにより、Claudeは`lines_of_text`パラメータが有効なJSONかどうかを検証するためのバッファリングなしに、長い詩の行をツール呼び出し`make_file`にストリーミングできます。これにより、パラメータ全体がバッファリングされて検証されるのを待つことなく、到着するとすぐにパラメータのストリームを確認できます。

きめ細かいツールストリーミングでは、ツール使用チャンクのストリーミング開始が速くなり、チャンクが長くなり、単語の区切りが少なくなることが多いです。これはチャンキング動作の違いによるものです。

例：

きめ細かいストリーミングなし（15秒の遅延）：

```
Chunk 1: '{"'
Chunk 2: 'query": "Ty'
Chunk 3: 'peScri'
Chunk 4: 'pt 5.0 5.1 '
Chunk 5: '5.2 5'
Chunk 6: '.3'
Chunk 8: ' new f'
Chunk 9: 'eatur'
...
```

きめ細かいストリーミングあり（3秒の遅延）：

```
Chunk 1: '{"query": "TypeScript 5.0 5.1 5.2 5.3'
Chunk 2: ' new features comparison'
```

きめ細かいストリーミングはバッファリングやJSON検証なしにパラメータを送信するため、結果のストリームが有効なJSON文字列として完了する保証はありません。 特に、[停止理由](https://docs.anthropic.com/docs/ja/build-with-claude/handling-stop-reasons)の`max_tokens`に達した場合、ストリームはパラメータの途中で終了し、不完全になる可能性があります。一般的に、`max_tokens`に達した場合を処理するための特定のサポートを記述する必要があります。

## ツール入力デルタの蓄積

`tool_use`コンテンツブロックがストリーミングされると、最初の`content_block_start`イベントには`input: {}`（空のオブジェクト）が含まれます。これはプレースホルダーです。実際の入力は、それぞれ`partial_json`文字列フラグメントを持つ一連の`input_json_delta`イベントとして到着します。コードはこれらのフラグメントを連結し、ブロックが閉じたら結果を解析する必要があります。

蓄積の契約：

1.   `type: "tool_use"`の`content_block_start`で、空の文字列を初期化します：`input_json = ""`
2.   `type: "input_json_delta"`の各`content_block_delta`で、追加します：`input_json += event.delta.partial_json`
3.   `content_block_stop`で、蓄積された文字列を解析します：`json.loads(input_json)`

最初の`input: {}`（オブジェクト）と`partial_json`（文字列）の型の不一致は設計によるものです。空のオブジェクトはコンテンツ配列のスロットをマークし、デルタ文字列が実際の値を構築します。

Python

```
import json
import anthropic

client = anthropic.Anthropic()

tool_inputs = {}  # index -> accumulated JSON string

with client.messages.stream(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get current weather for a city",
            "eager_input_streaming": True,
            "input_schema": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"],
            },
        }
    ],
    messages=[{"role": "user", "content": "Weather in Paris?"}],
) as stream:
    for event in stream:
        if (
            event.type == "content_block_start"
            and event.content_block.type == "tool_use"
        ):
            tool_inputs[event.index] = ""
        elif (
            event.type == "content_block_delta"
            and event.delta.type == "input_json_delta"
        ):
            tool_inputs[event.index] += event.delta.partial_json
        elif event.type == "content_block_stop" and event.index in tool_inputs:
            parsed = json.loads(tool_inputs[event.index])
            print(f"Tool input: {parsed}")
```

PythonおよびTypeScript SDKは、この蓄積を自動的に行う高レベルのストリームヘルパー（`stream.get_final_message()`、`stream.finalMessage()`）を提供しています。上記の手動パターンは、ブロックが閉じる前に部分的な入力に反応する必要がある場合（進捗インジケーターのレンダリングや下流リクエストの早期開始など）にのみ使用してください。

## ツールレスポンスでの無効なJSONの処理

きめ細かいツールストリーミングを使用する場合、モデルから無効または不完全なJSONを受け取る可能性があります。この無効なJSONをエラーレスポンスブロックでモデルに返す必要がある場合、適切な処理を確保するためにJSONオブジェクトでラップすることができます（適切なキーを使用して）。例えば：

```
{
  "INVALID_JSON": "<your invalid json string>"
}
```

このアプローチにより、モデルはコンテンツが無効なJSONであることを理解しながら、デバッグ目的で元の不正なデータを保持できます。

無効なJSONをラップする場合、ラッパーオブジェクトで有効なJSON構造を維持するために、無効なJSON文字列内の引用符や特殊文字を適切にエスケープするようにしてください。

## 次のステップ

[ストリーミングメッセージ サーバー送信イベントとストリームイベントタイプの完全なリファレンス。](https://docs.anthropic.com/docs/ja/build-with-claude/streaming)[ツール呼び出しの処理 ツールを実行し、必要なメッセージ形式で結果を返します。](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/handle-tool-calls)[ツールリファレンス Anthropicスキーマツールとそのバージョン文字列の完全なディレクトリ。](https://docs.anthropic.com/docs/ja/agents-and-tools/tool-use/tool-reference)

Was this page helpful?

*   [ツールレスポンスでの無効なJSONの処理](https://docs.anthropic.com/ja/docs/agents-and-tools/tool-use/fine-grained-tool-streaming#json)

[](https://docs.anthropic.com/docs)

[](https://x.com/claudeai)[](https://www.linkedin.com/showcase/claude)[](https://instagram.com/claudeai)

### Solutions

*   [AI agents](https://claude.com/solutions/agents)
*   [Code modernization](https://claude.com/solutions/code-modernization)
*   [Coding](https://claude.com/solutions/coding)
*   [Customer support](https://claude.com/solutions/customer-support)
*   [Education](https://claude.com/solutions/education)
*   [Financial services](https://claude.com/solutions/financial-services)
*   [Government](https://claude.com/solutions/government)
*   [Life sciences](https://claude.com/solutions/life-sciences)

### Partners

*   [Amazon Bedrock](https://claude.com/partners/amazon-bedrock)
*   [Google Cloud's Vertex AI](https://claude.com/partners/google-cloud-vertex-ai)

### Learn

*   [Blog](https://claude.com/blog)
*   [Courses](https://www.anthropic.com/learn)
*   [Use cases](https://claude.com/resources/use-cases)
*   [Connectors](https://claude.com/partners/mcp)
*   [Customer stories](https://claude.com/customers)
*   [Engineering at Anthropic](https://www.anthropic.com/engineering)
*   [Events](https://www.anthropic.com/events)
*   [Powered by Claude](https://claude.com/partners/powered-by-claude)
*   [Service partners](https://claude.com/partners/services)
*   [Startups program](https://claude.com/programs/startups)

### Company

*   [Anthropic](https://www.anthropic.com/company)
*   [Careers](https://www.anthropic.com/careers)
*   [Economic Futures](https://www.anthropic.com/economic-futures)
*   [Research](https://www.anthropic.com/research)
*   [News](https://www.anthropic.com/news)
*   [Responsible Scaling Policy](https://www.anthropic.com/news/announcing-our-updated-responsible-scaling-policy)
*   [Security and compliance](https://trust.anthropic.com/)
*   [Transparency](https://www.anthropic.com/transparency)

### Learn

*   [Blog](https://claude.com/blog)
*   [Courses](https://www.anthropic.com/learn)
*   [Use cases](https://claude.com/resources/use-cases)
*   [Connectors](https://claude.com/partners/mcp)
*   [Customer stories](https://claude.com/customers)
*   [Engineering at Anthropic](https://www.anthropic.com/engineering)
*   [Events](https://www.anthropic.com/events)
*   [Powered by Claude](https://claude.com/partners/powered-by-claude)
*   [Service partners](https://claude.com/partners/services)
*   [Startups program](https://claude.com/programs/startups)

### Help and security

*   [Availability](https://www.anthropic.com/supported-countries)
*   [Status](https://status.claude.com/)
*   [Support](https://support.claude.com/)
*   [Discord](https://www.anthropic.com/discord)

### Terms and policies

*   [Responsible disclosure policy](https://www.anthropic.com/responsible-disclosure-policy)
*   [Terms of service: Commercial](https://www.anthropic.com/legal/commercial-terms)
*   [Terms of service: Consumer](https://www.anthropic.com/legal/consumer-terms)
*   [Usage policy](https://www.anthropic.com/legal/aup)