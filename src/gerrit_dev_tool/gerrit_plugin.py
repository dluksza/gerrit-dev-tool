# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import re
from importlib.resources import contents, files, is_resource
from typing import Iterable

from gerrit_dev_tool.bazel.parser import BazelParser
from gerrit_dev_tool.bazel.plugin_build import PluginBuild
from gerrit_dev_tool.bazel.plugin_external_deps import PluginExternalDeps
from gerrit_dev_tool.config_parser import ConfigParser
from gerrit_dev_tool.git_client import GitClient
from gerrit_dev_tool.utils.version_utils import negotiate_version

_build = "BUILD"
_extenrnal_deps = "external_plugin_deps.bzl"
_git_version_matcher = re.compile(r"^origin/stable-(\d+\.\d+)$")
_package_version_matcher = re.compile(r"^(\d+_\d+)$")


class GerritPlugin:
    def __init__(self, name: str, path: str) -> None:
        self._name = name
        self._path = path
        self._resource_package = f"gerrit_dev_tool.plugins.{name}"

    def config(self, version: str) -> ConfigParser | None:
        if not self._has_resources():
            return

        config_version = negotiate_version(version, self._available_config_versions())

        config_resource = f"{self._resource_package}.{config_version}.etc"
        if not self._has_resources(config_resource):
            return

        config = files(config_resource).joinpath("gerrit.config")
        if config.is_file():
            config_content = config.read_text()
            parser = ConfigParser()
            parser.read_string(config_content)

            return parser

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
            plugin_names = [e.replace("//plugins/", "") for e in exports_exports]
            result.append(*plugin_names)
        return result

    def set_version(self, version: str) -> str:
        plugin_version = negotiate_version(version, self._available_git_versions())
        if plugin_version == "master":
            GitClient.checkout(self._path, "origin/master")
        else:
            GitClient.checkout(self._path, f"origin/stable-{plugin_version}")
        return plugin_version

    def is_lib_module(self) -> bool:
        return not self._is_builtin() or "modules" in os.readlink(self._path)

    def _is_builtin(self):
        return os.path.isdir(self._path)

    def _external_deps_path(self) -> str:
        return os.path.join(self._path, _extenrnal_deps)

    def _has_resources(self, resource=None) -> bool:
        try:
            return files(resource or self._resource_package).is_dir()
        except:
            return False

    def _available_git_versions(self) -> Iterable[str]:
        versions = sorted(GitClient.list_remote_branches(self._path, "origin/stable-*"))
        for version in versions:
            match = _git_version_matcher.search(version)
            if match:
                yield match[1]

    def _available_config_versions(self) -> Iterable[str]:
        for entry in contents(self._resource_package):
            if not is_resource(self._resource_package, entry) and _package_version_matcher.match(entry):
                yield entry
