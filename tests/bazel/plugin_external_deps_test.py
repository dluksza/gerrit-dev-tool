# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.bazel_import import BazelImport
from gerrit_dev_tool.bazel.bazel_maven_jar import BazelMavenJar
from gerrit_dev_tool.bazel.plugin_external_deps import PluginExternalDeps


def test_merging():
    d1 = PluginExternalDeps(
        [BazelImport("//tools/bzl:maven_jar.bzl", ["maven_jar"])],
        [
            BazelMavenJar(
                "kafka-client", "org.apache.kafka:kafka-clients:2.1.1", "a7b72831768ccfd69128385130409ae1a0e52f5f"
            )
        ],
    )
    d2 = PluginExternalDeps(
        [BazelImport("//tools/bzl:maven_jar.bzl", ["maven_jar"])],
        [BazelMavenJar("jna", "net.java.dev.jna:jna:5.8.0", "3551d8d827e54858214107541d3aff9c615cb615")],
    )

    assert d1.merge(d1) == d1
    assert d1.merge(d2) == PluginExternalDeps(
        [BazelImport("//tools/bzl:maven_jar.bzl", ["maven_jar"])],
        [
            BazelMavenJar("jna", "net.java.dev.jna:jna:5.8.0", "3551d8d827e54858214107541d3aff9c615cb615"),
            BazelMavenJar(
                "kafka-client", "org.apache.kafka:kafka-clients:2.1.1", "a7b72831768ccfd69128385130409ae1a0e52f5f"
            ),
        ],
    )
