import requests

access_token = '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'


def get_latest_version():
    api_url = 'https://api.github.com/repos/gabrielhz/DiscordSQL/releases'
    headers = {'Authorization': f'token {access_token}'}
    response = requests.get(api_url, headers=headers)


# Check if the request was successful
    if response.status_code == 200:
        # Extract the pre-release title from the response JSON
        releases = response.json()
        pre_releases = [r for r in releases if r['prerelease']]
        latest_pre_release = pre_releases[0]['name']

    # Print the pre-release title
        return latest_pre_release
    else:
        # Print an error message if the request failed
        print(f'Error fetching latest release: {response.status_code}')
