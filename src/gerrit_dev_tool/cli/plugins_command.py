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
def list_plugins(root_cfg: RootConfig):
    """Lists currently installed plugins."""
    plugins = list(root_cfg.gerrit_worktree.linked_plugins())
    if len(plugins) == 0:
        click.echo("No plugins are installed")
        return

    for plugin in plugins:
        click.echo(plugin)


@click.command
@click.argument("name", type=str)
@click.pass_context
def install(ctx: click.Context, name: str):
    """Install plugin by name.

    Link plugin into plugins directory and update external_plugin_deps.bzl if needed.
    """
    root_cfg = ctx.ensure_object(RootConfig)
    if root_cfg.gerrit_worktree.has_plugin(name):
        click.echo("Plugin already installed")
        ctx.exit(0)

    plugin_path = root_cfg.plugin_repo.get_path(name)
    if plugin_path is None:
        click.echo(f"Plugin {name} was not found in default locations.")
        ctx.exit(3)

    root_cfg.gerrit_worktree.link_plugin(plugin_path)
    plugin = root_cfg.gerrit_worktree.get_plugin(name)

    # sync plugin branch with Gerrit branch
    gerrit_version = root_cfg.gerrit_worktree.version()
    plugin.set_version(gerrit_version)

    for internal_dependency in plugin.get_internal_deps():
        ctx.invoke(install, name=internal_dependency)

    root_cfg.workspace_sync.external_deps()
    root_cfg.workspace_sync.plugins_bzl()
    root_cfg.workspace_sync.eclipse_project()
    jar_path = root_cfg.bazel.build_plugin(name)

    # update Gerrit configuration (if needed)
    root_cfg.site.add_to_config(plugin.config(gerrit_version))
    # deploy plugin JAR to Gerrit
    if plugin.is_moduler():
        root_cfg.site.deploy_module(jar_path)
    else:
        root_cfg.site.deploy_plugin(jar_path)

    click.echo("install %s plugin" % name)


@click.command
@click.argument("name")
@pass_root_config
def uninstall(root_cfg: RootConfig, name: str):
    """Uninstall plugin by name.

    Remove plugin from plugins directory and update external_plugin_deps.bzl if needed.
    """
    plugin = root_cfg.gerrit_worktree.get_plugin(name)
    gerrit_version = root_cfg.gerrit_worktree.version()
    root_cfg.site.remove_from_config(plugin.config(gerrit_version))
    root_cfg.gerrit_worktree.unlink_plugin(name)
    root_cfg.workspace_sync.external_deps()
    root_cfg.workspace_sync.plugins_bzl()
    root_cfg.workspace_sync.eclipse_project()
    click.echo("Uninstall %s plugin" % name)


@click.command()
@click.argument("name")
@pass_root_config
def test(root_cfg: RootConfig, name: str):
    """Run plugin tests."""
    click.echo("test plugin to gerrit")


@click.command()
@click.argument("name")
@pass_root_config
def deploy(root_cfg: RootConfig, name: str):
    """Build and deploy plugin to Gerrit test site."""
    click.echo("deploy plugin to gerrit")


@click.command
@pass_root_config
def clean(root_cfg: RootConfig):
    """Cleans up Gerrit working directory.

    Removes all linked plugins and changes to plugins/external_plugin_deps.bzl and tools/bzl/plugins.bzl.
    """
    for plugin in root_cfg.gerrit_worktree.linked_plugins():
        click.echo("Removing plugin: %s" % plugin)
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
