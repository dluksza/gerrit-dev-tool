# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import RootConfig, pass_root_config


@click.group(name="plugins")
def plugins():
    "Administrate installed plugins."
    pass


@click.command(name="list")
@pass_root_config
def list_plugins(root_cfg):
    """Lists currently installed plugins."""
    plugins = list(root_cfg.gerrit_worktree.linked_plugins())
    if len(plugins) == 0:
        click.echo("No plugins are installed")
        return

    for plugin in plugins:
        click.echo(plugin)


@click.command
@click.argument("name", type=str)
@pass_root_config
def install(root_cfg: RootConfig, name: str):
    """Install plugin by name.

    Link plugin into plugins directory and update external_plugin_deps.bzl if needed.
    """
    click.echo("install %s plugin" % name)


@click.command
@click.argument("name")
@pass_root_config
def uninstall(root_cfg, name):
    """Uninstall plugin by name.

    Remove plugin from plugins directory and update external_plugin_deps.bzl if needed.
    """
    click.echo("uinstall %s plugin" % name)


@click.command()
@click.argument("name")
@pass_root_config
def test(root_cfg):
    """Run plugin tests."""
    click.echo("test plugin to gerrit")


@click.command()
@click.argument("name")
@pass_root_config
def deploy(root_cfg):
    """Build and deploy plugin to Gerrit test site."""
    click.echo("deploy plugin to gerrit")


@click.command
@pass_root_config
def clean(root_cfg):
    """Cleans up Gerrit working directory.

    Removes all linked plugins and changes to plugins/external_plugin_deps.bzl and tools/bzl/plugins.bzl.
    """
    for plugin in root_cfg.gerrit_worktree.linked_plugins():
        if root_cfg.verbose:
            click.echo("Removing plugin: %s", plugin)
        click.echo("linked plugin: %s" % plugin)
        root_cfg.gerrit_worktree.unlink_plugin(plugin)

    if root_cfg.verbose:
        click.echo("Restore plugins/external_plugin_deps.bzl")
    root_cfg.gerrit_worktree.clean_external_plugin_deps()

    if root_cfg.verbose:
        click.echo("Restore tools/bzl/plugins.bzl")
    root_cfg.gerrit_worktree.clean_tools_plugins()


plugins.add_command(list_plugins)
plugins.add_command(install)
plugins.add_command(uninstall)
plugins.add_command(test)
plugins.add_command(deploy)
plugins.add_command(clean)
