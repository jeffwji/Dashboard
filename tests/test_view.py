from unittest.mock import Mock
import pytest
import os
import github


# Mock upstream
async def __get_commits(org, repo):
    import json
    with open("tests/test_data.json", 'r') as f:
        data = json.loads(f.read())
        return data
github.github = Mock()
github.github.get_commits = __get_commits


from ui.views import contribute


@pytest.mark.asyncio
async def test_github_view():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dashboard.settings")

    # Mock downstream
    request = Mock()
    request.method = "POST"
    request.body = """
    {
        "organization": "zio",
        "repository": "zio"
    }"""

    await contribute(request)
