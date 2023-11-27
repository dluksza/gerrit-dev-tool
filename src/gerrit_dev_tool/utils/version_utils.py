# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0


from typing import Iterable


def negotiate_version(expected: str, available: Iterable[str]) -> str:
    """
    Pick matching version from the list of available stable versions.

    A plugin can be compatible with multiple stable Gerrit versions. It also may
    not have a stable matching branch at all, or have one that was created for
    two or three version before.

    This function will pick a potentially matching branch on a simple heuristic:
     * if required version is `master` -> return `master`
     * if both version match -> return that version
     * try find lowest matching version
     * otherwise, return `master`

    >>> negotiate_version("master", ["3.1", "3.2"])
    'master'
    >>> negotiate_version("3.5", ["3.1", "3.2"])
    'master'
    >>> negotiate_version("3.3", ["3.1", "3.2", "3.4"])
    '3.2'
    >>> negotiate_version("3.1", ["3.1", "3.2"])
    '3.1'
    """
    if expected == "master":
        return "master"

    [expected_major, expected_minor] = expected.split(".")
    versions = sorted(available)
    versions.reverse()

    for version in versions:
        if expected == version:
            return expected

        [major, minor] = version.split(".")
        if expected_major == major and expected_minor > minor:
            if versions.index(version) == 0:
                return "master"
            return f"{major}.{minor}"

    return "master"
