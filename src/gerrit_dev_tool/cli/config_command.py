# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import RootConfig, pass_root_config


@click.command("config")
@click.argument("name", required=False, type=str)
@pass_root_config
def config(root_config: RootConfig, name):
    """Opens Gerrit configuration file from "$test_site/etc" directory for edit.

    NAME name of Gerrit configuration file. Default: "gerrit.config"
    """
    config_path = root_config.site.get_config(name or "gerrit.config")

    if root_config.verbose:
        click.echo("Opening: %s" % config_path)
    click.edit(filename=config_path)
    pass
