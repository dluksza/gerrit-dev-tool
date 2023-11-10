# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess


class GerritWorktree:
    def __init__(self, worktree):
        self._worktree = worktree
        self._plugin_dir = os.path.join(worktree, "plugins")
        self._dot_git = os.path.join(worktree, ".git")

    def has_plugin(self, plugin_name: str) -> bool:
        return os.path.islink(os.path.join(self._plugin_dir, plugin_name))

    def link_plugin(self, plugin_path: str):
        (_, name) = os.path.split(plugin_path)
        os.symlink(plugin_path, os.path.join(self._plugin_dir, name), target_is_directory=True)

    def linked_plugins(self):
        "List all plugins linked into plugins directory."
        for plugin in os.listdir(self._plugin_dir):
            path = os.path.join(self._plugin_dir, plugin)
            if os.path.islink(path) and os.path.isdir(path):
                yield plugin

    def unlink_plugin(self, plugin_name):
        "Removes plugin `plugin_name` from plugins directory."
        plugin_path = os.path.join(self._plugin_dir, plugin_name)
        os.unlink(plugin_path)

    def clean_external_plugin_deps(self):
        subprocess.run(["git", "--git-dir", self._dot_git, "restore", "plugins/external_plugin_deps.bzl"], check=True)

    def clean_tools_plugins(self):
        subprocess.run(["git", "--git-dir", self._dot_git, "restore", "tools/bzl/plugins.bzl"], check=True)
