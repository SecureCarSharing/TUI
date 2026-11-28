from dataclasses import InitVar, dataclass, field
from typing import Any, Callable, List, Optional

from valid8 import validate


@dataclass(frozen=True)
class MenuHeader:
    value: str

    def __post_init__(self):
        validate('value', self.value, instance_of=str, custom=lambda v: v.strip() != '',
                 help_msg='Header must not be blank')


@dataclass(frozen=True)
class MenuEntry:
    option: str
    function: Callable[[], None]

    def __post_init__(self):
        validate('option', self.option, instance_of=str, custom=lambda v: v.strip() != '',
                 help_msg='Option must not be blank')
        validate('function', self.function, custom=callable, help_msg='Function must be callable')


@dataclass(frozen=True)
class Menu:
    header: MenuHeader
    __entries: List[MenuEntry] = field(default_factory=list, init=False, repr=False)
    create_key: InitVar[Any] = field(default=None)

    def __post_init__(self, create_key: Any):
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key,
                 help_msg='Use Menu.builder() to create a Menu')
        validate('header', self.header, instance_of=MenuHeader)

    def _add_entry(self, entry: MenuEntry, create_key: Any) -> None:
        validate('create_key', create_key, custom=Menu.Builder.is_valid_key)
        validate('entry', entry, instance_of=MenuEntry)
        self.__entries.append(entry)

    def _has_entries(self) -> bool:
        return len(self.__entries) > 0

    def textual_menu(self) -> str:
        lines = [self.header.value]
        lines += [f'{index}) {entry.option}' for index, entry in enumerate(self.__entries)]
        return '\n'.join(lines) + '\n'

    def user_choice(self, index: int) -> None:
        validate('index', index, instance_of=int, min_value=0, max_value=len(self.__entries) - 1)
        self.__entries[index].function()

    @staticmethod
    def builder(header: MenuHeader) -> 'Menu.Builder':
        return Menu.Builder(header)

    class Builder:
        __create_key = object()

        def __init__(self, header: MenuHeader):
            self.__menu: Optional[Menu] = Menu(header, create_key=self.__create_key)

        @staticmethod
        def is_valid_key(key: Any) -> bool:
            return key is Menu.Builder.__create_key

        def with_entry(self, option: str, function: Callable[[], None]) -> 'Menu.Builder':
            validate('menu', self.__menu, help_msg='Builder already used')
            self.__menu._add_entry(MenuEntry(option, function), self.__create_key)
            return self

        def build(self) -> 'Menu':
            validate('menu', self.__menu, help_msg='Builder already used')
            validate('entries', self.__menu._has_entries(), equals=True,
                     help_msg='There must be at least 1 option')
            menu, self.__menu = self.__menu, None
            return menu
