import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
import numpy as np
import io


async def plot_commits(commits, most_commits):
    n = len(commits)
    num_rows, num_cols = int((n+2)/3), 3
    fig, axis = plt.subplots(num_rows, num_cols, figsize=(13, 20))
    ax = axis.flatten()

    for index, name in enumerate(commits.keys()):
        await __plot_commit(commits[name], name, ax[index], most_commits)
        plt.setp(ax[index].get_xticklabels(), rotation=30, horizontalalignment='right')

    return await __plot_to_svg(plt)


async def __plot_to_svg(plt):
    svg = io.StringIO()
    plt.savefig(svg, format="svg")
    return svg


async def __plot_commit(commit, label, ax, most_commits):
    x, y = zip(* sorted(commit.items()))
    ax.bar(x, y, label=label, color=np.random.rand(3, ))
    ax.set_ylim([0, most_commits])
    ax.legend()
