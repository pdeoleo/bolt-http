import asyncio, meraki.aio, os, pprint

MERAKI_DASHBOARD_API_KEY = os.environ.get('MERAKI_DASHBOARD_API_KEY')    

def user_select_option(options_list, msg='Input option no.:'):
    for i, org in enumerate(options_list):
        print(f'{i+1} - {org["name"]}')
    org_index = int(input(msg))
    return options_list[org_index-1]

async def main():
    async with meraki.aio.AsyncDashboardAPI(MERAKI_DASHBOARD_API_KEY, use_iterator_for_get_pages=True) as aiomeraki:
        my_orgs = await aiomeraki.organizations.getOrganizations()
        
        org_query = input('Input org name: ').lower()
        
        search_res = [org for org in my_orgs if org_query in org['name'].lower()]
        org = user_select_option(search_res)
        org_networks = aiomeraki.organizations.getOrganizationNetworks(organizationId=org['id'], total_pages='all', perPage=3)
        async for network in org_networks[0]:
            print(network)
        
        # pprint.pprint(org_networks)
        # user_select_option(org_networks)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
