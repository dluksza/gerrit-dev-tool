# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0


class Urls:
    gerrit = "https://gerrit.googlesource.com/gerrit"
    plugins = "https://gerrit.googlesource.com/plugins/"
    modules = "https://gerrit.googlesource.com/modules/"

    @staticmethod
    def plugin_url(plugin_name: str) -> str:
        return Urls.plugins + plugin_name

    @staticmethod
    def module_url(plugin_name: str) -> str:
        return Urls.modules + plugin_name
