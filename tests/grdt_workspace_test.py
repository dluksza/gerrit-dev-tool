# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import os

from gerrit_dev_tool.grdt_workspace import GrdtWorkspace


def test_discover(tmp_path):
    workspace = "test_gerrit-workspace"
    root = os.path.join(tmp_path, workspace)
    os.makedirs(os.path.join(root, "modules"), exist_ok=True)
    open(os.path.join(root, ".grdt-workspace"), "a").close()

    assert GrdtWorkspace.discover(tmp_path) is None
    assert GrdtWorkspace.discover(root) is not None
    assert GrdtWorkspace.discover(os.path.join(root, "modules")) is not None
