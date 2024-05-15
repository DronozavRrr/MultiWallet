from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window


class CryptoWalletPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 1  # Один столбец для всех элементов
        self.padding = 10
        self.spacing = 10  # Добавим небольшой отступ между элементами

        # Создание и настройка кнопки "Назад"
        self.back_button = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.on_back_button_pressed)  # Привязываем функцию к нажатию кнопки

        # Обернем кнопку "Назад" в AnchorLayout для позиционирования в левом верхнем углу
        back_button_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        back_button_layout.add_widget(self.back_button)

        # Создание и настройка виджета, содержащего информацию о балансе и переводе
        balance_layout = GridLayout(cols=2)  # Два столбца для текста и значений

        self.balance_label = Label(text="Баланс:", size_hint=(None, None), size=(150, 50), valign='middle', halign='right')
        balance_layout.add_widget(self.balance_label)

        self.balance_value = Label(text="10.00 ETH", size_hint=(None, None), size=(150, 50), valign='middle', halign='center')
        balance_layout.add_widget(self.balance_value)

        self.transfer_label = Label(text="Перевод:", size_hint=(None, None), size=(150, 50), valign='middle', halign='right')
        balance_layout.add_widget(self.transfer_label)

        self.transfer_value = Label(text="$100.00", size_hint=(None, None), size=(150, 50), valign='middle', halign='center')
        balance_layout.add_widget(self.transfer_value)

        # Создание и настройка кнопки "Отправить"
        self.send_button = Button(text="Отправить", size_hint=(None, None), size=(100, 50), valign='middle', halign='center')

        # Обернем кнопку "Отправить" в AnchorLayout для центрирования
        send_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        send_button_layout.add_widget(self.send_button)

        # Добавляем все виджеты на страницу
        self.add_widget(back_button_layout)
        self.add_widget(balance_layout)
        self.add_widget(send_button_layout)

    # Функция обработки нажатия кнопки "Назад"
    def on_back_button_pressed(self, instance):
        print("Button 'Назад' pressed")


class CryptoWalletApp(App):
    def build(self):
        # Устанавливаем размер окна
        Window.size = (350, 600)
        return CryptoWalletPage()


# Запуск приложения
if __name__ == "__main__":
    CryptoWalletApp().run()
