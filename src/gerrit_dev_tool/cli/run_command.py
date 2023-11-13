# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import RootConfig, pass_root_config


@click.command("run")
@pass_root_config
def run(root_config: RootConfig):
    """Runs Gerrit in foreground."""
    if root_config.verbose:
        click.echo("Starting Gerrit from: %s" % root_config.workspace.gerrit)

    root_config.site.gerrit_sh("run")
