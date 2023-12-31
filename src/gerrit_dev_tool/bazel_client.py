# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess


class BazelClient:
    def __init__(self, workdir: str) -> None:
        self.workdir = workdir

    def sync(self) -> None:
        self._run("sync")

    def build(self, target: str) -> None:
        self._run("build", target)

    def build_plugin(self, plugin_name: str) -> str:
        self._run("build", f"//plugins/{plugin_name}")
        return os.path.join(self.workdir, "bazel-bin", "plugins", plugin_name, f"{plugin_name}.jar")

    def _run(self, *args) -> None:
        subprocess.run(
            ["bazelisk", *args],  # noqa: S603 S607
            cwd=self.workdir,
            check=True,
        )
