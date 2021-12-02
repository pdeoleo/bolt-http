import meraki, pprint, os, time

def org_networks(meraki: meraki.DashboardAPI, organizations: list):
    for org in organizations:
        networks = meraki.organizations.getOrganizationNetworks(org['id'], total_pages='all', perPage=3)
        pass

if __name__ == '__main__':
    meraki_legacy = meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY'), use_iterator_for_get_pages=False)

    org_networks(meraki_legacy, meraki_legacy.organizations.getOrganizations())

    meraki_iter = meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY'), use_iterator_for_get_pages=True)

    org_networks(meraki_iter, meraki_legacy.organizations.getOrganizations())
    
    # meraki_iter = meraki.DashboardAPI(os.environ.get('MERAKI_DASHBOARD_API_KEY'), use_iterator_for_get_pages=True)

    # org_networks_iter(meraki_iter)


