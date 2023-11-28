# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import re
import subprocess
from typing import Iterable

from gerrit_dev_tool.gerrit_plugin import GerritPlugin
from gerrit_dev_tool.git_client import GitClient
from gerrit_dev_tool.plugins_bzl_parser import parse_plugins_bzl

_version_prefix = re.compile(r"^origin/(stable-)?")


class GerritWorktree:
    def __init__(self, worktree):
        self.worktree = worktree
        self._plugin_dir = os.path.join(worktree, "plugins")
        self._dot_git = os.path.join(worktree, ".git")

    def has_plugin(self, plugin_name: str) -> bool:
        return os.path.islink(self._plugin_path(plugin_name))

    def link_plugin(self, plugin_path: str) -> None:
        (_, name) = os.path.split(plugin_path)
        os.symlink(plugin_path, self._plugin_path(name), target_is_directory=True)

    def is_builtin_plugin(self, plugin_name: str) -> bool:
        with open(self.plugins_bzl()) as plugins_bzl:
            plugins = parse_plugins_bzl(plugins_bzl.read())
            return plugin_name in plugins.core

    def get_plugin(self, plugin_name: str) -> GerritPlugin:
        return GerritPlugin(plugin_name, self._plugin_path(plugin_name))

    def linked_plugins(self) -> Iterable[str]:
        "List all plugins linked into plugins directory."
        for plugin in os.listdir(self._plugin_dir):
            path = os.path.join(self._plugin_dir, plugin)
            if os.path.islink(path) and os.path.isdir(path):
                yield plugin

    def unlink_plugin(self, plugin_name) -> None:
        "Removes plugin `plugin_name` from plugins directory."
        plugin_path = os.path.join(self._plugin_dir, plugin_name)
        os.unlink(plugin_path)

    def plugins_depenedncy_file(self) -> str:
        return os.path.join(self._plugin_dir, "external_plugin_deps.bzl")

    def plugins_bzl(self):
        return os.path.join(self.worktree, "tools", "bzl", "plugins.bzl")

    def clean_external_plugin_deps(self) -> None:
        subprocess.run(
            ["git", "--git-dir", self._dot_git, "restore", "plugins/external_plugin_deps.bzl"],  # noqa: S603 S607
            check=True,
        )

    def clean_tools_plugins(self) -> None:
        subprocess.run(
            ["git", "--git-dir", self._dot_git, "restore", "tools/bzl/plugins.bzl"],  # noqa: S603 S607
            check=True,
        )

    def version(self) -> str:
        return _version_prefix.sub("", GitClient.version(self.worktree))

    def set_version(self, version: str) -> None:
        GitClient.checkout(self.worktree, f"origin/{version}")

    def _plugin_path(self, plugin_name: str) -> str:
        return os.path.join(self._plugin_dir, plugin_name)
