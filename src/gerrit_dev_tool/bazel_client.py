# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import subprocess


class BazelClient(object):
    def __init__(self, workdir):
        self.workdir = workdir

    def sync(self):
        self._run("sync")

    def build(self, target):
        self._run("build", target)

    def _run(self, *args):
        subprocess.run(["bazel"] + list(args), cwd=self.workdir, check=True)