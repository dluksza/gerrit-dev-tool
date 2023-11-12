# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from typing import Self

from gerrit_dev_tool.bazel.bazel_import import BazelImport
from gerrit_dev_tool.bazel.bazel_maven_jar import BazelMavenJar


class PluginExternalDeps:
    def __init__(self, imports: list[BazelImport], dependencies: list[BazelMavenJar]) -> None:
        self.imports = frozenset(imports)
        self.dependencies = frozenset(dependencies)

    def merge(self, other: Self) -> Self:
        merged_imports = self._merge_imports(other)

        return PluginExternalDeps(merged_imports, [*self.dependencies, *other.dependencies])

    def to_bazel_file(self) -> str:
        imports = "\n".join(map(str, self.imports))
        dependencies = (
            "\n\n    ".join(map(lambda d: str(d).replace("\n", "\n    ").strip(), self.dependencies))
            if len(self.dependencies) > 0
            else "pass"
        )
        return f"""
{imports}

def external_plugin_deps():
    {dependencies}
""".lstrip()

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, PluginExternalDeps):
            return False

        return self.imports == __value.imports and self.dependencies == __value.dependencies

    def _merge_imports(self, other: Self) -> list[BazelImport]:
        imports = dict(map(lambda i: (i.module, i), self.imports))

        for other_import in other.imports:
            if other_import.module in imports:
                imports[other_import.module].merge(other_import)
            else:
                imports[other_import.module] = other_import

        return list(imports.values())
