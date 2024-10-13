import json
import logging
import os

import requests
from slack_bolt import Ack, App, logger
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)

# ボットトークンを渡してアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# 'こんにちは' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
@app.message("こんにちは")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します

    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"こんにちは、<@{message['user']}> さん！",
            },
        },
        {"type": "divider"},
        {
            "type": "actions",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": f"クリックしてください",
                    },
                    "value": "click_me_123",
                    "action_id": "button_click",
                }
            ],
        },
    ]

    say(blocks=blocks)

    print(message)


@app.command("/command")
def handle_command_test(ack: Ack, body: dict, client: WebClient):

    ack()

    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            # このモーダルに自分で付けられる ID で、次に説明する @app.view リスナーはこの文字列を指定します
            "callback_id": "modal-id",
            # これは省略できないため、必ず適切なテキストを指定してください
            "title": {"type": "plain_text", "text": "テストモーダル"},
            "submit": {"type": "plain_text", "text": "送信"},
            "close": {"type": "plain_text", "text": "閉じる"},
            "blocks": [
                {
                    "type": "input",
                    # block_id / action_id を指定しない場合 Slack がランダムに指定します
                    # この例のように明に指定することで、@app.view リスナー側での入力内容の取得で
                    # ブロックの順序に依存しないようにすることをおすすめします
                    "block_id": "question-block",
                    # ブロックエレメントの一覧は https://api.slack.com/reference/block-kit/block-elements
                    # Works with block types で Input がないものは input ブロックに含めることはできません
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input-element",
                    },
                    # これはモーダル上での見た目を調整するものです
                    # 同様に placeholder を指定することも可能です
                    "label": {"type": "plain_text", "text": "質問"},
                }
            ],
        },
    )


### ショートカットアプリ１
APP1_SHORTCUT_ID = "test_shortcut1"
APP1_CALLBACK_ID = "APP_1_CALLBACK_ID"
APP1_MODAL1_BLOCK1_ID = "APP1_MODAL1_BLOCK1_ID"
APP1_MODAL1_BLOCK1_ACTIONID = "APP1_MODAL1_BLOCK1_ID"
APP1_MODAL1_BLOCK2_ID = "APP1_MODAL1_BLOCK2_ID"
APP1_MODAL1_BLOCK2_ACTIONID = "APP1_MODAL1_BLOCK2_ACTIONID"
APP1_MODAL1_BLOCK3_ID = "APP1_MODAL1_BLOCK3_ID"
APP1_MODAL1_BLOCK3_ACTIONID = "APP1_MODAL1_BLOCK3_ACTIONID"
APP1_MODAL1_BLOCK4_ID = "APP1_MODAL1_BLOCK4_ID"
APP1_MODAL1_BLOCK4_ACTIONID = "APP1_MODAL1_BLOCK4_ACTIONID"
APP1_MODAL1_BLOCK5_ID = "APP1_MODAL1_BLOCK5_ID"
APP1_MODAL1_BLOCK5_ACTIONID = "APP1_MODAL1_BLOCK5_ACTIONID"

DIFY_API_APP1_TOKEN = os.environ.get("DIFY_API_APP1_TOKEN")
DIFY_API_TOKEN_USER = os.environ.get("DIFY_API_TOKEN_USER")
DIFY_API_APP1_URL = os.environ.get("DIFY_API_APP1_URL")


def app1_create_view(
    callback_id: str,
    message: str = None,
    created_message: str = None,
    references: dict = None,
):

    block_1 = {
        "type": "input",
        "block_id": APP1_MODAL1_BLOCK1_ID,
        "element": {
            "type": "plain_text_input",
            "action_id": APP1_MODAL1_BLOCK1_ACTIONID,
            "multiline": True,
        },
        "label": {"type": "plain_text", "text": "変換前"},
    }
    if message:
        block_1["element"]["initial_value"] = message

    block_2 = {
        "type": "actions",
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": f"変換",
                },
                "value": "click_me_123",
                "action_id": APP1_MODAL1_BLOCK2_ACTIONID,
            }
        ],
    }

    blocks = [block_1, block_2]

    if created_message:
        block_3 = {
            "type": "input",
            "block_id": APP1_MODAL1_BLOCK3_ID,
            "element": {
                "type": "plain_text_input",
                "action_id": APP1_MODAL1_BLOCK3_ACTIONID,
                "multiline": True,
                "initial_value": created_message,
            },
            "label": {"type": "plain_text", "text": "変換後"},
        }

        blocks.append(block_3)

        block_4 = {
            "type": "section",
            "block_id": APP1_MODAL1_BLOCK4_ID,
            "text": {"type": "mrkdwn", "text": "送信先を選択"},
            "accessory": {
                "type": "users_select",
                "action_id": APP1_MODAL1_BLOCK4_ACTIONID,
                "placeholder": {
                    "type": "plain_text",
                    "text": "Select a user",
                    "emoji": True,
                },
            },
        }

        blocks.append(block_4)

        if references:
            block_5 = {
                "type": "section",
                "block_id": APP1_MODAL1_BLOCK5_ID,
                "text": {"type": "mrkdwn", "text": "関連ドキュメントを選択（任意）"},
                "accessory": {
                    "type": "checkboxes",
                    "action_id": APP1_MODAL1_BLOCK5_ACTIONID,
                    "options": [
                        {
                            "text": {
                                "type": "mrkdwn",
                                "text": f"{ref['document_name']}",
                            },
                            "description": {
                                "type": "mrkdwn",
                                "text": f"{ref['content']}",
                            },
                            "value": f"{ref['segment_id']}",
                        }
                        for ref in references
                    ],
                },
            }
            blocks.append(block_5)

    return {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "モーダル"},
        "submit": {"type": "plain_text", "text": "送信"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "blocks": blocks,
    }


@app.shortcut(APP1_SHORTCUT_ID)
def handle_shortcuts_app1(ack: Ack, body: dict, client: WebClient):

    ack()

    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        trigger_id=body["trigger_id"],
        view=app1_create_view(APP1_CALLBACK_ID),
    )


@app.action(APP1_MODAL1_BLOCK2_ACTIONID)
def handle_action_app1_modal1_block2(
    ack: Ack, body: dict, client: WebClient, logger: logger
):

    logger.info(body)

    ack()

    view = body["view"]
    inputs = view["state"]["values"]
    message = (
        inputs.get(APP1_MODAL1_BLOCK1_ID, {})
        .get(APP1_MODAL1_BLOCK1_ACTIONID, {})
        .get("value")
    )

    response = requests.post(
        DIFY_API_APP1_URL,
        headers={"Authorization": f"Bearer {DIFY_API_APP1_TOKEN}"},
        json={
            "inputs": {
                "input": message,
                "role": "上司",
            },
            "response_mode": "blocking",
            "user": DIFY_API_TOKEN_USER,
        },
    )

    response_json = response.json()
    created_message = response_json["data"]["outputs"]["result"]
    knowledge = response_json["data"]["outputs"]["knowledge"]

    references = list(
        map(
            lambda x: {
                "document_name": x["metadata"]["document_name"],
                "segment_id": x["metadata"]["segment_id"],
                "content": x["content"],
            },
            knowledge,
        )
    )

    client.views_update(
        view_id=body.get("view").get("id"),
        hash=body.get("view").get("hash"),
        view=app1_create_view(
            APP1_CALLBACK_ID,
            message=message,
            created_message=created_message,
            references=references,
        ),
    )


@app.view(APP1_CALLBACK_ID)
def handle_view_app1_callback(ack: Ack, body: dict, logger: logging.Logger):

    ack()

    logger.info(body)

    user = body["user"]
    view = body["view"]
    inputs = view["state"]["values"]

    message = (
        inputs.get(APP1_MODAL1_BLOCK1_ID, {})
        .get(APP1_MODAL1_BLOCK1_ACTIONID, {})
        .get("value")
    )

    created_message = (
        inputs.get(APP1_MODAL1_BLOCK3_ID, {})
        .get(APP1_MODAL1_BLOCK3_ACTIONID, {})
        .get("value")
    )

    selected_user = (
        inputs.get(APP1_MODAL1_BLOCK4_ID, {})
        .get(APP1_MODAL1_BLOCK4_ACTIONID, {})
        .get("selected_user")
    )

    selected_references_options = (
        inputs.get(APP1_MODAL1_BLOCK5_ID, {})
        .get(APP1_MODAL1_BLOCK5_ACTIONID, {})
        .get("selected_options")
    )

    logger.debug(created_message)
    logger.debug(selected_user)

    url = os.environ.get(f"WEBHOOK_URL_{selected_user}", None)

    if url:

        blocks = [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"<@{selected_user}> さんへ <@{user['id']}> さんからメッセージが届いています。",
                },
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{created_message}",
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://pbs.twimg.com/profile_images/625633822235693056/lNGUneLX_400x400.jpg",
                    "alt_text": "cute cat",
                },
            },
            {"type": "divider"},
            {"type": "section", "text": {"type": "mrkdwn", "text": "関連ドキュメント"}},
            {
                "type": "rich_text",
                "elements": [
                    {
                        "type": "rich_text_list",
                        "style": "bullet",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": f"{ref['text']['text']}:\n",
                                    },
                                    {
                                        "type": "text",
                                        "text": f"{ref['description']['text']}:\n",
                                    },
                                ],
                            }
                            for ref in selected_references_options
                        ],
                    }
                ],
            },
        ]

        logger.debug(json.dumps(blocks, indent=2, ensure_ascii=False))

        response = requests.post(
            url,
            json={"blocks": blocks},
        )

        logger.debug(response.text)


@app.action(APP1_MODAL1_BLOCK4_ACTIONID)
def handle_action_app1_model1_block4(ack, body, logger):
    ack()
    logger.info(body)


@app.action(APP1_MODAL1_BLOCK5_ACTIONID)
def handle_action_app1_model1_block5(ack, body, logger):
    ack()
    logger.info(body)


if __name__ == "__main__":
    # アプリを起動して、ソケットモードで Slack に接続します
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
