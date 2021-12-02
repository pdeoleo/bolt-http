import os, requests, meraki, json, sys
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
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@app.command("/organizations")
def cmd_organizations(ack, say, command):
    ack()

    # match x:
    #     case 1:
    #         pass
    #     case _:
    #         pass


    dashboard = meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY'))
    organizations = chunks(dashboard.organizations.getOrganizations(), 3)
    

    blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hello, Assistant to the Regional Manager Dwight! *Michael Scott* wants to know where you'd like to take the Paper Company investors to dinner tonight.\n\n *Please select a restaurant:*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Organization 2*\nAPI enabled: :white_check_mark:\n URL: <https://www.url.com>"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Organization 1*\nAPI enabled: :x:\n URL: <https://www.url.com>"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Showing 2 out of x",
					"emoji": True
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "First",
						"emoji": True
					},
					"value": "first"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Previous",
						"emoji": True
					},
					"value": "prev"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "1",
						"emoji": True
					},
					"value": "page_1"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "2",
						"emoji": True
					},
					"value": "page_2"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "3",
						"emoji": True
					},
					"value": "page_3"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Next",
						"emoji": True
					},
					"value": "next"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Last",
						"emoji": True
					},
					"value": "last"
				}
			]
		}
	]

    # for i, org in enumerate(user_orgs):
    #     user_orgs[i]['networks'] = dashboard.organizations.getOrganizationNetworks(org['id'])
    
    # for org in user_orgs:
    #     msg += f"{org['name']}\n"
    #     for network in org['networks']:
    #         msg += f"-{network['name']}\n"

    say(
        blocks=blocks,
        text="x organizations have been found."
    )
    

@app.message("organizations")
def message_organizations(message, say):
    # Load organizations for APP home page

    # dashboard = meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY'))
    # user_orgs = dashboard.organizations.getOrganizations(perPage=5)

    blocks = [
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "Hello, Assistant to the Regional Manager Dwight! *Michael Scott* wants to know where you'd like to take the Paper Company investors to dinner tonight.\n\n *Please select a restaurant:*"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Organization 2*\nAPI enabled: :white_check_mark:\n URL: <https://www.url.com>"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Organization 1*\nAPI enabled: :x:\n URL: <https://www.url.com>"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "plain_text",
					"text": "Showing 2 out of x",
					"emoji": True
				}
			]
		},
		{
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "First",
						"emoji": True
					},
					"value": "first"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Previous",
						"emoji": True
					},
					"value": "prev"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "1",
						"emoji": True
					},
					"value": "page_1"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "2",
						"emoji": True
					},
					"value": "page_2"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "3",
						"emoji": True
					},
					"value": "page_3"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Next",
						"emoji": True
					},
					"value": "next"
				},
				{
					"type": "button",
					"text": {
						"type": "plain_text",
						"text": "Last",
						"emoji": True
					},
					"value": "last"
				}
			]
		}
	]

    # for i, org in enumerate(user_orgs):
    #     user_orgs[i]['networks'] = dashboard.organizations.getOrganizationNetworks(org['id'])
    
    # for org in user_orgs:
    #     msg += f"{org['name']}\n"
    #     for network in org['networks']:
    #         msg += f"-{network['name']}\n"

    say(
        blocks=blocks
    )

    # with meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY')) as dashboard:
    #     # meraki_dashboard.
    #     pass


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
    
	# SOCKET MODE
	SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()

    # HTTP MODE
    # app.start(port=int(os.environ.get("PORT", 3000)))
