from aiogram.dispatcher.filters import Command, Text
from aiogram import types
from config import ADMIN_ID
from bot import bot, dp
import requests
from bs4 import BeautifulSoup as bs
from aiogram.utils.markdown import hlink
from fake_useragent import UserAgent
from keyboards import languages, language_callback, courses_python, courses_js
import wikipedia
from states import WikiState, HandbookState


@dp.message_handler(Command("handbook"))
async def handbook(message: types.Message):
    await message.answer("Введи название тега,свойства или :псевдокласса \n"
                         "поиск может занять некоторое время")
    await HandbookState.answer.set()


@dp.message_handler(state=HandbookState.answer)
async def answerHandbook(message: types.Message):
    main_page = requests.get("https://htmlbase.ru/")
    if main_page.status_code == 200:
        user_text = message.text
        main_page_bs = bs(main_page.text, "lxml")
        allTags = main_page_bs.findAll("a", class_="menu__link")
        try:
            for i in allTags:
                title = i.attrs["title"].split()[0]
                link = i.attrs["href"]
                if title == user_text.lower():
                    response_page = requests.get(i.attrs["href"])
                    if response_page.status_code == 200:
                        response_page_bs = bs(response_page.text, "lxml")
                        description = response_page_bs.find("p").get_text()
                        await message.answer(f"Найдено!\n\n<b>{description}</b> \n подробнее - {link}")
                        break  # для работы else
            else:
                await message.answer("К сожалению, не найдено")

        except:
            await message.answer("Ошибка! попробуйте снова")
        finally:
            await HandbookState.next()





@dp.message_handler(Command("wiki"))
async def wikipediaSearch(message: types.Message):
    await message.answer(f"Введи нужное тебе слово или тему и получи краткий ответ от Wikipedia \n"
                         f"( <em>не совсем корректно работает с русским языком</em> )")
    await WikiState.answer.set()


@dp.message_handler(state=WikiState.answer)
async def answerWiki(message: types.Message):
    try:
        page = wikipedia.page(message.text)
        title = page.original_title
        content = page.summary
        await message.answer(f"<b>{title}</b> \n\n {content}")

    except:
        await message.answer("Ошибка поиска , попробуйте переформулировать запроc , /wiki")

    finally:
        await WikiState.next()


@dp.message_handler(Command("learn"))
async def toStudy(message: types.Message):
    await message.answer("Здесь вы найдете курсы по языкам для новичков \n"
                         "И полезные фишки если им уже не являетесь\n"
                         "<em>Выберете нужный язык из предложенных:</em>", reply_markup=languages)


@dp.callback_query_handler(text_contains="lang:python:_")
async def langPython(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer("<b>Выбери нужное</b>", reply_markup=courses_python)


@dp.callback_query_handler(text_contains="lang:js:_")
async def langJS(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    await call.message.answer("<b>Выбери нужное</b>", reply_markup=courses_js)


@dp.callback_query_handler(text_contains="lang:python:newbie")
async def langPythonNewbie(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    link = "https://telegra.ph/Kursy-Python-dlya-novichkov-01-13"
    await call.message.answer("Держи крутые курсы по <b>Python</b> для новичков \n"
                              f"{hlink('Нажимай!😜', link)}")


@dp.callback_query_handler(text_contains="lang:python:interesting")
async def langPythonInteresting(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    link = "https://telegra.ph/Interesnye-kanaly-i-sajty-po-Python-01-13"
    await call.message.answer(f"Держи интересные каналы и сайты по <b>Python</b> \n"
                              f"{hlink('Нажимай!😜', link)}")


@dp.callback_query_handler(text_contains="lang:js:newbie")
async def langJsNewbie(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    link = "https://telegra.ph/Kursy-JavaScript-dlya-novichkov-01-13"
    await call.message.answer("Держи крутые курсы по <b>JavaScript</b> для новичков \n"
                              f"{hlink('Нажимай!😜', link)}")


@dp.callback_query_handler(text_contains="lang:js:interesting")
async def langJsInteresting(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    link = "https://telegra.ph/Interesnye-uroki-zadachi-fishki-po-JavaScript-01-13"
    await call.message.answer(f"Держи интересные уроки и фишки <b>JavaScript</b> \n"
                              f"{hlink('Нажимай!😜', link)}")


@dp.callback_query_handler(text_contains="lang:html_css:_")
async def langHtmlAndCss(call: types.CallbackQuery):
    await call.answer(cache_time=60)
    link = "https://telegra.ph/Kursy-HTMLCSS-dlya-novichkov-01-14"
    await call.message.answer("Держи крутые курсы по <b>HTML/CSS</b> для новичков \n"
                              f"{hlink('Нажимай!😜', link)}")


@dp.message_handler(Command("prog_news"))
async def sendProgrammingNews(message: types.Message):
    show = {}
    ua = UserAgent()
    randomUserAgent = ua.random
    # print(randomUserAgent)
    headerUserAgent = {"User-Agent": randomUserAgent}

    page = requests.get("https://itproger.com/news", headers=headerUserAgent)
    if page.status_code == 200:
        soup = bs(page.text, "lxml")
        article = soup.findAll("div", class_="article")[:5]
        for i in article:
            article_a = i.find("a")
            show[f"{article_a.attrs['href']}"] = article_a.attrs['title']
        # keys = list(show.keys())
        # values = list(show.values())

        send_str = "<b>Последние новости мира программирования:</b> \n\n"
        num = 0
        full_link = "https://itproger.com/"
        for k, v in show.items():
            num += 1
            add_str = f"{num}:{v}\n{hlink('Читать статью...', f'{full_link + k}')}\n\n"
            send_str += add_str
        await message.answer(send_str)
        # await bot.send_photo()
    else:
        print(page.status_code)
        await message.answer("Ошибка")

@dp.message_handler(Command("game_news"))
async def sendGamesNews(message: types.Message):
    show = {}

    page = requests.get("https://stopgame.ru/news")
    soup = bs(page.text, "lxml")
    last_three_posts = soup.findAll("div", class_="item article-summary")[:3]
    links = list()
    for a in last_three_posts:
        if a.find("a") is not None:
            # links.append(a.attrs["href"])
            get_a = a.find("a")
            links.append(get_a.attrs["href"])

    for l in links:
        new_page = requests.get(f"https://stopgame.ru{l}")
        new_soup = bs(new_page.text, "lxml")
        title = new_soup.find("h1", class_="article-title").text
        go_to_site = f"https://stopgame.ru{l}"
        show[title] = go_to_site

    keys = list(show.keys())
    values = list(show.values())
    await message.answer("Последние новости в мире игр: \n\n"
                         f"1: {keys[0]} \n{hlink('Читать статью...', f'{values[0]}' )}  \n\n"
                          f"2: {keys[1]} \n{hlink('Читать статью...', f'{values[1]}' )} \n\n" 
                           f"2: {keys[2]} \n{hlink('Читать статью...', f'{values[2]}' )} \n\n"
                           )

@dp.message_handler(Command("start"))
async def startBot(message: types.Message):
    await bot.send_message(message.chat.id, text="Добро пожаловать!🙋‍")