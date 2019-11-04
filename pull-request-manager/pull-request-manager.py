from github import Github, GithubException
from datetime import datetime, timedelta
import random
import yaml

REPO_NAME = "george-webb-oxb/test-repo"

SMUG_ASCII_ART_LIST = ["( ͡ᵔ ͜ʖ ͡ᵔ )", "¯|_(◉‿◉)_|¯", "☜(⌒▽⌒)☞", "(◕‿◕✿)"]
ANGRY_ASCII_ART_LIST = ["(ノಠ益ಠ)ノ", "(╯°Д°)╯︵/(.□ . |)",
                        "(☞ಠ_ಠ)☞", "(,,#ﾟДﾟ)", "( ﾟДﾟ)＜!!", "(┛ಠ_ಠ)┛彡┻━┻"]


def is_stale(pr):
    '''returns true if a pull request is older than MAX_TIME_SINCE_CREATED'''
    time_since_pr_created = datetime.now() - pr.created_at
    if time_since_pr_created > timedelta(days=params["MAX_TIME_SINCE_CREATED"]):
        return True
    return False


def mark_as_stale(pr, STALE_LABEL):
    '''comments and labels stale PRs'''
    # check if already stale
    for label in pr.labels:
        if label.name == STALE_LABEL:
            print("Already marked as stale")
            return

    print('posting stale comment')
    comment_message = "Hey @{}! Your PR is more than {} days old :/ If there is no more activity for {} days, we'll close the PR \n\n{}".format(
        pr.user.login, params["MAX_TIME_SINCE_CREATED"], params["EXTRA_TIME_BEFORE_CLOSE"], random.choice(ANGRY_ASCII_ART_LIST))
    pr.create_issue_comment(comment_message)

    # label this PR as stale
    pr.add_to_labels(STALE_LABEL)
    return


def is_stale_enough_to_close(pr):
    '''check activity in last EXTRA_TIME_BEFORE_CLOSE days, return true if no activity'''

    print("This pr was last updated at {}".format(pr.updated_at))
    time_since_pr_updated = datetime.now() - pr.updated_at
    print('it has been {} since last update'.format(time_since_pr_updated))

    if time_since_pr_updated > timedelta(days=params["EXTRA_TIME_BEFORE_CLOSE"]):
        return True
    return False


def close_the_pr(pr, CLOSED_LABEL):
    '''comments then closes the pr'''

    print('closing the pr')
    comment_message = 'This PR is being automatically closed because it has been stale for {} days \n\n{}'.format(
        params["EXTRA_TIME_BEFORE_CLOSE"], random.choice(SMUG_ASCII_ART_LIST))
    pr.create_issue_comment(comment_message)

    pr.add_to_labels(CLOSED_LABEL)
    print('labelled as closed')
    pr.edit(state='closed')
    return


def main():
    # get an access token from file
    with open("access-token.txt", 'r') as access_token_file:
        personal_access_token = access_token_file.readline()

    # open the parameters file and copy into a global dict called params
    with open("pull-request-manager/parameters.yaml", 'r') as parameters_file:
        try:
            global params
            params = yaml.load(parameters_file)
            print("Parameter YAML file loaded.")
            print("params: MAX_TIME_SINCE_CREATED = {}, EXTRA_TIME_BEFORE_CLOSE = {}".format(
                params["MAX_TIME_SINCE_CREATED"], params["EXTRA_TIME_BEFORE_CLOSE"]))
        except yaml.YAMLError as exc:
            print(exc)

    # generate a label based on given max
    STALE_LABEL = "Older than {} days".format(params["MAX_TIME_SINCE_CREATED"])
    CLOSED_LABEL = "CLOSED AUTOMATICALLY"

    # instantiate a Github object
    gh = Github(personal_access_token)

    # make a repo object
    repo = gh.get_repo(REPO_NAME)

    # get an object with all pull requests
    pulls = repo.get_pulls(state='open', sort='created', base='master')

    print('This repo has {} open pull requests'.format(pulls.totalCount))
    # loop through the pull requests
    for pr in pulls:
        print('\n\nInvestigating PR: {}'.format(pr.title))
        if is_stale(pr):
            # method only executes if not already labelled as stale
            mark_as_stale(pr, STALE_LABEL)

            if is_stale_enough_to_close(pr):
                close_the_pr(pr, CLOSED_LABEL)
            else:
                print('not stale enough to close')
        else:
            print('not stale')

    print('\nAll open pull requests assessed. Exiting')


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Github API has returned an error, details below")
        print(e)  # where should this be logged
