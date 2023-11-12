# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.parser import BazelImport, BazelMavenJar, BazelParser
from gerrit_dev_tool.bazel.plugin_build import BazelJavaLibrary

example_config = """
load("//tools/bzl:maven_jar.bzl", "maven_jar")

def external_plugin_deps():
    maven_jar(
        name = "kafka-client",
        artifact = "org.apache.kafka:kafka-clients:2.1.1",
        sha1 = "a7b72831768ccfd69128385130409ae1a0e52f5f",
    )
""".lstrip()

example_build = """
load("//tools/bzl:junit.bzl", "junit_tests")
load(
    "//tools/bzl:plugin.bzl",
    "PLUGIN_DEPS",
    "PLUGIN_TEST_DEPS",
    "gerrit_plugin",
)

gerrit_plugin(
    name = "events-kafka",
    srcs = glob(["src/main/java/**/*.java"]),
    manifest_entries = [
        "Gerrit-PluginName: events-kafka",
        "Gerrit-InitStep: com.googlesource.gerrit.plugins.kafka.InitConfig",
        "Gerrit-Module: com.googlesource.gerrit.plugins.kafka.Module",
        "Implementation-Title: Gerrit Apache Kafka plugin",
        "Implementation-URL: https://gerrit.googlesource.com/plugins/events-kafka",
    ],
    resources = glob(["src/main/resources/**/*"]),
    deps = [
        ":events-broker-neverlink",
        "//lib/httpcomponents:httpclient",
        "@httpasyncclient//jar",
        "@httpcore-nio//jar",
        "@kafka-client//jar",
    ],
)

junit_tests(
    name = "events_kafka_tests",
    timeout = "long",
    srcs = glob(["src/test/java/**/*.java"]),
    resources = glob(["src/test/resources/**/*"]),
    tags = ["events-kafka"],
    deps = [
        ":events-kafka__plugin_test_deps",
        "//plugins/events-broker",
        "@kafka-client//jar",
        "@testcontainers-kafka//jar",
        "@testcontainers//jar",
    ],
)

java_library(
    name = "events-broker-neverlink",
    neverlink = 1,
    exports = ["//plugins/events-broker"],
)
"""


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


def test_parse_plugin_build():
    actual = BazelParser.build(example_build)

    assert (
        BazelJavaLibrary(name="events-broker-neverlink", neverlink=True, exports=["//plugins/events-broker"])
        in actual.java_libraries
    )
