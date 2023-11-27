# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess
from gerrit_dev_tool.config_parser import ConfigParser

from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


class TestsiteClient:
    def __init__(self, workspace: GrdtWorkspace) -> None:
        self._worktree = workspace.gerrit
        self._testsite = workspace.testsite
        self._etc_dir = os.path.join(self._testsite, "etc")
        self._java_path = None

    def get_config(self, config_name) -> str:
        return os.path.join(self._etc_dir, config_name)

    def add_to_config(self, src: ConfigParser | None) -> None:
        if not src:
            return

        site_config = ConfigParser()
        site_config.read(self.get_config("gerrit.config"))
        site_config.read_dict(src)

        with open(os.path.join(self._etc_dir, "gerrit.config"), "w") as output:
            site_config.write(output)

    def remove_from_config(self, src: ConfigParser | None) -> None:
        if not src:
            return

        site_config = ConfigParser()
        site_config.read(self.get_config("gerrit.config"))

        for section in src:
            for option in src[section]:
                site_config.remove_value(section, option, src[section][option])

        with open(os.path.join(self._etc_dir, "gerrit.config"), "w") as output:
            site_config.write(output)

    def gerrit_sh(self, arg: str) -> None:
        subprocess.run(
            ["./bin/gerrit.sh", arg],  # noqa: S603
            cwd=self._testsite,
            check=True,
        )

    def init_dev(self):
        self._run("init", "--batch", "--no-auto-start", "--dev")

    def reindex(self):
        self._run("reindex")

    def deploy_plugin(self, plugin_path: str) -> None:
        subprocess.run(
            ["cp", "-f", plugin_path, os.path.join(self._testsite, "plugins")],  #  noqa: S603 S607
            check=True,
        )

    def deploy_module(self, module_path: str) -> None:
        subprocess.run(
            ["cp", "-f", module_path, os.path.join(self._testsite, "lib")],  #  noqa: S603 S607
            check=True,
        )

    def _run(self, *args):
        if not self._java_path:
            output_base = subprocess.check_output(
                ["bazel", "info", "output_base"],  # noqa: S603 S607
                text=True,
                cwd=self._worktree,
                stderr=subprocess.DEVNULL,
            )
            self._java_path = os.path.join(self._worktree, output_base.strip(), "external", "local_jdk", "bin", "java")

        subprocess.run(
            [self._java_path, "-jar", "bazel-bin/gerrit.war", *args, "-d", self._testsite],  # noqa: S603
            cwd=self._worktree,
            check=True,
        )
