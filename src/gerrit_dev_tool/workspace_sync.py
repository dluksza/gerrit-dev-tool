# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import subprocess
from functools import reduce
from typing import Iterator

from gerrit_dev_tool.gerrit_plugin import GerritPlugin
from gerrit_dev_tool.gerrit_worktree import GerritWorktree
from gerrit_dev_tool.plugins_bzl_parser import PluginsBzl, parse_plugins_bzl


class WorkspaceSync:
    def __init__(self, gerrit_worktree: GerritWorktree) -> None:
        self._gerrit_worktree = gerrit_worktree

    def external_deps(self) -> None:
        dependencies = reduce(
            lambda d1, d2: d1.merge(d2),
            map(lambda p: p.get_extenal_deps(), self._linked_plugins()),
        )
        with open(self._gerrit_worktree.plugins_depenedncy_file(), "w") as deps_file:
            deps_file.write(dependencies.to_bazel_file())

    def plugins_bzl(self) -> None:
        plugins = self._load_plugins_bzl()

        for plugin_name in list(plugins.custom):
            if not self._gerrit_worktree.has_plugin(plugin_name):
                plugins.custom.remove(plugin_name)
                plugins.custom_test.discard(plugin_name)

        for plugin_name in self._gerrit_worktree.linked_plugins():
            plugins.custom.add(plugin_name)

        if len(plugins.custom) > 0:
            with open(self._gerrit_worktree.plugins_bzl(), "w") as output:
                output.write(str(plugins))

    def eclipse_project(self) -> None:
        subprocess.run('./tools/eclipse/project.py', cwd=self._gerrit_worktree.worktree, check=True)

    def _linked_plugins(self) -> Iterator[GerritPlugin]:
        return map(self._gerrit_worktree.get_plugin, self._gerrit_worktree.linked_plugins())

    def _load_plugins_bzl(self) -> PluginsBzl:
        with open(self._gerrit_worktree.plugins_bzl()) as current:
            return parse_plugins_bzl(current.read())
