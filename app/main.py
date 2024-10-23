import datetime
import json
import logging
import os
import time
import zoneinfo

import dateparser
import requests
from slack_bolt import Ack, App, logger
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
from slack_sdk.web.slack_response import SlackResponse

# デバッグレベルのログを有効化
logging.basicConfig(level=logging.DEBUG)

# ボットトークンを渡してアプリを初期化します
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))


# 'こんにちは' を含むメッセージをリッスンします
# 指定可能なリスナーのメソッド引数の一覧は以下のモジュールドキュメントを参考にしてください：
# https://tools.slack.dev/bolt-python/api-docs/slack_bolt/kwargs_injection/args.html
# @app.message("こんにちは")
# def message_hello(message, say):
#     # イベントがトリガーされたチャンネルへ say() でメッセージを送信します

#     blocks = [
#         {
#             "type": "section",
#             "text": {
#                 "type": "mrkdwn",
#                 "text": f"こんにちは、<@{message['user']}> さん！",
#             },
#         },
#         {"type": "divider"},
#         {
#             "type": "actions",
#             "elements": [
#                 {
#                     "type": "button",
#                     "text": {
#                         "type": "plain_text",
#                         "text": f"クリックしてください",
#                     },
#                     "value": "click_me_123",
#                     "action_id": "button_click",
#                 }
#             ],
#         },
#     ]

#     say(blocks=blocks)

#     print(message)


@app.command("/command")
def handle_command_test(ack: Ack, body: dict, client: WebClient, logger: logger, say):

    ack()
    logger.info(body)
    pass


@app.command("/yaruki")
def handle_command_yaruki(ack: Ack, body: dict, client: WebClient, logger: logger, say):

    ack()
    logger.info(body)

    text = body["text"]

    channel_id = body["channel_id"]
    history = client.conversations_history(channel=channel_id, limit=20)
    messages = history["messages"]

    messages = sorted(messages, key=lambda x: x["ts"], reverse=False)

    for m in messages:
        if "blocks" in m:
            del m["blocks"]

    dt_now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo"))
    now = dt_now.strftime("%Y年%m月%d日 %H:%M:%S")

    response = requests.post(
        DIFY_API_APP_URL,
        headers={"Authorization": f"Bearer {DIFY_API_APP4_TOKEN}"},
        json={
            "inputs": {
                "chat_history": json.dumps(messages, ensure_ascii=False),
                "today": now,
                "prompt": text,
            },
            "response_mode": "blocking",
            "user": DIFY_API_TOKEN_USER,
        },
    )

    response_json = response.json()
    output = response_json["data"]["outputs"]["text"]

    client.chat_postEphemeral(
        channel=body["channel_id"],
        user=body["user_id"],
        text=output,
    )


@app.command("/yaruki_reminder")
def handle_command_yaruki_reminder(
    ack: Ack, body: dict, client: WebClient, logger: logger, say
):
    ack()
    logger.info(body)

    text = body["text"]

    channel_id = body["channel_id"]
    history = client.conversations_history(channel=channel_id, limit=20)
    messages = history["messages"]

    messages = sorted(messages, key=lambda x: x["ts"], reverse=False)

    for m in messages:
        if "blocks" in m:
            del m["blocks"]

    dt_now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo"))
    now = dt_now.strftime("%Y年%m月%d日 %H:%M:%S")

    client.chat_scheduleMessage(
        channel=body["user_id"],
        text="議事録の修正終わった？🍔",
        post_at=int(time.time()) + 30,
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
DIFY_API_APP2_TOKEN = os.environ.get("DIFY_API_APP2_TOKEN")
DIFY_API_TOKEN_USER = os.environ.get("DIFY_API_TOKEN_USER")
DIFY_API_APP_URL = os.environ.get("DIFY_API_APP_URL")

### ショートカットアプリ２
APP2_SHORTCUT_ID = "task_manager_001"
DIFY_API_APP3_TOKEN = os.environ.get("DIFY_API_APP3_TOKEN")
APP2_CALLBACK_ID = "APP2_CALLBACK_ID"
APP2_MODAL1_BLOCK1_ID = "APP2_MODAL1_BLOCK1_ID"
APP2_MODAL1_BLOCK1_ACTIONID = "APP2_MODAL1_BLOCK1_ACTIONID"
APP2_MODAL1_BLOCK2_ID = "APP2_MODAL1_BLOCK2_ID"
APP2_MODAL1_BLOCK2_ACTIONID = "APP2_MODAL1_BLOCK2_ACTIONID"
APP2_MODAL1_BLOCK3_ID = "APP2_MODAL1_BLOCK3_ID"
APP2_MODAL1_BLOCK3_ACTIONID = "APP2_MODAL1_BLOCK3_ACTIONID"
APP2_MODAL1_BLOCK4_ID = "APP2_MODAL1_BLOCK4_ID"
APP2_MODAL1_BLOCK4_ACTIONID = "APP2_MODAL1_BLOCK4_ACTIONID"

### コマンドアプリ
DIFY_API_APP4_TOKEN = os.environ.get("DIFY_API_APP4_TOKEN")


## ショートカットアプリ２
APP3_SHORTCUT_ID = "test_shortcut3"
APP3_CALLBACK_ID = "APP_3_CALLBACK_ID"


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
        "label": {"type": "plain_text", "text": "送りたい内容"},
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
                    "text": f"やわらかくする",
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
            "label": {"type": "plain_text", "text": "やわらか"},
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
                "initial_user": "U07RNU50QKW",
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
        "title": {"type": "plain_text", "text": "やわらかコミュニケーター"},
        "submit": {"type": "plain_text", "text": "送信"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "blocks": blocks,
    }


# チャンネル名 : channel_id
channel_list = {"user1-bot": "C07S4DSDMBQ"}


def app2_create_view(callback_id: str, task_list: list = None):

    blocks = []

    block_1 = {
        "type": "actions",
        "block_id": APP2_MODAL1_BLOCK1_ID,
        "elements": [
            {
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": f"タスク取得",
                },
                "value": "click_me_123",
                "action_id": APP2_MODAL1_BLOCK1_ACTIONID,
            }
        ],
    }

    blocks.append(block_1)

    if task_list:

        task_str = [
            f"{task['term']} {task['description']} {task['status']}"
            for task in task_list
        ]
        task_str = "\n".join(task_str)

        block_2 = {
            "type": "input",
            "block_id": APP2_MODAL1_BLOCK2_ID,
            "element": {
                "type": "plain_text_input",
                "action_id": APP2_MODAL1_BLOCK2_ACTIONID,
                "multiline": True,
                "initial_value": task_str,
            },
            "label": {"type": "plain_text", "text": "タスク"},
        }

        blocks.append(block_2)

        block_3 = {
            "type": "input",
            "block_id": APP2_MODAL1_BLOCK3_ID,
            "element": {
                "type": "plain_text_input",
                "action_id": APP2_MODAL1_BLOCK3_ACTIONID,
                "multiline": True,
            },
            "label": {"type": "plain_text", "text": "変更ある？？"},
        }

        blocks.append(block_3)

        block_4 = {
            "type": "actions",
            "block_id": APP2_MODAL1_BLOCK4_ID,
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": f"お願い！",
                    },
                    "value": "click_me_123",
                    "action_id": APP2_MODAL1_BLOCK4_ACTIONID,
                }
            ],
        }

        blocks.append(block_4)

    return {
        "type": "modal",
        "callback_id": callback_id,
        "title": {"type": "plain_text", "text": "モーダル"},
        "submit": {"type": "plain_text", "text": "送信"},
        "close": {"type": "plain_text", "text": "閉じる"},
        "blocks": blocks,
    }


@app.shortcut(APP2_SHORTCUT_ID)
def handle_shortcuts_app2(ack: Ack, body: dict, client: WebClient, logger: logger):

    logger.info(body)
    ack()

    # views.open という API を呼び出すことでモーダルを開きます
    client.views_open(
        trigger_id=body["trigger_id"],
        view=app2_create_view(APP2_CALLBACK_ID),
    )


@app.action(APP2_MODAL1_BLOCK1_ACTIONID)
def handle_action_app2_modal1_block1(
    ack: Ack, body: dict, client: WebClient, logger: logger
):
    ack()
    logger.info(body)

    channel_id = channel_list["user1-bot"]
    history = client.conversations_history(channel=channel_id, limit=100)
    messages = history["messages"]

    messages = sorted(messages, key=lambda x: x["ts"], reverse=False)

    for m in messages:
        if "blocks" in m:
            del m["blocks"]

    # logger.info(json.dumps(messages, indent=2, ensure_ascii=False))

    dt_now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo"))
    now = dt_now.strftime("%Y年%m月%d日 %H:%M:%S")

    response = requests.post(
        DIFY_API_APP_URL,
        headers={"Authorization": f"Bearer {DIFY_API_APP3_TOKEN}"},
        json={
            "inputs": {
                "chat_history": json.dumps(messages, ensure_ascii=False),
                "date": now,
            },
            "response_mode": "blocking",
            "user": DIFY_API_TOKEN_USER,
        },
    )

    response_json = response.json()
    task_list = response_json["data"]["outputs"]["task_list"]

    logger.info(json.dumps(task_list, indent=2, ensure_ascii=False))

    client.views_update(
        view_id=body.get("view").get("id"),
        hash=body.get("view").get("hash"),
        view=app2_create_view(
            callback_id=APP2_CALLBACK_ID,
            task_list=task_list,
        ),
    )

    pass


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
        DIFY_API_APP_URL,
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
def handle_view_app1_callback(
    ack: Ack, body: dict, logger: logging.Logger, client: WebClient
):

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

    ## 画像生成
    response = requests.post(
        DIFY_API_APP_URL,
        headers={"Authorization": f"Bearer {DIFY_API_APP2_TOKEN}"},
        json={"user": DIFY_API_TOKEN_USER, "inputs": {}},
    )

    response_json = response.json()
    prompt = response_json["data"]["outputs"]["prompt"]
    image_url = response_json["data"]["outputs"]["url"]

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
                    "image_url": f"{image_url}",
                    "alt_text": f"{prompt}",
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

        # response = requests.post(
        #     url,
        #     json={"blocks": blocks},
        # )

        # logger.debug(response.text)

        client.chat_postMessage(channel=selected_user, blocks=blocks)


@app.event("message")
def handle_message_events(
    ack: Ack, body: dict, logger: logging.Logger, client: WebClient
):
    logger.info(body)
    ack()

    event = body["event"]
    user = event["user"]
    ts = event["ts"]
    thread_ts = event.get("thread_ts", None)
    text = event["text"]

    logger.info(body)

    channel_id = event["channel"]
    history = client.conversations_history(channel=channel_id, limit=10)
    messages = history["messages"]

    messages = sorted(messages, key=lambda x: x["ts"], reverse=False)

    for m in messages:
        if "blocks" in m:
            del m["blocks"]

    dt_now = datetime.datetime.now(zoneinfo.ZoneInfo("Asia/Tokyo"))
    now = dt_now.strftime("%Y年%m月%d日 %H:%M:%S")

    response = requests.post(
        DIFY_API_APP_URL,
        headers={"Authorization": f"Bearer {DIFY_API_APP4_TOKEN}"},
        json={
            "inputs": {
                "chat_history": json.dumps(messages, ensure_ascii=False),
                "today": now,
                "prompt": text,
            },
            "response_mode": "blocking",
            "user": DIFY_API_TOKEN_USER,
        },
    )

    response_json = response.json()
    output = response_json["data"]["outputs"]["text"]

    client.chat_postMessage(
        channel=channel_id,
        thread_ts=thread_ts,
        user=user,
        text=output,
    )


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
