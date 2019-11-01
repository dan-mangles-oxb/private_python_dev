from github import Github

# First create a Github instance:
personal_access_token = "0827d2864f9214a2ff4a0ca4de57aef11f32e06a"

# using username and password
# g = Github("user", "password")

# or using an access token
g = Github(personal_access_token)

# # Github Enterprise with custom hostname
# g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")

# # Then play with your Github objects:
# for repo in g.get_user().get_repos():
# #     print(repo.name)
# for repo in g.get_user().get_repos():
#     print(repo.name)


my_user_name = 'dan-mangles-oxb/'
repo_name = "api_test_repo"
repo_sel = g.get_repo(my_user_name+repo_name, lazy = False)

contents = repo_sel.get_contents("")
for content_file in contents:
     print(content_file)

pulls = repo_sel.get_pulls(state='open', sort='created', base='master')
for pr in pulls:
    print(pr.number)
    print(pr.commits)
    # print(pr.get_commits)
    cs = pr.get_commits()
    for c in cs:
        print(c.commit)
        print(c)
