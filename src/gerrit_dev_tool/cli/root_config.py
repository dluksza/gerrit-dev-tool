# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import click


class RootConfig:
    def __init__(self, verbose=False):
        self.verbose = verbose


pass_root_config = click.make_pass_decorator(RootConfig)
