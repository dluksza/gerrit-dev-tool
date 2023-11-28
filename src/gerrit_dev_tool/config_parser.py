# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0

import configparser


class _MultiDict(dict):
    def __setitem__(self, key, value):
        if isinstance(value, list) and key in self:
            current = self[key]
            if isinstance(current, list):
                self[key].extend(value)
            else:
                super(__class__, self).__setitem__(key, [current, *value])
        else:
            super().__setitem__(key, value)


class ConfigParser(configparser.RawConfigParser):
    def __init__(self, allow_no_value=False):
        super().__init__(
            strict=False,
            dict_type=_MultiDict,
            comment_prefixes=("#",),
            inline_comment_prefixes=("#",),
            empty_lines_in_values=False,
            allow_no_value=allow_no_value,
            converters={"list": lambda v: v.split("\n")},
        )
        self._allow_no_value = allow_no_value

    def optionxform(self, optionstr: str) -> str:
        return optionstr

    def write(self, fp, space_around_delimiters=True):
        if space_around_delimiters:
            d = " = "
        else:
            d = "="
        for section in self.sections():
            self._write_section(fp, section, self[section].items(), d)

    def remove_value(self, section_name: str, option_name: str, value) -> None:
        if section_name not in self:
            return
        section = self[section_name]

        if option_name not in section:
            return

        current = section[option_name]
        if value == current:
            section.pop(option_name)
        if "\n" in current:
            current_list = current.split("\n")
            index = current_list.index(value)
            if index > -1:
                current_list.pop(index)
                section[option_name] = "\n".join(current_list)

    def _write_section(self, fp, section_name: str, section_items: str, delimiter: str):
        if len(section_items) == 0:
            return

        fp.write(f"[{section_name}]\n")
        for key, value in section_items:
            if "\n" in value:
                for v in value.split("\n"):
                    self._write_value(fp, key, v, delimiter)
            else:
                self._write_value(fp, key, value, delimiter)

    def _write_value(self, fp, key: str, value: str, delimiter: str) -> None:
        if value is not None or not self._allow_no_value:
            value = delimiter + str(value).replace("\n", "\n\t")
        else:
            value = ""
        fp.write(f"\t{key}{value}\n")
