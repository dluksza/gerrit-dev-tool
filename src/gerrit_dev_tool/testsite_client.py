# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import shutil
import subprocess

from gerrit_dev_tool.config_parser import ConfigParser
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


class TestsiteClient:
    def __init__(self, workspace: GrdtWorkspace) -> None:
        self._sites = workspace.sites
        self._worktree = workspace.gerrit
        self._testsite = workspace.testsite
        self._etc_dir = os.path.join(self._testsite, "etc")
        self._java_path = None

    def current(self) -> str:
        return os.path.split(os.readlink(self._testsite))[-1]

    def sites(self) -> list[str]:
        return [item for item in os.listdir(self._sites) if os.path.isdir(os.path.join(self._sites, item))]

    def snapshot(self, dst: str) -> None:
        dst_path = os.path.join(self._sites, dst)
        src_path = os.readlink(self._testsite)

        shutil.copytree(src_path, dst_path, symlinks=True)

    def create(self, name: str) -> None:
        dst_path = os.path.join(self._sites, name)
        os.mkdir(dst_path)
        self.init_dev(dst_path)

    def switch(self, name: str) -> None:
        dst_path = os.path.join(self._sites, name)
        os.unlink(self._testsite)
        os.symlink(dst_path, self._testsite, target_is_directory=True)

    def restore(self, name: str) -> None:
        dst_path = os.readlink(self._testsite)
        src_path = os.path.join(self._sites, name)

        shutil.rmtree(dst_path)
        shutil.copytree(src_path, dst_path, symlinks=True)

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

    def init_dev(self, site=None):
        self._run("init", "--batch", "--no-auto-start", "--dev", site=site)

    def reindex(self, site=None):
        self._run("reindex", site=site)

    def deploy_plugin(self, plugin_path: str) -> None:
        subprocess.run(
            ["cp", "-f", plugin_path, self._plugins_path()],  #  noqa: S603 S607
            check=True,
        )

    def deploy_module(self, module_path: str) -> None:
        subprocess.run(
            ["cp", "-f", module_path, self._modules_path()],  #  noqa: S603 S607
            check=True,
        )

    def remove_plugin(self, plugin_name: str) -> None:
        os.remove(os.path.join(self._plugins_path(), f"{plugin_name}.jar"))

    def remove_module(self, plugin_name: str) -> None:
        os.remove(os.path.join(self._modules_path(), f"{plugin_name}.jar"))

    def _plugins_path(self) -> str:
        return os.path.join(self._testsite, "plugins")

    def _modules_path(self) -> str:
        return os.path.join(self._testsite, "lib")

    def _run(self, *args, site=None):
        if not self._java_path:
            output_base = subprocess.check_output(
                ["bazelisk", "info", "output_base"],  # noqa: S603 S607
                text=True,
                cwd=self._worktree,
                stderr=subprocess.DEVNULL,
            )
            self._java_path = os.path.join(self._worktree, output_base.strip(), "external", "local_jdk", "bin", "java")

        dst = os.path.join(self._sites, site) if site else self._testsite

        subprocess.run(
            [self._java_path, "-jar", "bazel-bin/gerrit.war", *args, "-d", dst],  # noqa: S603
            cwd=self._worktree,
            check=True,
        )
