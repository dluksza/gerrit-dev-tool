# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os

"Root directory for all of the cloned plugins"
_plugins_dir = "plugins"
"Root directory for all for the cloned modules"
_modules_dir = "modules"
"Root directory for all test site configurations"
_sites_dir = "sites"
"Name of the default test site"
_default_site_name = "master"
"Directory where custom recipes are stored"
_recepies_dir = "recipes"
"Main Gerrit working directory"
_gerrit_dir = "gerrit"
"The Gerrit's test site location"
_testsite_dir = "gerrit_testsite"
"Marker file to mark root location of grdt workspace"
_grdt_marker = ".grdt-workspace"


class GrdtWorkspace:
    @staticmethod
    def create(root: str):
        os.mkdir(root)
        open(os.path.join(root, _grdt_marker), "a").close()

        workspace = GrdtWorkspace(root)
        default_site = os.path.join(workspace.sites, _default_site_name)

        os.mkdir(workspace.plugins)
        os.mkdir(workspace.modules)
        os.mkdir(workspace.sites)
        os.mkdir(default_site)
        os.mkdir(workspace.gerrit)
        os.mkdir(workspace.recepies)
        os.symlink(default_site, workspace.testsite, target_is_directory=True)

        return workspace

    @staticmethod
    def discover(directory: str):
        location = directory
        prev_location = None
        while location != prev_location:
            if os.path.isfile(os.path.join(location, _grdt_marker)):
                return GrdtWorkspace(location)
            else:
                prev_location = location
                location = os.path.abspath(os.path.join(location, os.path.pardir))

        return None

    def __init__(self, root):
        self.root = root
        self.plugins = os.path.join(root, _plugins_dir)
        self.modules = os.path.join(root, _modules_dir)
        self.sites = os.path.join(root, _sites_dir)
        self.recepies = os.path.join(root, _recepies_dir)
        self.testsite = os.path.join(root, _testsite_dir)
        self.gerrit = os.path.join(root, _gerrit_dir)

    def plugin_path(self, plugin_name: str) -> str:
        return os.path.join(self.plugins, plugin_name)

    def module_path(self, plugin_name: str) -> str:
        return os.path.join(self.modules, plugin_name)
