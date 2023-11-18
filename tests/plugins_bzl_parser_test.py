# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

from gerrit_dev_tool.plugins_bzl_parser import parse_plugins_bzl


def test_parse_empty_custom_plugins():
    result = parse_plugins_bzl(
        """
CORE_PLUGINS = ["codemirror-editor"]

CUSTOM_PLUGINS = [
    # Add custom core plugins here
]

CUSTOM_PLUGINS_TEST_DEPS = [
    # add custom core plugins with tests deps here
]
"""
    )

    assert result.core == {"codemirror-editor"}
    assert result.custom == set()
    assert result.custom_test == set()


def test_parse_custom_plugins():
    result = parse_plugins_bzl(
        """
CORE_PLUGINS = ["replication"]

CUSTOM_PLUGINS = ["quota"]

CUSTOM_PLUGINS_TEST_DEPS = ["quota"]
"""
    )

    assert result.core == {"replication"}
    assert result.custom == {"quota"}
    assert result.custom_test == {"quota"}
