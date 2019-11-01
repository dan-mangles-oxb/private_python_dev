from github import Github
from datetime import datetime, timedelta
import random
import yaml

LIST_OF_ASCII_ART = ["-.-", ":3"]


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
        pr.user.login, params["MAX_TIME_SINCE_CREATED"], params["EXTRA_TIME_BEFORE_CLOSE"], random.choice(LIST_OF_ASCII_ART))
    pr.create_issue_comment(comment_message)

    # label this PR as stale
    pr.add_to_labels(STALE_LABEL)
    return


def is_stale_enough_to_close(pr):
    '''check activity in last EXTRA_TIME_BEFORE_CLOSE days, return true if no activity'''
    # # check the PR is already stale
    # if not is_stale(pr):
    #     return False

    print("This pr was last updated at ")
    print(pr.updated_at)

    time_since_pr_updated = datetime.now() - pr.updated_at
    print('it has been this much time since update')
    print(time_since_pr_updated)

    if time_since_pr_updated > timedelta(days=params["EXTRA_TIME_BEFORE_CLOSE"]):
        return True
    return False


def close_the_pr(pr):
    '''comments then closes the pr'''

    print('closing the pr')
    comment_message = 'This PR is being automatically closed because it has been stale for {} days'.format(
        params["EXTRA_TIME_BEFORE_CLOSE"])
    pr.create_issue_comment(comment_message)

    pr.edit(state='closed')
    return


def main():
    # get an access token from file
    with open("pull-request-manager/access-token.txt", 'r') as access_token_file:
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

    # instantiate a Github object
    gh = Github(personal_access_token)

    # make a repo object
    repo = gh.get_repo("george-webb-oxb/test-repo")

    # get an object with all pull requests
    pulls = repo.get_pulls(state='open', sort='created', base='master')

    # loop through the pull requests
    for pr in pulls:

        print('\n\nInvestigating PR: {}'.format(pr.title))
        if is_stale(pr):
            # method only executes if not already labelled as stale
            mark_as_stale(pr, STALE_LABEL)

            if is_stale_enough_to_close(pr):
                close_the_pr(pr)
            else:
                print('not stale enough to close')
        else:
            print('not stale')

    print('all pull requests assessed')


if __name__ == "__main__":
    main()
