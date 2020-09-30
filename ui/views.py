from .plot import plot
from django.shortcuts import render
from .services import commit_service
from github import github


async def hello_world(request):
    # Load template from templates folder, which defined in `Dashboard/settings.py` within `TEMPLATES` list.
    data = await github.get_commits('zio', 'zio')
    commits, most_commits = commit_service.generate_commit_table(data)
    figure = await plot.plot_commits(commits, most_commits)

    return render(request, 'hello_world.html', {'figure': figure.getvalue()})
