import asyncio, meraki.aio, os, pprint

MERAKI_DASHBOARD_API_KEY = os.environ.get('MERAKI_DASHBOARD_API_KEY')    

def user_select_organization(orgs_list):
    for i, org in enumerate(orgs_list):
        print(f'{i+1} - {org["name"]}')
    org_index = int(input("Input desired organization no.:"))
    return orgs_list[org_index-1]

async def main():
    async with meraki.aio.AsyncDashboardAPI(MERAKI_DASHBOARD_API_KEY) as aiomeraki:
        my_orgs = await aiomeraki.organizations.getOrganizations()
        
        org_query = input('Input org name: ').lower()
        
        search_res = [org for org in my_orgs if org_query in org['name'].lower()]
        org = user_select_organization(search_res)
        print(f"==={org['name']} Networks===")
        org_networks = await aiomeraki.organizations.getOrganizationNetworks(org['id'])
        for i, network in enumerate(org_networks):
            print(f"{i}. {network['name']}")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
