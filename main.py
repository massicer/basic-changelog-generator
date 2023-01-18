from typing import List
import json
import os
from git import Repo
from git.refs.tag import TagReference
from git.objects.commit import Commit


def run():
    print("Running..")

    # rorepo is a Repo instance pointing to the git-python repository.
    # For all you know, the first argument to Repo is a path to the repository
    # you want to work with
    repo = Repo()
    print(repo.git)
    tags = get_last_two_tags(repo)
    commits = get_commits_between(repo, tags[1], tags[0])
    commitMsgs = extract_commit_message_from(commits)

    configuration = get_config()
    print(f"Retrieved configuration: {configuration}")

    mappedCommits = map_commits(commitMsgs, configuration)
    output = format_output(mappedCommits)

    print("The changelog has been generated correctly: \n")
    print(output)
    export_changelog_output(output)


def get_last_two_tags(repo: Repo) -> List[TagReference]:
    tags = list(repo.tags)
    print(f"Extracted the following tags: {tags}")
    tags.reverse()
    return (tags[0], tags[1])


def get_commits_between(
    repo: Repo, start: TagReference, end: TagReference
) -> List[Commit]:
    print(f"Getting commits between {start.commit}..{end.commit}")
    commits = repo.iter_commits(f"{start.commit}...{end.commit}")
    return list(commits)


def extract_commit_message_from(commits: List[Commit]) -> List[str]:
    return [commit.message.splitlines()[0] for commit in commits]


def get_config() -> dict:
    f = open("config.json")
    return json.load(f)


def map_commits(commits: List[str], config: dict) -> dict:
    map = {}
    for i in config["categories"]:
        map[i["label"]] = list()

    map[config["uncategorized"]["label"]] = list()

    for c in commits:
        added = False
        for i in map:
            if c.startswith(i):
                map[i].append(c)
                added = True
        if added is False:
            print("Here")
            map[config["uncategorized"]["label"]].append(c)

    return map


def format_output(info: dict) -> str:
    base_changelog = "Changelog:"
    for i in info.items():
        if len(i[1]) > 0:
            base_changelog += f"\n{i[0]}:"
            for e in i[1]:
                base_changelog += f"\n- {e}"

    return base_changelog


def export_changelog_output(changelog: str):
    o = f"""changelog=
changelog<<EOF
{changelog}
EOF"""
    with open(os.getenv("GITHUB_OUTPUT"), "a") as f:
        print(f"{o}", file=f)


if __name__ == "__main__":
    run()
