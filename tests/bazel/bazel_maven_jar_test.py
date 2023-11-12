# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.bazel_maven_jar import BazelMavenJar


def test_str():
    maven_jar = str(BazelMavenJar("jna", "net.java.dev.jna:jna:5.8.0", "3551d8d827e54858214107541d3aff9c615cb615"))

    assert (
        maven_jar
        == """
maven_jar(
    name = "jna",
    artifact = "net.java.dev.jna:jna:5.8.0",
    sha1 = "3551d8d827e54858214107541d3aff9c615cb615",
)""".strip()
    )
