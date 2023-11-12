# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from gerrit_dev_tool.bazel.bazel_import import BazelImport
from gerrit_dev_tool.bazel.bazel_maven_jar import BazelMavenJar
from gerrit_dev_tool.bazel.plugin_build import BazelJavaLibrary, PluginBuild
from gerrit_dev_tool.bazel.plugin_external_deps import PluginExternalDeps


class _BazelApi:
    def __init__(self) -> None:
        self.imports = []
        self.dependencies = []
        self.java_libraries = []
        self.has_unit_tests = False

    def load(self, module: str, *functions) -> None:
        self.imports.append(BazelImport(module, list(functions)))

    def gerrit_plugin(self, **_args) -> None:
        pass

    def glob(self, *_args) -> None:
        pass

    def java_library(self, name: str, exports: list[str], neverlink=False, *_args, **_keywords) -> None:
        self.java_libraries.append(BazelJavaLibrary(name, bool(neverlink), exports))

    def junit_tests(self, **_args) -> None:
        self.has_unit_tests = True

    def maven_jar(self, name, artifact, sha1) -> None:
        self.dependencies.append(BazelMavenJar(name, artifact, sha1))

    def package(self, **_keywords) -> None:
        pass


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

    @staticmethod
    def build(content: str) -> PluginBuild:
        if content == "":
            return PluginBuild([], [])

        bazelApi = _BazelApi()

        exec(
            content,
            {
                "load": bazelApi.load,
                "glob": bazelApi.glob,
                "gerrit_plugin": bazelApi.gerrit_plugin,
                "junit_tests": bazelApi.junit_tests,
                "java_library": bazelApi.java_library,
                "package": bazelApi.package,
                "PLUGIN_DEPS": [],
                "PLUGIN_TEST_DEPS": [],
            },
        )

        return PluginBuild(bazelApi.imports, bazelApi.java_libraries)
