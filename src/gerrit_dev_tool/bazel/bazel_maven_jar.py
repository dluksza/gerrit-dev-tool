# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.maven_artifact import MavenArtifact


class BazelMavenJar:
    def __init__(self, name: str, artifact: str, sha1: str) -> None:
        self.name = name
        self.artifact = MavenArtifact.parse(artifact)
        self.sha1 = sha1

    def __str__(self) -> str:
        return f"""
maven_jar(
    name = "{self.name}",
    artifact = "{self.artifact}",
    sha1 = "{self.sha1}",
)""".strip()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, BazelMavenJar):
            return False

        return self.name == __value.name and self.artifact == __value.artifact and self.sha1 == __value.sha1

    def __hash__(self) -> int:
        return hash((self.name, self.artifact, self.sha1))
