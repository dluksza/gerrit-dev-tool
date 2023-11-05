# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess

from click.testing import CliRunner

from gerrit_dev_tool.cli import gerrit_dev_tool
from gerrit_dev_tool.urls import Urls

_java_dir = "mocked-java-dir"


def test_default_execution(mocker, tmp_path):
    mocker.patch("subprocess.run")
    mocker.patch("subprocess.check_output", return_value=_java_dir)
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as cwd:
        result = runner.invoke(gerrit_dev_tool, ["setup"])

        print(result.output)
        assert result.exit_code == 0

        assert_directory_structure(cwd)
        assert_gerrit_cloned(cwd)
        assert_build_gerrit(cwd)
        assert_site_initialized(cwd)


def assert_directory_structure(cwd, name="gerrit-workspace"):
    workspace = os.path.join(cwd, name)

    assert os.path.isdir(workspace)
    assert os.path.isfile(os.path.join(workspace, ".grdt-workspace"))
    assert os.path.isdir(os.path.join(workspace, "plugins"))
    assert os.path.isdir(os.path.join(workspace, "modules"))
    assert os.path.isdir(os.path.join(workspace, "sites", "master"))
    assert os.path.isdir(os.path.join(workspace, "gerrit"))
    assert os.path.islink(os.path.join(workspace, "gerrit_testsite"))


def assert_gerrit_cloned(cwd, name="gerrit-workspace"):
    subprocess.run.assert_any_call(
        ["git", "clone", "--recurse-submodules", Urls.gerrit, os.path.join(cwd, name, "gerrit")],
        check=True,
    )


def assert_build_gerrit(cwd, name="gerrit-workspace"):
    cwd = os.path.join(cwd, name, "gerrit")

    subprocess.run.assert_any_call(["bazel", "sync"], cwd=cwd, check=True)
    subprocess.run.assert_any_call(["bazel", "build", "gerrit"], cwd=cwd, check=True)


def assert_site_initialized(cwd, name="gerrit-workspace"):
    root = os.path.join(cwd, name)
    cwd = os.path.join(root, "gerrit")

    subprocess.check_output.assert_any_call(
        ["bazel", "info", "output_base"], text=True, cwd=cwd, stderr=subprocess.DEVNULL
    )
    subprocess.run.assert_any_call(
        [
            os.path.join(cwd, _java_dir, "external", "local_jdk", "bin", "java"),
            "-jar",
            "bazel-bin/gerrit.war",
            "init",
            "--batch",
            "--no-auto-start",
            "--dev",
            "-d",
            os.path.join(root, "gerrit_testsite"),
        ],
        cwd=cwd,
        check=True,
    )
