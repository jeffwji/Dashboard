from unittest.mock import Mock
import pytest
import os
from ui import views


# Async annotation for Pytest
@pytest.mark.asyncio
async def test_github_view():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Dashboard.settings")

    '''
    Mock upstream:
    
    Replace views.github and its function to Mockup object
    '''
    async def __get_commits(org, repo):
        print("\nUsing mocked __get_commits() function")

        import json
        with open("tests/test_data.json", 'r') as f:
            data = json.loads(f.read())
            return data
    views.github = Mock()
    views.github.get_commits = __get_commits

    '''
    Mock downstream
    '''
    request = Mock()
    request.method = "POST"
    request.body = """
    {
        "organization": "zio",
        "repository": "zio"
    }"""

    await views.contribute(request)
