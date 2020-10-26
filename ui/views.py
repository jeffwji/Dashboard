from .plot import plot
from django.shortcuts import render
from .services import commit_service
from github import github
from django import forms
import json
from django.http import HttpResponse


class DevOpsForm(forms.Form):
    organization = forms.CharField(label='Organization', max_length=100)
    repository = forms.CharField(label='Repository', max_length=100)


async def index(request):
    return render(request, 'hello_world.html', {})


async def contribute(request):
    if request.method == 'POST':
        form = json.loads(request.body)
        # Load template from templates folder, which defined in `Dashboard/settings.py` within `TEMPLATES` list.
        data = await github.get_commits(form['organization'], form['repository'])
        commits, most_commits = commit_service.generate_commit_table(data)
        figure = await plot.plot_commits(commits, most_commits)

        #return render(request, 'hello_world.html', {'figure': figure.getvalue()})
        return HttpResponse(figure.getvalue(), content_type ="image/svg+xml")
    return HttpResponse("Nothing", content_type="text/text")