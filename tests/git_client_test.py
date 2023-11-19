# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0


from gerrit_dev_tool.git_client import GitClient

_stable_2_8 = "origin/stable-2.8"
_stable_3_8 = "origin/stable-3.8"
_stable_3_9 = "origin/stable-3.9"
_master = "origin/master"


def test_version_no_stable_branches(mocker):
    mocker.patch("subprocess.check_output", return_value="")

    generation = GitClient.version("not-used")

    assert generation == ""


def test_generation_matches_master(mocker):
    def mock_handler(cmd, **_):
        if _is_conains_cmd(cmd) and cmd[3] == _master:
            return f"* (HEAD detached at {_master}\n"
        if _is_remote_cmd(cmd):
            return ""
        raise Exception("mock error")

    mocker.patch("subprocess.check_output", side_effect=mock_handler)

    version = GitClient.version("not-used")

    assert version == _master


def test_version_matches_stable_3_8(mocker):
    def mock_handler(cmd, **_):
        if _is_conains_cmd(cmd):
            if cmd[3] in (_master, _stable_2_8, _stable_3_9):
                return ""
            if cmd[3] == _stable_3_8:
                return f"* (HEAD detached at {_stable_3_8})\n"
        if _is_remote_cmd(cmd):
            return "\n ".join([_stable_2_8, _stable_3_8, _stable_3_9])
        raise Exception("mock error")

    mocker.patch("subprocess.check_output", side_effect=mock_handler)

    version = GitClient.version("not-used")

    assert version == _stable_3_8


def _is_conains_cmd(cmd: list[str]) -> bool:
    return cmd[2] == "--contains"


def _is_remote_cmd(cmd: list[str]) -> bool:
    return cmd[2] == "--remote"
