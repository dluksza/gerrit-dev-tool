# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.bazel_import import BazelImport


class BazelJavaLibrary:
    def __init__(self, name: str, neverlink: bool, exports: list[str]) -> None:
        self.name = name
        self.neverlink = neverlink
        self.exports = exports

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, BazelJavaLibrary):
            return False

        return self.name == __value.name and self.neverlink == __value.neverlink and self.exports == __value.exports

    def __hash__(self) -> int:
        return hash((self.name, self.neverlink, *self.exports))


class PluginBuild:
    def __init__(self, imports: list[BazelImport], java_libraries: list[BazelJavaLibrary]) -> None:
        self.imports = frozenset(imports)
        self.java_libraries = frozenset(java_libraries)

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, PluginBuild):
            return False

        return self.imports == __value.imports and self.java_libraries == __value.java_libraries

    def __hash__(self) -> int:
        return hash((self.imports, self.java_libraries))
