# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess

from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


class TestsiteClient:
    def __init__(self, workspace: GrdtWorkspace) -> None:
        self._worktree = workspace.gerrit
        self._testsite = workspace.testsite
        self._java_path = None

    def init_dev(self):
        self._run("init", "--batch", "--no-auto-start", "--dev")

    def reindex(self):
        self._run("reindex")

    def _run(self, *args):
        if not self._java_path:
            output_base = subprocess.check_output(
                ["bazel", "info", "output_base"],
                text=True,
                cwd=self._worktree,
                stderr=subprocess.DEVNULL,
            )
            self._java_path = os.path.join(self._worktree, output_base.strip(), "external", "local_jdk", "bin", "java")

        subprocess.run(
            [self._java_path, "-jar", "bazel-bin/gerrit.war"] + list(args) + ["-d", self._testsite],
            cwd=self._worktree,
            check=True,
        )
