from github import Github, GithubException
from datetime import datetime, timedelta
import logging
import random
import yaml

SMUG_ASCII_ART_LIST = ["( ͡ᵔ ͜ʖ ͡ᵔ )", "¯|_(◉‿◉)_|¯", "☜(⌒▽⌒)☞", "(◕‿◕✿)"]
ANGRY_ASCII_ART_LIST = [
    "(ノಠ益ಠ)ノ", "(╯°Д°)╯︵/(.□ . |)", "(☞ಠ_ಠ)☞", "(,,#ﾟДﾟ)", "( ﾟДﾟ)＜!!",
    "(┛ಠ_ಠ)┛彡┻━┻"
]


def is_stale(pr):
    '''Returns true if a pull request is older than MAX_TIME_SINCE_CREATED'''
    time_since_pr_created = datetime.now() - pr.created_at
    if time_since_pr_created > timedelta(
            days=params["MAX_TIME_SINCE_CREATED"]):
        return True
    return False


def mark_as_stale(pr, STALE_LABEL):
    '''Comments and labels stale PRs'''
    logging.info("PR Title: {}".format(pr.title))
    logging.info("Created on {}".format(pr.created_at))

    # check if already stale
    for label in pr.labels:
        if label.name == STALE_LABEL:
            marked_as_stale_datetime = pr.created_at + timedelta(
                days=params["MAX_TIME_SINCE_CREATED"])
            logging.info("Marked as stale {} days ago (on {})".format(
                (datetime.now() - marked_as_stale_datetime).days,
                marked_as_stale_datetime))
            print("Already marked as stale")
            return False

    comment_message = "Hey @{}! Your PR is more than {} days old :/ If there is no more activity for {} days, we'll close the PR \n\n{}".format(
        pr.user.login, params["MAX_TIME_SINCE_CREATED"],
        params["EXTRA_TIME_BEFORE_CLOSE"], random.choice(ANGRY_ASCII_ART_LIST))

    if params["MODE"] == "READ_ONLY":
        logging.info("To be marked as stale")
    else:
        pr.create_issue_comment(comment_message)
        logging.debug("Commented on stale message")

        # label this PR as stale
        pr.add_to_labels(STALE_LABEL)
        logging.debug("Added stale label to PR")
        logging.info("This PR has been marked as stale from {}".format(
            pr.created_at + timedelta(days=params["MAX_TIME_SINCE_CREATED"])))
    return True


def is_stale_enough_to_close(pr):
    '''check activity in last EXTRA_TIME_BEFORE_CLOSE days, return true if no activity'''
    time_since_pr_updated = datetime.now() - pr.updated_at
    logging.info("Inactive for {} days. Last activity at {}".format(
        time_since_pr_updated.days, pr.updated_at))

    if time_since_pr_updated > timedelta(
            days=params["EXTRA_TIME_BEFORE_CLOSE"]):
        return True
    return False


def close_the_pr(pr, CLOSED_LABEL):
    '''comments then closes the pr'''
    comment_message = 'This PR is being automatically closed because it has been stale for {} days \n\n{}'.format(
        params["EXTRA_TIME_BEFORE_CLOSE"], random.choice(SMUG_ASCII_ART_LIST))

    if params["MODE"] == "READ_ONLY":
        logging.info("PR to be closed")

    else:
        pr.create_issue_comment(comment_message)
        pr.add_to_labels(CLOSED_LABEL)
        logging.debug('Labelled as closed')

        if params["MODE"] == "COMMENTS_ONLY":
            logging.info("This PR has been marked to be closed")

        if params["MODE"] == "CLOSE_PR":
            pr.edit(state='closed')
            logging.info("This PR has been closed")

    return


def main():
    # Set up logging
    time_now = datetime.now()
    logging.basicConfig(filename='./logs/example ({}).log'.format(time_now),
                        format="%(message)s",
                        level=logging.INFO)
    logging.info("Ran on {}".format(time_now))

    # get an access token from file
    with open("access-token.txt", 'r') as access_token_file:
        personal_access_token = access_token_file.readline()

    # open the parameters file and copy into a global dict called params
    with open("pull-request-manager/parameters.yaml", 'r') as parameters_file:
        global params
        params = yaml.load(parameters_file, Loader=yaml.SafeLoader)
        logging.debug("Parameter YAML file loaded.")
        logging.info(
            "Config Parameters:\nMAX_TIME_SINCE_CREATED = {}\nEXTRA_TIME_BEFORE_CLOSE = {}\nMODE = {}\nREPO_NAMES = {}"
            .format(params["MAX_TIME_SINCE_CREATED"],
                    params["EXTRA_TIME_BEFORE_CLOSE"], params["MODE"],
                    params["REPO_NAMES"]))

    # generate a label based on given max
    STALE_LABEL = "Older than {} days".format(params["MAX_TIME_SINCE_CREATED"])
    CLOSED_LABEL = "CLOSED AUTOMATICALLY"

    logging.info("")

    # instantiate a Github object
    gh = Github(personal_access_token)

    for REPO_NAME in params["REPO_NAMES"]:
        repo = gh.get_repo(REPO_NAME)

        # get an object with all pull requests
        pulls = repo.get_pulls(state='open', sort='created', base='master')
        logging.info('{} has {} open pull requests'.format(
            repo.full_name, pulls.totalCount))
        logging.info("")

        # loop through the pull requests
        for pr in pulls:
            logging.debug('Investigating PR: {}'.format(pr.title))
            if is_stale(pr):
                if mark_as_stale(pr, STALE_LABEL) is False:

                    if is_stale_enough_to_close(pr):
                        close_the_pr(pr, CLOSED_LABEL)
                    else:
                        print('not stale enough to close')
            else:
                print('not stale')
            logging.info("")

    logging.info('\nAll open pull requests assessed. Exiting')


if __name__ == "__main__":
    try:
        main()
    except yaml.YAMLError as ye:
        logging.critical("YAML File Error: {}".format(ye))
        raise Exception(
            "YAML File Error, check logs for more information.")
    except GithubException as ge:
        logging.critical("GithubException: {}".format(ge))
        raise Exception(
            "Github API has returned an error, check logs for more information.")
    except Exception as e:
        logging.critical("Exception: {}".format(e))
        raise Exception(
            'Some exception thrown, check logs for more information.')
