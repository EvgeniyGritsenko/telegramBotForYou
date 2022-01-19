from aiogram.dispatcher.filters.state import State, StatesGroup


class WikiState(StatesGroup):
    answer = State()


class HandbookState(StatesGroup):
    answer = State()
