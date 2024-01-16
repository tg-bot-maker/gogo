from random import randint
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class ButtonPagination:  # создаем пагинированный dist всех клавишь
    """Класс пагинации информации в виде клавиатур для TG БОТА"""
    def __init__(self, button_data: dict or list, amount_elements: int):
        self.ButtonData = button_data   # Список для пагинации
        self.NumberRecords = amount_elements    # Количество эллементов на одной странице пагинации

        self.NumberKeyboard = 1
        self.Index = 1
        self.MaxIndex = 0
        self.ListButton = []
        self.ResultPagination = {}
        self.Keyboard = []
        self.SmileNumber = '1️⃣'
        self.CustomKeyboard = []

        self.CurrantPage = 1
        self._Markup = False

    def pagination(self, random_callback_data=None, custom_keyboard=None, horizontal=None) -> InlineKeyboardMarkup:
        self.CustomKeyboard = custom_keyboard
        for data in self.ButtonData:  # создаем список всех клавиш
            if not random_callback_data:
                new_button = InlineKeyboardButton(text=self.ButtonData[data], callback_data=f'item#{data}')
            else:
                callback_data = randint(9999999, 99999999999)
                new_button = InlineKeyboardButton(text=data, callback_data=f'item#{callback_data}')
            self.ListButton.append(new_button)

        for button in self.ListButton:
            if self.NumberKeyboard == self.NumberRecords + 1:
                self.NumberKeyboard = 1
                self.Index += 1
            try:
                self.ResultPagination[self.Index].append(button)
                self.NumberKeyboard += 1
            except KeyError:
                self.ResultPagination.update({self.Index: [button]})
                self.NumberKeyboard += 1
        self.MaxIndex = len(self.ResultPagination)

        keyboard = InlineKeyboardMarkup()
        if not horizontal:
            for key in self.ResultPagination[1]:
                keyboard.row(key)
        else:
            button_repository = []
            for key in self.ResultPagination[1]:
                if len(button_repository) == 1:
                    keyboard.row(button_repository[0], key)
                    button_repository = []
                else:
                    button_repository.append(key)
            if button_repository:
                for key in button_repository:
                    keyboard.row(key)

        left_key = InlineKeyboardButton(text='◀︎', callback_data='amg#left_pages')
        number_page = InlineKeyboardButton(text='1️⃣', callback_data='amg#number_page')
        right_key = InlineKeyboardButton(text='▶︎', callback_data='amg#right_pages')
        keyboard.row(left_key, number_page, right_key)
        if custom_keyboard:
            for custom in custom_keyboard:
                keyboard.row(custom)
        self.Keyboard = keyboard
        return self.Keyboard

    def _markup(self, index):
        keyboard = InlineKeyboardMarkup()
        try:
            for key in self.ResultPagination[index]:
                keyboard.row(key)
        except KeyError:
            for key in self.ResultPagination[1]:
                keyboard.row(key)

        left_key = InlineKeyboardButton(text='◀︎', callback_data='amg#left_pages')
        self._number_smile_convertor(index)
        number_page = InlineKeyboardButton(text=self.SmileNumber, callback_data='amg#number_page')
        right_key = InlineKeyboardButton(text='▶︎', callback_data='amg#right_pages')
        keyboard.row(left_key, number_page, right_key)
        for custom in self.CustomKeyboard:
            keyboard.row(custom)
        self._Markup = keyboard

    def page_switch(self, callback_data: str):
        if callback_data == 'left_pages':
            if self.CurrantPage == 1:
                self.CurrantPage = self.MaxIndex
                self._markup(self.CurrantPage)
            else:
                self.CurrantPage -= 1
                self._markup(self.CurrantPage)
        elif callback_data == 'right_pages':
            if self.CurrantPage == self.MaxIndex:
                self.CurrantPage = 1
                self._markup(self.CurrantPage)
            else:
                self.CurrantPage += 1
                self._markup(self.CurrantPage)
        self.Keyboard = self._Markup
        return self.Keyboard

    def _number_smile_convertor(self, number):
        constructor = {0: '0️⃣', 1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣'}
        numbers = list(str(number))
        result = ''
        for key in numbers:
            result = result + constructor[int(key)]
        self.SmileNumber = result
