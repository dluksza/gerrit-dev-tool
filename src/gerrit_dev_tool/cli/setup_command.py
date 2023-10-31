# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


@click.command
@click.option(
    "-n",
    "--name",
    default="./gerrit-workspace",
    type=click.Path(exists=False, file_okay=False),
    help="Name of directory where workspace should be initialised.",
)
def setup(name):
    """Setup Gerrit Dev Tool workspace.

    Creates a directory structure for Gerrit Dev Tool to operate and clones the Gerrit project.
    """
    GrdtWorkspace.create(name)
