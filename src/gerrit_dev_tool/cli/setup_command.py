# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os

import click

from gerrit_dev_tool.bazel_client import BazelClient
from gerrit_dev_tool.git_client import GitClient
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace
from gerrit_dev_tool.testsite_client import TestsiteClient
from gerrit_dev_tool.urls import Urls


@click.command
@click.option(
    "-n",
    "--name",
    default="gerrit-workspace",
    type=str,
    help="Name of directory where workspace should be initialised.",
)
@click.option("--no-build", is_flag=True, help="Don't build Gerrit during setup also implies '--no-init'")
@click.option("--no-init", is_flag=True, help="Don't initialize Gerrit testsite.")
@click.pass_context
def setup(ctx: click.Context, name: str, no_build: bool, no_init: bool):
    """Setup Gerrit Dev Tool workspace.

    Creates a directory structure for Gerrit Dev Tool to operate and clones the Gerrit project.
    """
    path = os.path.join(os.getcwd(), name)

    if GrdtWorkspace.discover(path) is not None:
        click.echo(f"Error: Workspace already exists at: {path}")
        ctx.exit(1)

    workspace = GrdtWorkspace.create(path)
    GitClient.clone(Urls.gerrit, workspace.gerrit)
    GitClient.install_commit_msg_hook(workspace.gerrit)

    if not no_build:
        bazel = BazelClient(workspace.gerrit)
        bazel.sync()
        bazel.build("gerrit")

    if not no_build or not no_init:
        TestsiteClient(workspace).init_dev()
