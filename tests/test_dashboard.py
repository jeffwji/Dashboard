import unittest
import asyncio
from ui.services import commit_service
from ui.plot import plot


"""
Switch to "/h/to/DevOpsDashboard/Dashboard"
"""
class GithubTestCases(unittest.TestCase):
    loop = None

    def setUp(self):
        self.loop = asyncio.get_event_loop()

    def tearDown(self):
        self.loop.close()

    """
    Test commit figure generation.
    """
    def test_commit_table(self):
        def assert_result(result):
            # print(result)
            self.assertTrue(result.find("<?xml") == 0)   # svg

        import json
        with open("tests/test_data.json", 'r') as f:
            data = json.loads(f.read())
            commits, most_commits = commit_service.generate_commit_table(data)

            f = self.loop.create_task(plot.plot_commits(commits, most_commits))
            f.add_done_callback(lambda result: assert_result(result.result().getvalue()))

            self.loop.run_until_complete(f)


