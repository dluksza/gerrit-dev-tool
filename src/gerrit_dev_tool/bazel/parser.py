# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.bazel_import import BazelImport
from gerrit_dev_tool.bazel.bazel_maven_jar import BazelMavenJar
from gerrit_dev_tool.bazel.plugin_external_deps import PluginExternalDeps


class _BazelApi:
    def __init__(self) -> None:
        self.imports = []
        self.dependencies = []

    def load(self, module: str, *functions):
        self.imports.append(BazelImport(module, list(functions)))

    def maven_jar(self, name, artifact, sha1):
        self.dependencies.append(BazelMavenJar(name, artifact, sha1))


_code_template = """
{code}

external_plugin_deps()
"""


class BazelParser:
    @staticmethod
    def external_plugin_deps(content: str) -> PluginExternalDeps:
        if content == "":
            return PluginExternalDeps([], [])

        bazelApi = _BazelApi()

        exec(
            _code_template.format(code=content),
            {"load": bazelApi.load, "maven_jar": bazelApi.maven_jar},
        )

        return PluginExternalDeps(bazelApi.imports, bazelApi.dependencies)
