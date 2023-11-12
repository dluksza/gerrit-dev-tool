# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import pytest

from gerrit_dev_tool.bazel.bazel_import import BazelImport


def test_merging():
    i1 = BazelImport("//tools/bzl:maven_jar.bzl", ["maven_jar"])
    i2 = BazelImport("//tools/bzl:maven_jar.bzl", ["other_dependency"])

    assert i1.merge(i1) == i1
    assert i1.merge(i2) == BazelImport("//tools/bzl:maven_jar.bzl", ["maven_jar", "other_dependency"])


def test_do_not_merge_differnt_modules():
    with pytest.raises(AssertionError):
        BazelImport("module1", []).merge(BazelImport("module2", []))


def test_str():
    import_str = str(BazelImport("//tools/bzl:maven_jar.bzl", ["maven_jar"]))

    assert import_str == 'load("//tools/bzl:maven_jar.bzl", "maven_jar")'
