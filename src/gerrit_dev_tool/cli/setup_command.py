# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import click

from gerrit_dev_tool.git_client import GitClient
from gerrit_dev_tool.bazel_client import BazelClient
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace
from gerrit_dev_tool.testsite_client import TestsiteClient
from gerrit_dev_tool.urls import Urls


@click.command
@click.option(
    "-n",
    "--name",
    default=os.path.join(os.getcwd(), "gerrit-workspace"),
    type=click.Path(exists=False, file_okay=False, resolve_path=True),
    help="Name of directory where workspace should be initialised.",
)
@click.option("--no-build", is_flag=True, help="Don't build Gerrit during setup also implies '--no-init'")
@click.option("--no-init", is_flag=True, help="Don't initialize Gerrit testsite.")
def setup(name, no_build, no_init):
    """Setup Gerrit Dev Tool workspace.

    Creates a directory structure for Gerrit Dev Tool to operate and clones the Gerrit project.
    """
    workspace = GrdtWorkspace.create(name)
    GitClient.clone(Urls.gerrit, workspace.gerrit())

    if not no_build:
        bazel = BazelClient(workspace.gerrit())
        bazel.sync()
        bazel.build("gerrit")

    if not no_build or not no_init:
        TestsiteClient(workspace).init_dev()
