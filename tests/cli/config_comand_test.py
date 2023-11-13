# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os

import click
from click.testing import CliRunner

from gerrit_dev_tool.cli import gerrit_dev_tool
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


def test_default_value(mocker, tmp_path):
    mocker.patch("click.edit")

    runner = CliRunner()
    workspace = GrdtWorkspace.create(os.path.join(tmp_path, "workspace"))

    with runner.isolated_filesystem(temp_dir=workspace.root):
        runner.invoke(gerrit_dev_tool, ["config"])

        assert_config_opened(workspace)


def test_open_config_from_anywhere(mocker, tmp_path):
    mocker.patch("click.edit")

    runner = CliRunner()
    workspace = GrdtWorkspace.create(os.path.join(tmp_path, "workspace"))

    with runner.isolated_filesystem(temp_dir=workspace.modules):
        runner.invoke(gerrit_dev_tool, ["config"])

        assert_config_opened(workspace)


def test_open_any_file(mocker, tmp_path):
    mocker.patch("click.edit")

    runner = CliRunner()
    filename = "sercure.config"
    workspace = GrdtWorkspace.create(os.path.join(tmp_path, "workspace"))

    with runner.isolated_filesystem(temp_dir=workspace.modules):
        runner.invoke(gerrit_dev_tool, ["config", filename])

        assert_config_opened(workspace, filename)


def assert_config_opened(workspace: GrdtWorkspace, name="gerrit.config"):
    click.edit.assert_any_call(filename=os.path.join(workspace.testsite, "etc", name))
