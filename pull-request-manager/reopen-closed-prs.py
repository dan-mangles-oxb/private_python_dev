from github import Github

def reopen_the_pr(pr, CLOSED_LABEL):
    print('reopening the pr')
    comment_message = 'This PR is being reopened'
    pr.create_issue_comment(comment_message)

    # remove closed label
    pr.remove_from_labels(CLOSED_LABEL)
            
    print('pr reopeneed')
    pr.edit(state='open')
    return

def reopen_all_prs(repo, CLOSED_LABEL):
    '''reopens all prs in this repo'''

    # get an object with all pull requests
    pulls = repo.get_pulls(state='closed', sort='created', base='master')

    print('This repo has {} closed pull requests'.format(pulls.totalCount))
    # loop through the pull requests
    for pr in pulls:
        reopen_the_pr(pr, CLOSED_LABEL)
    return

def main():
    # get an access token from file
    with open("pull-request-manager/access-token.txt", 'r') as access_token_file:
        personal_access_token = access_token_file.readline()

    # generate a label based on given max
    CLOSED_LABEL = "CLOSED AUTOMATICALLY"

    # instantiate a Github object
    gh = Github(personal_access_token)

    # make a repo object
    repo = gh.get_repo("george-webb-oxb/test-repo")

    reopen_all_prs(repo, CLOSED_LABEL)

if __name__ == "__main__":
    main()
