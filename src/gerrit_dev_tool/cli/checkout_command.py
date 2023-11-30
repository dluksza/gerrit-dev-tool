# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import RootConfig, pass_root_config


@click.command("checkout")
@click.argument("version")
@pass_root_config
def checkout(root_cfg: RootConfig, version: str):
    """
    Change workspace version.

    Switches Gerrit, the test site and all installed plugins to a given version.
    """
    if root_cfg.verbose:
        click.echo("> Checkout Gerrit branch: '%s'" % version)
    root_cfg.gerrit_worktree.set_version(version)
    gerrit_version = root_cfg.gerrit_worktree.version()
    plugins = root_cfg.gerrit_worktree.linked_plugins()

    for plugin_name in plugins:
        plugin = root_cfg.gerrit_worktree.get_plugin(plugin_name)
        plugin_version = plugin.set_version(gerrit_version)
        if root_cfg.verbose:
            click.echo(f"> Checkout {plugin_name} to '{plugin_version}'")

    if root_cfg.verbose:
        click.echo("> Updating external_plugin_deps.bzl")
    root_cfg.workspace_sync.external_deps()
    root_cfg.workspace_sync.eclipse_project()

    if version not in root_cfg.site.sites():
        if root_cfg.verbose:
            click.echo("Building Gerrit")
        root_cfg.bazel.build("gerrit")

        if root_cfg.verbose:
            click.echo("Creating new test site")
        root_cfg.site.create(version)
        root_cfg.site.init_dev(version)

    if root_cfg.verbose:
        click.echo(f"> Switching test site to: '{version}'")
    root_cfg.site.switch(version)

    for plugin_name in root_cfg.gerrit_worktree.linked_plugins():
        plugin = root_cfg.gerrit_worktree.get_plugin(plugin_name)
        jar_path = root_cfg.bazel.build_plugin(plugin_name)
        if plugin.is_lib_module():
            root_cfg.site.deploy_module(jar_path)
        else:
            root_cfg.site.deploy_plugin(jar_path)

        root_cfg.site.add_to_config(plugin.config(gerrit_version))
        user_config = root_cfg.recipes.for_plugin(plugin_name, gerrit_version)
        if user_config:
            root_cfg.site.add_to_config(user_config.gerrit_config())
