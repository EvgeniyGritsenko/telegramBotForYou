from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

language_callback = CallbackData("lang", "name", "add")

languages = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Python", callback_data=language_callback.new(
                name="python", add="_"
            )),
            InlineKeyboardButton(text="Java Script", callback_data=language_callback.new(
                name="js", add="_"
            )),
        ],
        [
            InlineKeyboardButton(text="HTML/CSS", callback_data=language_callback.new(
                name="html_css", add="_"
            )),
        ],
    ]
)


courses_python = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Курсы для новичков", callback_data=language_callback.new(
                name="python", add="newbie",
            )),
            InlineKeyboardButton(text="Интересные уроки и фишки", callback_data=language_callback.new(
                name="python", add="interesting",
            )),
        ],
    ]
)


courses_js = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Курсы для новичков", callback_data=language_callback.new(
                name="js", add="newbie",
            )),
            InlineKeyboardButton(text="Интересные уроки и фишки", callback_data=language_callback.new(
                name="js", add="interesting",
            )),
        ],
    ]
)
