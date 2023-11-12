# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.parser import BazelImport, BazelMavenJar, BazelParser

example_config = """
load("//tools/bzl:maven_jar.bzl", "maven_jar")

def external_plugin_deps():
    maven_jar(
        name = "kafka-client",
        artifact = "org.apache.kafka:kafka-clients:2.1.1",
        sha1 = "a7b72831768ccfd69128385130409ae1a0e52f5f",
    )
""".lstrip()


def test_parse_extenal_plugin_deps():
    actual = BazelParser.external_plugin_deps(example_config)

    assert actual.imports == {BazelImport("//tools/bzl:maven_jar.bzl", ["maven_jar"])}
    assert actual.dependencies == {
        BazelMavenJar(
            "kafka-client", "org.apache.kafka:kafka-clients:2.1.1", "a7b72831768ccfd69128385130409ae1a0e52f5f"
        )
    }


def test_parse_and_serialize():
    actual = BazelParser.external_plugin_deps(example_config)

    assert actual.to_bazel_file() == example_config


def test_parse_empty_config():
    actual = BazelParser.external_plugin_deps("")

    assert actual.imports == frozenset()
    assert actual.dependencies == frozenset()


def test_parse_and_serialize_empty():
    actual = BazelParser.external_plugin_deps("")

    assert (
        actual.to_bazel_file()
        == """
def external_plugin_deps():
    pass
""".lstrip()
    )
