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

    def gerrit_plugin(self, *_args, **keywords) -> None:
        pass

    def glob(self, *_args, **keywords) -> list:
        return []

    def java_library(self, name: str, exports: list[str] = [], neverlink=False, *_args, **_keywords) -> None:
        self.java_libraries.append(BazelJavaLibrary(name, bool(neverlink), exports))

    def junit_tests(self, *_args, **_keywords) -> None:
        self.has_unit_tests = True

    def maven_jar(self, name, artifact, sha1, *_args, **_keywords) -> None:
        self.dependencies.append(BazelMavenJar(name, artifact, sha1))

    def package(self, *_args, **_keywords) -> None:
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

        bazel_api = _BazelApi()

        exec(  # noqa: S102
            _code_template.format(code=content),
            {"load": bazel_api.load, "maven_jar": bazel_api.maven_jar},
        )

        return PluginExternalDeps(bazel_api.imports, bazel_api.dependencies)

    @staticmethod
    def build(content: str) -> PluginBuild:
        if content == "":
            return PluginBuild([], [])

        bazel_api = _BazelApi()

        exec(  # noqa: S102
            content,
            {
                "load": bazel_api.load,
                "glob": bazel_api.glob,
                "gerrit_plugin": bazel_api.gerrit_plugin,
                "junit_tests": bazel_api.junit_tests,
                "java_library": bazel_api.java_library,
                "package": bazel_api.package,
                "PLUGIN_DEPS": [],
                "PLUGIN_TEST_DEPS": [],
            },
        )

        return PluginBuild(bazel_api.imports, bazel_api.java_libraries)
