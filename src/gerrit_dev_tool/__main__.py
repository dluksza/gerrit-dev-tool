# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
import sys

if __name__ == "__main__":
    from gerrit_dev_tool.cli import gerrit_dev_tool

    sys.exit(gerrit_dev_tool())
