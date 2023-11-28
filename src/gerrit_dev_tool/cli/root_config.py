# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.bazel_client import BazelClient
from gerrit_dev_tool.gerrit_worktree import GerritWorktree
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace
from gerrit_dev_tool.plugin_repository import PluginRepository
from gerrit_dev_tool.recipes import Recipes
from gerrit_dev_tool.testsite_client import TestsiteClient
from gerrit_dev_tool.workspace_sync import WorkspaceSync


class RootConfig:
    def __init__(self, workspace: GrdtWorkspace, verbose=False):
        self.workspace = workspace
        self.gerrit_worktree = GerritWorktree(workspace.gerrit)
        self.bazel = BazelClient(workspace.gerrit)
        self.site = TestsiteClient(workspace)
        self.plugin_repo = PluginRepository(workspace)
        self.workspace_sync = WorkspaceSync(self.gerrit_worktree)
        self.recipes = Recipes(workspace)
        self.verbose = verbose


pass_root_config = click.make_pass_decorator(RootConfig)
