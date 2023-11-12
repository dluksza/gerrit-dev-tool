# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os

from gerrit_dev_tool.bazel.parser import BazelParser
from gerrit_dev_tool.bazel.plugin_external_deps import PluginExternalDeps

_extenrnal_deps = "external_plugin_deps.bzl"


class GerritPlugin:
    def __init__(self, name: str, path: str) -> None:
        self._name = name
        self._path = path

    def has_external_deps(self) -> bool:
        return os.path.isfile(self._external_deps_path())

    def get_extenal_deps(self) -> PluginExternalDeps:
        if not self.has_external_deps():
            return PluginExternalDeps([], [])

        with open(self._external_deps_path()) as deps_file:
            deps = deps_file.read().strip()
            return BazelParser.external_plugin_deps(deps)

    def _external_deps_path(self) -> str:
        return os.path.join(self._path, _extenrnal_deps)
