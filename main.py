from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.core.window import Window
from WorkWithDB import create_table, transfer_in_array, add_new_key, dell_key, delete_all, transfer_in_array_address, \
    get_key_on_address, get_address_on_key
import requests
from web3 import Web3

Window.size = (350, 600)
Window.clearcolor = (10 / 255, 10 / 255, 10 / 255, 1)
Window.title = "MultiWallet"

create_table()
global wallets
global private_keys
private_keys = transfer_in_array()
print(private_keys)
wallets = transfer_in_array_address()
global layout
global popup_add_private_key
w3 = Web3(Web3.HTTPProvider("https://arbitrum.drpc.org"))
current_wallet = str()


class CryptoWork:
    def get_eth_price_from_bybit(self):
        response = requests.get('https://api.bybit.com/derivatives/v3/public/tickers?symbol=ETHUSDT&limit=1')
        return (response.json()['result']['list'][0]['lastPrice'])

    def get_eth_balance_from_wallet(self, private_key, rpc):
        w3 = Web3(Web3.HTTPProvider(rpc))
        account = w3.eth.account.from_key(private_key)
        address = account.address
        balance_wei = w3.eth.get_balance(address)
        balance_eth = w3.from_wei(balance_wei, 'ether')  # Преобразование из wei в эфиры
        return balance_eth

    def get_address_from_private_key(self, private_key, rpc):
        w3 = Web3(Web3.HTTPProvider(rpc))
        account = w3.eth.account.from_key(private_key)
        address = account.address
        return address

    def send_eth(self, key_from, address_to, eth_amount):
        web3 = Web3(Web3.HTTPProvider("https://arbitrum.drpc.org"))
        account = web3.eth.account.from_key(private_key=key_from)
        nonce = web3.eth.get_transaction_count(account.address, 'pending')
        gas_estimate = web3.eth.estimate_gas({
            'to': address_to,
            'value': web3.to_wei(eth_amount, 'ether'),
        })

        transaction = {
            'nonce': nonce,  # Добавляем nonce сюда
            'to': address_to,
            'value': web3.to_wei(eth_amount, 'ether'),
            'gas': gas_estimate,
            'gasPrice': web3.eth.gas_price,
        }

        print(web3.from_wei(transaction['gas'], 'ether'))
        signed_txn = web3.eth.account.sign_transaction(transaction, key_from)

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        return txn_hash.hex()

    # scan - example - etherscan,arbiscan
    # address - кошелек для которого нужно сканить
    # api_key - брал для арбитрума, для эфира не тестил
    def get_transactions_history(self, scan, address, api_key='272WETQQ4WRRUVBINPZRXBWPRE2G4G4SE8'):
        response = requests.get(
            f'https://api.{scan}.io/api?module=account&action=txlist&address={address}&startblock=0&endblock=latest&sort=asc&page=1&offset=10&apikey={api_key}')
        # потом обработать транзакции
        return response.json()['result']


class WalletsCatalog(App):
    def __init__(self, **kwargs):
        super(WalletsCatalog, self).__init__(**kwargs)
        self.wallet_input = str()
        self.popup_add_private_key = None
        self.wallet_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.wallet_layout.bind(minimum_height=self.wallet_layout.setter('height'))

    def refresh_table(self):  # выход - из бд тянуть строчки с адресами и вставлять
        self.wallet_layout.clear_widgets()
        w3 = Web3(Web3.HTTPProvider("https://arbitrum.drpc.org"))

        print(f"ключи - {private_keys}")
        for wallet in wallets:
            button = Button(text=wallet, size_hint=(1, None), height=40,
                            background_color=(50 / 255, 205 / 255, 50 / 255, 1))
            button.bind(on_press=self.on_wallet_click)
            self.wallet_layout.add_widget(button)

    def create_popup_add_private_key(self):
        content = BoxLayout(orientation='vertical', spacing=10)
        text_input_layout = AnchorLayout(anchor_y='top')
        content.add_widget(text_input_layout)
        text_input = TextInput(text='close_key', size_hint=(1, 0.2))
        text_input.bind(text=self.on_text_input)
        text_input_layout.add_widget(text_input)
        button_add = Button(text="ADD", size_hint=(1, 0.2))
        button_add.bind(on_press=self.on_add_button_press)
        content.add_widget(button_add)
        self.popup_add_private_key = Popup(title='Enter close key',
                                           size_hint=(0.7, 0.5), content=content)

    def on_text_input(self, instance, value):
        self.wallet_input = value

    def on_add_button_press(self, instance):
        try:
            try:
                account = w3.eth.account.from_key(self.wallet_input)
            except Exception as e:
                print("Ошибка при создании аккаунта 1 :", e)
            print(f'1 step {self.wallet_input}')
            try:
                add_new_key(self.wallet_input)
            except Exception as e:
                print("Ошибка при создании аккаунта2 :", e)
            if (account and account.address):
                wallets.append(account.address)
                private_keys.append(self.wallet_input)
                print(f'2 step adr - {account.address}')
                print(f'2 step key -  {self.wallet_input}')
                try:
                    self.refresh_table()
                except Exception as e:
                    print("Ошибка при создании аккаунта3:", e)

                self.popup_add_private_key.dismiss()
        except Exception as e:
            print("Ошибка при создании аккаунта:", e)

    def build(self):
        main_layout = BoxLayout(spacing=10, orientation='vertical')
        self.refresh_table()
        scrollview = ScrollView(size_hint=(1, 7), size=(Window.width, Window.height))
        scrollview.add_widget(self.wallet_layout)
        main_layout.add_widget(scrollview)
        bottom_layout = BoxLayout(spacing=10, orientation='horizontal')
        button_add = Button(text="ADD")
        button_add.bind(on_press=self.show_popup_add_private_key)
        bottom_layout.add_widget(button_add)
        button_dell = Button(text="DELL")
        button_dell.bind(on_press=self.on_dell_button_press)
        bottom_layout.add_widget(button_dell)
        main_layout.add_widget(bottom_layout)
        return main_layout

    def show_popup_add_private_key(self, instance):
        self.create_popup_add_private_key()
        self.popup_add_private_key.open()

    def on_dell_button_press(self, instance):
        print('')

    def on_wallet_click(self, instance):
        global current_wallet
        current_wallet = get_key_on_address(instance.text)
        print(current_wallet)
        self.stop()
        CryptoWalletApp().run()


class CryptoWalletPage(GridLayout):
    MainApp = None

    def __init__(self, App, **kwargs):
        self.MainApp = App
        super().__init__(**kwargs)
        self.cols = 1  # Один столбец для всех элементов
        self.padding = 10
        self.spacing = 10  # Добавим небольшой отступ между элементами
        test = CryptoWork()
        # Создание и настройка кнопки "Назад"
        self.back_button = Button(text="Назад", size_hint=(None, None), size=(100, 50))
        self.back_button.bind(on_press=self.on_back_button_pressed)  # Привязываем функцию к нажатию кнопки

        # Обернем кнопку "Назад" в AnchorLayout для позиционирования в левом верхнем углу
        back_button_layout = AnchorLayout(anchor_x='left', anchor_y='top')
        back_button_layout.add_widget(self.back_button)

        # Создание и настройка виджета, содержащего информацию о балансе и переводе
        balance_layout = GridLayout(cols=1)  # Два столбца для текста и значений

        self.balance_label = Label(
            text=f"{'{:.10f}'.format(test.get_eth_balance_from_wallet(current_wallet, 'https://arbitrum.drpc.org'))} ETH",
            size_hint=(None, None), size=(150, 50), valign='middle',
            halign='center')
        balance_layout.add_widget(self.balance_label)

        get_balance = (float(test.get_eth_balance_from_wallet(current_wallet, "https://arbitrum.drpc.org")) * float(test.get_eth_price_from_bybit()))

        self.transfer_label = Label(
            text=f"{get_balance}$",
            size_hint=(None, None), size=(150, 50), valign='middle',
            halign='auto')
        balance_layout.add_widget(self.transfer_label)

        # Создание и настройка кнопки "Отправить"
        self.send_button = Button(text="Отправить", size_hint=(None, None), size=(100, 50), valign='middle',
                                  halign='center')

        # Обернем кнопку "Отправить" в AnchorLayout для центрирования
        send_button_layout = AnchorLayout(anchor_x='center', anchor_y='center')
        send_button_layout.add_widget(self.send_button)

        # Добавляем все виджеты на страницу
        self.add_widget(back_button_layout)
        self.add_widget(balance_layout)
        self.add_widget(send_button_layout)

    # Функция обработки нажатия кнопки "Назад"
    def on_back_button_pressed(self, instance):
        self.MainApp.stop()
        WalletsCatalog().run()
        print("Button 'Назад' pressed")


class CryptoWalletApp(App):
    def build(self):
        Window.size = (350, 600)
        return CryptoWalletPage(self)


if __name__ == "__main__":
    WalletsCatalog().run()