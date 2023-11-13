# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import subprocess


class BazelClient:
    def __init__(self, workdir: str):
        self.workdir = workdir

    def sync(self):
        self._run("sync")

    def build(self, target: str):
        self._run("build", target)

    def _run(self, *args):
        subprocess.run(
            ["bazel", *args],  # noqa: S603 S607
            cwd=self.workdir,
            check=True,
        )
