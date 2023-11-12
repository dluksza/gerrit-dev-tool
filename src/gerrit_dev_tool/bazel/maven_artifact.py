# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0


class MavenArtifact:
    @staticmethod
    def parse(line: str):
        segments = line.split(":")
        assert len(segments) == 3

        return MavenArtifact(segments[0], segments[1], segments[2])

    def __str__(self) -> str:
        return f"{self.group_id}:{self.artifact_id}:{self.version}"

    def __init__(self, group_id: str, artifact_id: str, version: str) -> None:
        self.group_id = group_id
        self.artifact_id = artifact_id
        self.version = version

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, MavenArtifact):
            return False

        return (
            self.group_id == __value.group_id
            and self.artifact_id == __value.artifact_id
            and self.version == __value.version
        )

    def __hash__(self) -> int:
        return hash((self.group_id, self.artifact_id, self.version))
