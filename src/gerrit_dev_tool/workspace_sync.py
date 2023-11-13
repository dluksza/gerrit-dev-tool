# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from functools import reduce
from typing import Iterator

from gerrit_dev_tool.gerrit_plugin import GerritPlugin
from gerrit_dev_tool.gerrit_worktree import GerritWorktree


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

    def _linked_plugins(self) -> Iterator[GerritPlugin]:
        return map(self._gerrit_worktree.get_plugin, self._gerrit_worktree.linked_plugins())
