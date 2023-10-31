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
        os.mkdir(os.path.join(root, _plugins_dir))
        os.mkdir(os.path.join(root, _modules_dir))
        os.mkdir(os.path.join(root, _sites_dir))
        os.mkdir(os.path.join(root, _sites_dir, _default_site_name))
        os.mkdir(os.path.join(root, _gerrit_dir))
        os.mkdir(os.path.join(root, _recepies_dir))
        os.symlink(
            os.path.join(_sites_dir, _default_site_name),
            os.path.join(root, _testsite_dir),
            target_is_directory=True,
        )

        return GrdtWorkspace(root)

    def __init__(self, root):
        self._root = root

    def plugins(self):
        return os.path.join(self._root, _plugins_dir)

    def modules(self):
        return os.path.join(self._root, _modules_dir)

    def sites(self):
        return os.path.join(self._root, _sites_dir)

    def recepies(self):
        return os.path.join(self._root, _recepies_dir)

    def testsite(self):
        return os.path.join(self._root, _testsite_dir)

    def gerrit(self):
        return os.path.join(self._root, _gerrit_dir)
