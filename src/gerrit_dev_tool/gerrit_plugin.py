# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import re

from gerrit_dev_tool.bazel.parser import BazelParser
from gerrit_dev_tool.bazel.plugin_build import PluginBuild
from gerrit_dev_tool.bazel.plugin_external_deps import PluginExternalDeps
from gerrit_dev_tool.git_client import GitClient

_build = "BUILD"
_extenrnal_deps = "external_plugin_deps.bzl"
_version_match = re.compile(r"^origin/stable-(\d+\.\d+)$")


class GerritPlugin:
    def __init__(self, name: str, path: str) -> None:
        self._name = name
        self._path = path

    def get_build(self) -> PluginBuild:
        with open(os.path.join(self._path, _build)) as build:
            content = build.read().strip()
            return BazelParser.build(content)

    def has_external_deps(self) -> bool:
        return os.path.isfile(self._external_deps_path())

    def get_extenal_deps(self) -> PluginExternalDeps:
        if not self.has_external_deps():
            return PluginExternalDeps([], [])

        with open(self._external_deps_path()) as deps_file:
            deps = deps_file.read().strip()
            return BazelParser.external_plugin_deps(deps)

    def get_internal_deps(self) -> list[str]:
        result = []
        neverlink = filter(lambda library: library.neverlink, self.get_build().java_libraries)
        for library in neverlink:
            exports_exports = filter(lambda e: e.startswith("//plugins/"), library.exports)
            plugin_names = map(lambda e: e.replace("//plugins/", ""), exports_exports)
            result.append(*plugin_names)
        return result

    def set_version(self, version: str) -> None:
        matching_branches = GitClient.list_remote_branches(self._path, version)
        if version in matching_branches:
            GitClient.checkout(self._path, version)
            return

        [expected_major, expected_minor] = version.split(".")
        versions = sorted(GitClient.list_remote_branches(self._path, "origin/stable-*"))

        for version in versions:
            # extract version from branch name
            match = _version_match.search(version)
            if match:
                [major, minor] = match[1].split(".")
                # check for greater version
                if expected_major == major and expected_minor < minor or expected_major < major:
                    GitClient.checkout(self._path, version)
                    return

        GitClient.checkout(self._path, "origin/master")

    def _external_deps_path(self) -> str:
        return os.path.join(self._path, _extenrnal_deps)
