import os, pprint
from os import path
import requests
import meraki
import json
import sys
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

if sys.version_info[0] == 3 and sys.version_info[1] < 10 or sys.version_info[0] < 3:
    raise Exception('Requires python 3.10 or higher.')

# SOCKET MODE SETUP

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN")
)

# HTTP SETUP
# app = App(
#     token=os.environ.get("SLACK_BOT_TOKEN"),
#     signing_secret=os.environ.get("SLACK_SIGNIN_SECRET")
# )


def chunks(lst, n):
    chunked_lst = []
    for i in range(0, len(lst), n):
        chunked_lst.append(lst[i:i + n])
    return chunked_lst


@app.command("/organizations")
def cmd_organizations(ack, say, command, client):
    ack()
    
    msg = say("...")
    
    split_command = command['text'].split()

    print(split_command)

    match len(split_command):
        case 1:
            perPage = int(split_command[0])
            page = 1
        case 2:
            perPage = int(split_command[0])
            page = int(split_command[1])
        case _:
            perPage = 3
            page = 1

    client.chat_update(
        ts=msg['ts'], 
        channel=msg['channel'],
        text="Connecting to Meraki Dashboard API...")
    
    try:
        dashboard = meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY'), log_path='./log_meraki')
        organizations = dashboard.organizations.getOrganizations()
    except:
        client.chat_update(
            ts=msg['ts'], 
            channel=msg['channel'],
            text="Connection failed")
        return None

    # with meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY'), log_path='./log_meraki') as dashboard:
    #     organizations = dashboard.organizations.getOrganizations()

    organization_chunks = chunks(organizations, perPage)

    block_header = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Hello,  *{command['user_name']}*.\n\n *These are your managed organizations:*"
            }
        },
        {
            "type": "divider"
        }
    ]

    block_body_organizations = []

    for org in organization_chunks[page]:
        block_body_organizations.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"*{org['name']}*\nAPI enabled: {':white_check_mark:' if org['api']['enabled'] else ':x:'}\n URL: <{org['url']}>"
                },
                "accessory": {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Details",
                        "emoji": True
                    },
                    "value": f"get_org_{org['id']}",
                    "action_id": f"get_org_{org['id']}"
			    }
            }
        )

    block_footer = [
        {
            "type": "divider"
        },
        {
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"Showing *{perPage}* out of *{len(organizations)}* | Page *{page}* of *{len(organization_chunks)}*",
                }
            ]
        }
    ]

    # Only add navigation buttons if more than one page
    if len(organization_chunks) > 1:
        block_nav_buttons = {
            "type": "actions",
            "elements": []
        }
        
        # 'First' btn only if not in first page
        if page != 1:
            block_nav_buttons['elements'].append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "First :black_left_pointing_double_triangle_with_vertical_bar:",
                        "emoji": True
                    },
                    "value": "first"
                }
            )   

        # 'Prev' btn only if beyond second page
        if page > 2:
            block_nav_buttons['elements'].append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Previous :arrow_backward:",
                        "emoji": True
                    },
                    "value": "prev"
                }
            )
        
        # 'Next' only if before penultimate page
        if page < len(organization_chunks) - 1:
            block_nav_buttons['elements'].append(
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "Next :arrow_forward:",
                        "emoji": True
                    },
                    "value": "next"
                }
            )

        # 'Last' only if not in last page
        if page != len(organization_chunks):
            block_nav_buttons['elements'].append({
                "type": "button",
                "text": {
                    "type": "plain_text",
                    "text": "Last :black_right_pointing_double_triangle_with_vertical_bar:",
                    "emoji": True
                },
                "value": "last"
            })


        block_pages_buttons = [
        {
            "type": "button",
            "text": {
                "type": "plain_text",
                "text": str(n),
                "emoji": True
            },
            "value": f"page_{n}"
        } for n in range(1, len(organization_chunks)+1) if n != page]
        
        block_nav_buttons['elements'].extend(block_pages_buttons)
        block_footer.append(block_nav_buttons)

    say(
        blocks=block_header + block_body_organizations + block_footer,
        text=f"{len(organizations)} organizations have been found."
    )



@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        logger.info("Updating home tab")
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app's app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "callback_id": "home_view",

                # body of the view
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to your _App's Home_* :tada:"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "This button won't do much for now but you can set up a listener for it using the `actions()` method and passing its unique `action_id`. See an example in the `examples` folder within your Bolt app."
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Click me!"
                                }
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.message("hello")
def message_hello(message, say):
    say(f"Hey there <@{message['user']}>!")


if __name__ == "__main__":
    if not path.exists('./log_meraki'):
        os.makedirs('./log_meraki')
    # SOCKET MODE
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
    

    # HTTP MODE
    # app.start(port=int(os.environ.get("PORT", 3000)))
