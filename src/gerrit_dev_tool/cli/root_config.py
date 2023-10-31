# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.gerrit_worktree import GerritWorktree


class RootConfig:
    def __init__(self, verbose=False):
        self.gerrit_worktree = GerritWorktree(".")
        self.verbose = verbose


pass_root_config = click.make_pass_decorator(RootConfig)
