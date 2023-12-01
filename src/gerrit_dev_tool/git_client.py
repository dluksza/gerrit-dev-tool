# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os
import re
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
    def checkout(workdir: str, branch: str) -> None:
        GitClient._git(workdir, "checkout", "--recurse-submodules", branch)

    @staticmethod
    def install_commit_msg_hook(dst: str) -> None:
        hooks_path = os.path.join(dst, ".git", "hooks")
        msg_hook_path = os.path.join(hooks_path, "commit-msg")
        resp = requests.get(
            "https://gerrit-review.googlesource.com/tools/hooks/commit-msg",
            allow_redirects=True,
        )
        os.makedirs(hooks_path, exist_ok=True)
        with open(msg_hook_path, "wb") as msg_hook:
            msg_hook.write(resp.content)
        os.chmod(msg_hook_path, os.stat(msg_hook_path).st_mode | stat.S_IEXEC)

    @staticmethod
    def restore_file(workdir: str, path: str) -> None:
        GitClient._git(workdir, "restore", "--worktree", "--staged", path)

    @staticmethod
    def list_remote_branches(workdir: str, pattern: str) -> list[str]:
        return [
            branch.strip()
            for branch in GitClient._exec(
                workdir,
                "git",
                "branch",
                "--remote",
                "--list",
                pattern,
            ).split("\n")
        ]

    @staticmethod
    def version(workdir: str) -> str:
        branches = GitClient.list_remote_branches(workdir, "origin/stable-*")
        stable_branches = sorted(
            filter(
                lambda branch: re.match(r"^origin/stable-\d+\.\d+$", branch),
                branches,
            )
        )
        stable_branches.reverse()

        for version in ["origin/master", *stable_branches]:
            result = GitClient._exec(workdir, "git", "branch", "--contains", version)
            if len(result) > 0:
                return version

        return ""

    @staticmethod
    def _git(workdir: str, *cmd: str) -> None:
        subprocess.run(
            ["git", *cmd],  # noqa: S603 S607
            cwd=workdir,
            check=True,
        )

    @staticmethod
    def _exec(workdir: str, *cmd) -> str:
        try:
            return subprocess.check_output(
                cmd,  # noqa: S603
                cwd=workdir,
                text=True,
            )
        except subprocess.CalledProcessError:
            return ""
