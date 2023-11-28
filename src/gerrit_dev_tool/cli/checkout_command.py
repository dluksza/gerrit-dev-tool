# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import RootConfig, pass_root_config


@click.command("checkout")
@click.argument("version")
@pass_root_config
def checkout(root_cfg: RootConfig, version: str):
    if root_cfg.verbose:
        click.echo("Checkout Gerrit branch: %s" % version)
    root_cfg.gerrit_worktree.set_version(version)
    gerrit_version = root_cfg.gerrit_worktree.version()
    plugins = root_cfg.gerrit_worktree.linked_plugins()

    for plugin_name in plugins:
        plugin = root_cfg.gerrit_worktree.get_plugin(plugin_name)
        plugin_version = plugin.set_version(gerrit_version)
        if root_cfg.verbose:
            click.echo(f"Checkout {plugin_name} to {plugin_version}")

    if root_cfg.verbose:
        click.echo("Updating external_plugin_deps.bzl")
    root_cfg.workspace_sync.external_deps()
