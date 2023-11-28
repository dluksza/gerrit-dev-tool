# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

import os

from gerrit_dev_tool.config_parser import ConfigParser

example_config = "./tests/gerrit.config"


def test_no_op(tmp_path):
    parser = ConfigParser()
    output_file = os.path.join(tmp_path, "output.config")

    with open(output_file, "w") as output:
        parser.read(example_config)
        parser.write(output)

    with open(example_config) as expected, open(output_file) as actual:
        assert expected.read() == actual.read()


def test_add_list_option(tmp_path):
    parser = ConfigParser()
    output_file = os.path.join(tmp_path, "output.config")

    with open(output_file, "w") as output:
        parser.read(example_config)
        parser.read("./tests/append_list_item.config")
        parser.write(output)

    actual = ConfigParser()
    actual.read(output_file)

    assert len(actual["container"].getlist("javaOptions")) == 3


def test_add_section(tmp_path):
    parser = ConfigParser()
    output_file = os.path.join(tmp_path, "output.config")

    with open(output_file, "w") as output:
        parser.read(example_config)
        parser.read("./tests/append_section.config")
        parser.write(output)

    actual = ConfigParser()
    actual.read(output_file)

    assert actual["github"].get("url") == "https://github.com"


def test_remove_value_from_list():
    parser = ConfigParser()
    parser.read(example_config)

    assert len(parser["container"].getlist("javaOptions")) == 2
    javaOption = parser["container"].getlist("javaOptions")[0]

    parser.remove_value("container", "javaOptions", javaOption)

    assert len(parser["container"].getlist("javaOptions")) == 1


def test_remove_scalar_value():
    parser = ConfigParser()
    parser.read(example_config)

    assert "basePath" in parser["gerrit"]

    parser.remove_value("gerrit", "basePath", "git")

    assert "basePath" not in parser["gerrit"]
