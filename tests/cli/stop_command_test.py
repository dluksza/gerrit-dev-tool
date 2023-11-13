# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import subprocess

from click.testing import CliRunner

from gerrit_dev_tool.cli import gerrit_dev_tool
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


def test_stop_gerrit(mocker, tmp_path):
    mocker.patch("subprocess.run")

    runner = CliRunner()
    workspace = GrdtWorkspace.create(os.path.join(tmp_path, "workspace"))

    with runner.isolated_filesystem(temp_dir=workspace.root):
        runner.invoke(gerrit_dev_tool, ["stop"])

        subprocess.run.assert_any_call(["./bin/gerrit.sh", "stop"], cwd=workspace.testsite, check=True)


def test_stop_gerrit_from_any_directroy(mocker, tmp_path):
    mocker.patch("subprocess.run")

    runner = CliRunner()
    workspace = GrdtWorkspace.create(os.path.join(tmp_path, "workspace"))

    with runner.isolated_filesystem(temp_dir=workspace.plugins):
        runner.invoke(gerrit_dev_tool, ["stop"])

        subprocess.run.assert_any_call(["./bin/gerrit.sh", "stop"], cwd=workspace.testsite, check=True)
