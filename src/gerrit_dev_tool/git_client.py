# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import stat
import subprocess

import requests


class GitClient:
    @staticmethod
    def clone(url: str, dst: str) -> None:
        subprocess.run(
            ["git", "clone", "--recurse-submodules", url, dst],  # noqa: S603 S607
            check=True,
        )

    @staticmethod
    def install_commit_msg_hook(dst: str) -> None:
        hooks_path = os.path.join(dst, ".git", "hooks")
        msg_hook_path = os.path.join(hooks_path, "commit-msg")
        resp = requests.get(
            "https://gerrit-review.googlesource.com/tools/hooks/commit-msg",
            allow_redirects=True,
        )
        os.makedirs(hooks_path)
        with open(msg_hook_path, "wb") as msg_hook:
            msg_hook.write(resp.content)
        os.chmod(msg_hook_path, os.stat(msg_hook_path).st_mode | stat.S_IEXEC)
