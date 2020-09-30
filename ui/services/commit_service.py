import datetime


def generate_commit_table(commits):
    table = {}
    earliest_date = None
    last_date = None
    most_commits = 1

    for author in (commit['author'] for commit in (item['commit'] for item in commits)):
        name = author['name']
        commit_date = datetime.datetime.strptime(author['date'], "%Y-%m-%dT%H:%M:%SZ").date()

        if earliest_date is None or earliest_date > commit_date:
            earliest_date = commit_date

        if last_date is None or last_date < commit_date:
            last_date = commit_date

        if name not in table.keys():
            table.update({name: {commit_date: 1}})
        else:
            committed = table.get(name)
            if commit_date not in committed:
                committed.update({commit_date: 1})
            else:
                commit_times = committed.get(commit_date) + 1
                if most_commits < commit_times:
                    most_commits = commit_times
                committed.update({commit_date: commit_times})
            table.update({name: committed})

    for name in table.keys():
        commits = table[name]
        if earliest_date not in commits:
            commits.update({earliest_date: 0})
        if last_date not in commits:
            commits.update({last_date: 0})

    return table, most_commits
