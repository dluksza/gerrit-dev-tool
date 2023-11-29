# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess

from click.testing import CliRunner

from gerrit_dev_tool.cli import gerrit_dev_tool
from gerrit_dev_tool.git_client import GitClient
from gerrit_dev_tool.urls import Urls

_java_dir = "mocked-java-dir"
_default_workspace = "gerrit-workspace"


def setup_mocks(mocker):
    mocker.patch("subprocess.run")
    mocker.patch("subprocess.check_output", return_value=_java_dir)
    mocker.patch("gerrit_dev_tool.git_client.GitClient.install_commit_msg_hook")


def test_default_execution(mocker, tmp_path):
    setup_mocks(mocker)
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as cwd:
        result = runner.invoke(gerrit_dev_tool, ["setup"])

        assert result.exit_code == 0

        assert_directory_structure(cwd)
        assert_gerrit_cloned(cwd)
        assert_install_commit_mst_hook(cwd)
        assert_build_gerrit(cwd)
        assert_site_initialized(cwd)


def test_execution_with_name(mocker, tmp_path):
    workspace_name = "test-workspace"
    setup_mocks(mocker)
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as cwd:
        result = runner.invoke(gerrit_dev_tool, ["setup", "--name", workspace_name])

        assert result.exit_code == 0

        assert_directory_structure(cwd, workspace_name)
        assert_gerrit_cloned(cwd, workspace_name)
        assert_install_commit_mst_hook(cwd, workspace_name)
        assert_build_gerrit(cwd, workspace_name)
        assert_site_initialized(cwd, workspace_name)


def test_default_without_build(mocker, tmp_path):
    setup_mocks(mocker)
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as cwd:
        result = runner.invoke(gerrit_dev_tool, ["setup", "--no-build"])

        assert result.exit_code == 0

        assert_directory_structure(cwd)
        assert_gerrit_cloned(cwd)
        assert_install_commit_mst_hook(cwd)


def test_default_without_init(mocker, tmp_path):
    setup_mocks(mocker)
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as cwd:
        result = runner.invoke(gerrit_dev_tool, ["setup", "--no-init"])

        assert result.exit_code == 0

        assert_directory_structure(cwd)
        assert_gerrit_cloned(cwd)
        assert_install_commit_mst_hook(cwd)
        assert_build_gerrit(cwd)


def test_fail_when_worskspace_exist(tmp_path):
    runner = CliRunner()

    with runner.isolated_filesystem(temp_dir=tmp_path) as cwd:
        root = os.path.join(cwd, _default_workspace)
        os.mkdir(root)
        open(os.path.join(root, ".grdt-workspace"), "a").close()

        result = runner.invoke(gerrit_dev_tool, ["setup"])

        assert result.exit_code == 1
        assert result.output.strip() == f"Error: Workspace already exists at: {root}"


def assert_directory_structure(cwd, name=_default_workspace):
    workspace = os.path.join(cwd, name)

    assert os.path.isdir(workspace)
    assert os.path.isfile(os.path.join(workspace, ".grdt-workspace"))
    assert os.path.isdir(os.path.join(workspace, "plugins"))
    assert os.path.isdir(os.path.join(workspace, "modules"))
    assert os.path.isdir(os.path.join(workspace, "sites", "master"))
    assert os.path.isdir(os.path.join(workspace, "gerrit"))
    assert os.path.islink(os.path.join(workspace, "gerrit_testsite"))


def assert_gerrit_cloned(cwd, name=_default_workspace):
    subprocess.run.assert_any_call(
        ["git", "clone", "--recurse-submodules", Urls.gerrit, os.path.join(cwd, name, "gerrit")],
        check=True,
    )


def assert_install_commit_mst_hook(cwd, name=_default_workspace):
    GitClient.install_commit_msg_hook.assert_any_call(os.path.join(cwd, name, "gerrit"))


def assert_build_gerrit(cwd, name=_default_workspace):
    cwd = os.path.join(cwd, name, "gerrit")

    subprocess.run.assert_any_call(["bazelisk", "sync"], cwd=cwd, check=True)
    subprocess.run.assert_any_call(["bazelisk", "build", "gerrit"], cwd=cwd, check=True)


def assert_site_initialized(cwd, name=_default_workspace):
    root = os.path.join(cwd, name)
    cwd = os.path.join(root, "gerrit")

    subprocess.check_output.assert_any_call(
        ["bazelisk", "info", "output_base"], text=True, cwd=cwd, stderr=subprocess.DEVNULL
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
