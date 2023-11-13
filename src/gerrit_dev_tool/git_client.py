# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import subprocess


class GitClient:
    @staticmethod
    def clone(url: str, dst: str):
        subprocess.run(
            ["git", "clone", "--recurse-submodules", url, dst],  # noqa: S603 S607
            check=True,
        )
