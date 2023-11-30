# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click

from gerrit_dev_tool.cli.root_config import RootConfig, pass_root_config


@click.group()
def sites():
    """
    Administrate Gerrit test sites
    """
    pass


@click.command(name="list")
@pass_root_config
def list_sites(root_cfg: RootConfig):
    for site in root_cfg.site.sites():
        click.echo(site)


@click.command
@click.argument("name")
@pass_root_config
def snapshot(root_cfg: RootConfig, name: str):
    """
    Create copy of current test site
    """
    root_cfg.site.snapshot(name)


@click.command
@click.argument("name")
@pass_root_config
def switch(root_cfg: RootConfig, name: str):
    """
    Switch current site to given one
    """
    root_cfg.site.switch(name)


@click.command
@click.argument("name")
@pass_root_config
def restore(root_cfg: RootConfig, name: str):
    """
    Replace current test site with the "NAME"
    """
    root_cfg.site.restore(name)


sites.add_command(list_sites)
sites.add_command(snapshot)
sites.add_command(switch)
sites.add_command(restore)
