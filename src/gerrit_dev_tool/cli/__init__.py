# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.__about__ import __version__
from gerrit_dev_tool.cli.checkout_command import checkout
from gerrit_dev_tool.cli.root_config import RootConfig


@click.option("--verbose", is_flag=True)
@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="grdt - Gerrit Dev Tool")
@click.pass_context
def gerrit_dev_tool(ctx, verbose):
    ctx.obj = RootConfig(verbose=verbose)


gerrit_dev_tool.add_command(checkout)
