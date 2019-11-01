from github import Github

# get an access token from file
with open("pull-request-manager/access-token.txt",'r') as access_token_file:
    personal_access_token = access_token_file.readline()

# instantiate a Github object
gh = Github(personal_access_token)

# make a repo object
repo = gh.get_repo("george-webb-oxb/test-repo")

# print out all prs
pulls = repo.get_pulls(state='open', sort='created', base='master')
for pr in pulls:
    print(pr.number)
    print(pr.commits)
    # print(pr.get_commits)
    cs = pr.get_commits()
    for c in cs:
        # print(c.commit)
        print(c)