# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import re

from gerrit_dev_tool.config_parser import ConfigParser
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace
from gerrit_dev_tool.utils.version_utils import negotiate_version

_version_matcher = re.compile(r"^\d+\.\d+$")


class PluginVersionRecipe:
    def __init__(self, root: str) -> None:
        self._root = root

    def gerrit_config(self) -> ConfigParser | None:
        config_path = os.path.join(self._root, "etc", "gerrit.config")
        if not os.path.isfile(config_path):
            return

        config_parser = ConfigParser()
        with open(config_path) as config:
            config_parser.read_string(config.read())

            return config_parser


class Recipes:
    def __init__(self, workspace: GrdtWorkspace):
        self._root = workspace.recipes

    def for_plugin(self, name: str, version: str) -> PluginVersionRecipe | None:
        plugin_dir = os.path.join(self._root, name)
        if not os.path.isdir(plugin_dir):
            return

        versions = [
            elem
            for elem in os.listdir(plugin_dir)
            if os.path.isdir(os.path.join(plugin_dir, elem)) and _version_matcher.match(elem)
        ]

        plugin_version = negotiate_version(version, versions)
        resource_dir = os.path.join(plugin_dir, plugin_version)

        return PluginVersionRecipe(resource_dir)
