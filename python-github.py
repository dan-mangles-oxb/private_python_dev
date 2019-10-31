from github import Github

# First create a Github instance:
personal_access_token = "abde505ab2224c2dc55a34b67733e8bb0a136363"

# using username and password
# g = Github("user", "password")

# or using an access token
g = Github(personal_access_token)

# # Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# # Then play with your Github objects:
for repo in g.get_user().get_repos():
    print(repo.name)

    