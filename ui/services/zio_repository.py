from github import github
import asyncio
from . import commit_service


def get_zio_commits():
    loop = asyncio.get_event_loop()

    task = asyncio.ensure_future(github.get_commits("zio", "zio"))

    def process_commits(data):
        commit_service.generate_commit_table(data.result())

    task.add_done_callback(process_commits  )

    loop.run_until_complete(task)

    loop.close()
