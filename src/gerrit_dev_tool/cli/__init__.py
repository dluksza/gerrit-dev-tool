# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os

import click

from gerrit_dev_tool.__about__ import __version__
from gerrit_dev_tool.cli.checkout_command import checkout
from gerrit_dev_tool.cli.plugins_command import plugins
from gerrit_dev_tool.cli.root_config import RootConfig
from gerrit_dev_tool.cli.setup_command import setup
from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


@click.option("--verbose", is_flag=True)
@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="grdt - Gerrit Dev Tool")
@click.pass_context
def gerrit_dev_tool(ctx: click.Context, verbose: bool):
    workspace = GrdtWorkspace.discover(os.getcwd())

    if ctx.invoked_subcommand != setup.name and workspace is None:
        click.echo("Error: Workspace not found!")
        ctx.exit(2)
    elif workspace is not None:
        ctx.obj = RootConfig(workspace, verbose=verbose)


gerrit_dev_tool.add_command(checkout)
gerrit_dev_tool.add_command(plugins)
gerrit_dev_tool.add_command(setup)
