# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os

import requests

from gerrit_dev_tool.git_client import GitClient
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace
from gerrit_dev_tool.urls import Urls


class PluginRepository:
    def __init__(self, workspace: GrdtWorkspace) -> None:
        self.workspace = workspace

    def get_path(self, plugin_name: str):
        plugin_path = self.workspace.plugin_path(plugin_name)
        if os.path.isdir(plugin_path):
            return plugin_path

        module_path = self.workspace.module_path(plugin_name)
        if os.path.isdir(module_path):
            return module_path

        plugin_url = Urls.plugin_url(plugin_name)
        if self._has_repository(plugin_url):
            self._clone(plugin_url, plugin_path)
            return plugin_path

        module_url = Urls.module_url(plugin_name)
        if self._has_repository(module_url):
            self._clone(module_url, module_path)
            return module_path

        return None

    def _has_repository(self, url) -> bool:
        resp = requests.head(url)

        return resp.ok

    def _clone(self, src: str, dst: str) -> None:
        GitClient.clone(src, dst)
        GitClient.install_commit_msg_hook(dst)
