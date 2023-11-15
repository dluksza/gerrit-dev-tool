# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0


class PluginsBzl:
    def __init__(self, core: set[str], custom: set[str], custom_test: set[str]) -> None:
        self.core = core
        self.custom = custom
        self.custom_test = custom_test

    def __str__(self) -> str:
        return f"""
CORE_PLUGINS = [
    {self._join_plugins(self.core)}
]

CUSTOM_PLUGINS = [
    {self._join_plugins(self.custom)}
]

CUSTOM_PLUGINS_TEST_DEPS = [
    {self._join_custom_test()}
]
""".lstrip()

    def _join_custom_test(self):
        if len(self.custom_test) == 0:
            return "# Add custom core plugins with tests deps here"

        return self._join_plugins(self.custom_test)

    def _join_plugins(self, plugins: set[str]) -> str:
        if len(plugins) == 0:
            return ""

        return ",\n    ".join(f'"{plugin}"' for plugin in sorted(plugins)) + ","


class _PluginsBzlApi:
    def __init__(self):
        self.core = set()
        self.custom = set()
        self.custom_test = set()

    def set_core(self, plugins):
        self.core = set(plugins)

    def set_custom(self, plugins):
        self.custom = set(plugins)

    def set_custom_test(self, plugins):
        self.custom_test = set(plugins)


__template = """
{code}

set_core(CORE_PLUGINS)
set_custom(CUSTOM_PLUGINS)
set_custom_test(CUSTOM_PLUGINS_TEST_DEPS)
"""


def parse_plugins_bzl(content: str) -> PluginsBzl:
    api = _PluginsBzlApi()
    exec(
        __template.format(code=content),
        {
            "set_core": api.set_core,
            "set_custom": api.set_custom,
            "set_custom_test": api.set_custom_test,
        },
    )

    return PluginsBzl(api.core, api.custom, api.custom_test)
