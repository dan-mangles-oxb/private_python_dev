from github import Github

REPO_NAME = "george-webb-oxb/test-repo"


def reopen_the_pr(pr, CLOSED_LABEL):
    print('reopening the pr')
    comment_message = 'This PR is being reopened'
    pr.create_issue_comment(comment_message)

    # remove all
    pr.delete_labels()

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


def remove_all_labels(repo):
    '''removes all labels in open prs in this repo'''

    # get an object with all pull requests
    pulls = repo.get_pulls(state='open', sort='created', base='master')
    print('This repo has {} open pull requests'.format(pulls.totalCount))
    # loop through the pull requests
    for pr in pulls:
        pr.delete_labels()


def main():
    # get an access token from file
    with open("access-token.txt", 'r') as access_token_file:
        personal_access_token = access_token_file.readline()

    # generate a label based on given max
    CLOSED_LABEL = "CLOSED AUTOMATICALLY"

    # instantiate a Github object
    gh = Github(personal_access_token)

    # make a repo object
    repo = gh.get_repo(REPO_NAME)

    reopen_all_prs(repo, CLOSED_LABEL)
    remove_all_labels(repo)


if __name__ == "__main__":
    main()
