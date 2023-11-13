# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import RootConfig, pass_root_config


@click.command("stop")
@pass_root_config
def stop(root_config: RootConfig):
    """Stop Gerrit running in background."""
    if root_config.verbose:
        click.echo("Stopping Gerrit from: %s" % root_config.workspace.gerrit)

    root_config.site.gerrit_sh("stop")
