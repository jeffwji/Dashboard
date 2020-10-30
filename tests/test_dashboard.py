import unittest
from ui.services import commit_service
from ui.plot import plot
import json


"""
Switch to "/path/to/DevOpsDashboard/Dashboard"
"""
class GithubTestCases(unittest.IsolatedAsyncioTestCase):
    """
    Test commit figure generation.
    """
    async def test_commit_table(self):
        with open("tests/test_data.json", 'r') as f:
            data = json.loads(f.read())
            commits, most_commits = commit_service.generate_commit_table(data)

            svgIO = await plot.plot_commits(commits, most_commits)
            svg = svgIO.getvalue()
            self.assertTrue(svg.find("<?xml") == 0)


