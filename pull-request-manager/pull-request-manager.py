from github import Github
from datetime import datetime, timedelta
import random

MAX_TIME_SINCE_CREATED = 1 # days
EXTRA_TIME_BEFORE_CLOSE = 7 # days

LIST_OF_COMMENTS = ["YOU SUCK","YOU REALLY SUCK","HEY! YOUR PR IS STALE!!!!!!!!!!!!!!!!!!","WINTER IS COMING"]

# for each pr in a repo, test it based on a criterion
def is_stale(pr):
    '''returns true if a pull request is stale'''
    time_since_pr_created = datetime.now() - pr.created_at
    if time_since_pr_created > timedelta(days = MAX_TIME_SINCE_CREATED):
        return True
    return False


def send_stale_message(pr):
    '''posts a comment on the PR explaining that this PR is stale'''
    print('sending stale message')
    # user_name = pr.user.login
    comment_message = "Hey @{}! Your PR is more than {} days old :/ If there is no more activity for {} days, we'll close the PR \n\n{}".format(pr.user.login, MAX_TIME_SINCE_CREATED, EXTRA_TIME_BEFORE_CLOSE,"-.-")
    # pr.create_issue_comment(random.choice(LIST_OF_COMMENTS))
    pr.create_issue_comment(comment_message)
    return

def main():
    # get an access token from file
    with open("pull-request-manager/access-token.txt",'r') as access_token_file:
        personal_access_token = access_token_file.readline()

    # instantiate a Github object
    gh = Github(personal_access_token)

    # repo_name = 
    # make a repo object
    repo = gh.get_repo("george-webb-oxb/test-repo")

    # print out all prs
    pulls = repo.get_pulls(state='open', sort='created', base='master')

    # print out some stuff from repo
    for pr in pulls:
        print(is_stale(pr))
        if is_stale(pr):
            send_stale_message(pr)


if __name__ == "__main__":
    main()