# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import pass_root_config


@click.command("checkout")
@click.argument("name")
@pass_root_config
def checkout(root_cfg, name):
    if root_cfg.verbose:
        click.echo("Switching to branch: %s" % name)
