# SPDX-FileCopyrightText: 2023-present Dariusz Luksza <dariusz.luksza@gmail.com>
#
# SPDX-License-Identifier: Apache-2.0
from typing import Self


class BazelImport:
    def __init__(self, module: str, functions: list[str]) -> None:
        self.module = module
        self.functions = frozenset(functions)

    def merge(self, other: Self) -> Self:
        assert self.module == other.module
        merged_functions = {*self.functions, *other.functions}

        return BazelImport(self.module, [*merged_functions])

    def __str__(self) -> str:
        functions = ", ".join(f'"{function}"' for function in self.functions)
        return f"""load("{self.module}", {functions})"""

    def __eq__(self, __value: object) -> bool:
        if not isinstance(__value, BazelImport):
            return False

        return self.module == __value.module and self.functions == __value.functions

    def __hash__(self) -> int:
        return hash((self.module, *self.functions))
