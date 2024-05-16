from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDFillRoundFlatButton, MDTextButton
from kivymd.uix.anchorlayout import MDAnchorLayout
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDList, OneLineListItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.toolbar import MDTopAppBar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.selectioncontrol import MDCheckbox

from WorkWithDB import create_table, transfer_in_array, add_new_key, dell_key, delete_all, transfer_in_array_address, \
    get_key_on_address, get_address_on_key
import requests
from web3 import Web3

width = 350
height = 600

##########

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


class WalletsCatalog(MDScreen):
    delete_dialog = None
    add_dialog = None
    key_input = None
    key_text_field = None
    def __init__(self, **kwargs):
        super(WalletsCatalog, self).__init__(**kwargs)
        self.key_text_field = MDTextField(hint_text="Enter Key")
        self.wallet_input = str()
        self.popup_add_private_key = None
        self.wallet_layout = MDGridLayout(cols=1, spacing=10, size_hint_y=None)
        self.wallet_layout.bind(minimum_height=self.wallet_layout.setter('height'))

        toolbar = MDTopAppBar(title="DronozavRR")


        toolbar.right_action_items = [
            ["plus", lambda x: self.show_dialog_add()],
            ["trash-can-outline", lambda x: self.show_dialog_delete()]
        ]

        main_layout = MDBoxLayout(spacing=10, orientation='vertical')
        main_layout.add_widget(toolbar)
        self.refresh_table()
        scrollview = MDScrollView(size_hint=(1, 7), size=(width, height))
        scrollview.add_widget(self.wallet_layout)
        main_layout.add_widget(scrollview)
        # bottom_layout = MDBoxLayout(spacing=10, orientation='horizontal')
        # button_add = Button(text="ADD")
        # button_add = MDFillRoundFlatButton(MDTextButton(text="Add"), size_hint=(None, None), size=(120, 60),
        #                                    valign='center',
        #                                    halign='center')
        # bottom_layout.add_widget(button_add)
        # # button_dell = Button(text="DELL")
        # button_dell = MDFillRoundFlatButton(MDTextButton(text="Dell"), size_hint=(None, None), size=(120, 60),
        #                                     valign='center',
        #                                     halign='center')
        # button_dell.bind(on_press=self.on_dell_button_press)
        # bottom_layout.add_widget(button_dell)
        # main_layout.add_widget(bottom_layout)

        self.add_widget(main_layout)

    def refresh_table(self):  # выход - из бд тянуть строчки с адресами и вставлять
        self.wallet_layout.clear_widgets()
        w3 = Web3(Web3.HTTPProvider("https://arbitrum.drpc.org"))

        print(f"ключи - {private_keys}")
        for wallet in wallets:
            # button = MDButton(text=wallet, size_hint=(1, None), height=40,
            #                 background_color=(50 / 255, 205 / 255, 50 / 255, 1))
            item = OneLineListItem(text=wallet)

            item.bind(on_press=self.on_wallet_click)
            self.wallet_layout.add_widget(item)

    def create_popup_add_private_key(self):
        content = MDBoxLayout(orientation='vertical', spacing=10)
        text_input_layout = MDAnchorLayout(anchor_y='top')
        content.add_widget(text_input_layout)
        # text_input = MDTextInput(text='close_key', size_hint=(1, 0.2))
        # text_input.bind(text=self.on_text_input)
        # text_input_layout.add_widget(text_input)
        # button_add = MDButton(text="ADD", size_hint=(1, 0.2))
        # button_add.bind(on_press=self.on_add_button_press)
        # content.add_widget(button_add)
        # self.popup_add_private_key = MDPopup(title='Enter close key',
        #                                    size_hint=(0.7, 0.5), content=content)

    def on_text_input(self, instance, value):
        self.wallet_input = value

    def on_add_button_press(self, instance):
        try:

            try:
                account = w3.eth.account.from_key(self.wallet_input)
            except Exception as e:
                Snackbar(text=f"Error - {e}").show()
                print("Ошибка при создании аккаунта 1 :", e)
            print(f'1 step {self.wallet_input}')
            try:
                add_new_key(self.wallet_input)
            except Exception as e:
                Snackbar(text=f"Error - {e}").show()
                print("Ошибка при создании аккаунта2 :", e)
            if (account and account.address):
                wallets.append(account.address)
                private_keys.append(self.wallet_input)
                print(f'2 step adr - {account.address}')
                print(f'2 step key -  {self.wallet_input}')
                try:
                    self.refresh_table()
                except Exception as e:
                    Snackbar(text=f"Error - {e}").show()
                    print("Ошибка при создании аккаунта3:", e)
        except Exception as e:
            Snackbar(text=f"Error - {e}").show()
            print("Ошибка при создании аккаунта:", e)

    def show_dialog_add(self):
        self.create_popup_add_private_key()

        if not self.add_dialog:
            self.add_dialog = MDDialog(
                title="Private Key:",
                type="custom",
                content_cls=self.key_text_field,

                buttons=[
                    MDFillRoundFlatButton(
                        text="OK", on_release=self.ok_button_pressed_for_add
                    ),
                    MDFillRoundFlatButton(
                        text="CANCEL", on_release=self.cancel_button_pressed
                    ),
                ],

            )
        self.add_dialog.open()

    def show_dialog_delete(self):
        if len(wallets) == 0:
            return
        if not self.delete_dialog:

            scroll_view = MDScrollView()
            checkbox_layout = MDGridLayout(cols=1, spacing=10, size_hint_y=None)

            for wallet in wallets:
                print(wallet)
                CheckBoxLayout = MDGridLayout(cols=2)
                checkbox = MDCheckbox(text=wallet, active=False, size_hint=(None, None),adaptive_height=True)
                CheckBox_Label = MDLabel(text=wallet)
                CheckBoxLayout.add_widget(checkbox)
                CheckBoxLayout.add_widget(CheckBox_Label)
                checkbox_layout.add_widget(CheckBoxLayout)
            scroll_view.add_widget(checkbox_layout)

            self.delete_dialog = MDDialog(
                title="Need for delete",
                type="custom",
                content_cls=scroll_view,
                buttons=[
                    MDFillRoundFlatButton(
                        text="OK", on_release=self.ok_button_pressed_for_delete
                    ),
                    MDFillRoundFlatButton(
                        text="CANCEL", on_release=self.cancel_button_pressed_for_delete
                    ),
                ],

            )

        self.delete_dialog.update_height()
        self.delete_dialog.open()
    def ok_button_pressed_for_delete(self, instance):
        mg_gl = self.delete_dialog.content_cls
        for grid in mg_gl.children[0].children: #grid
            if grid.children[1].active == False:
                continue
            select = grid.children[0].text
            dell_key(get_key_on_address(select))
        global private_keys
        private_keys = transfer_in_array()
        global wallets
        wallets = transfer_in_array_address()
        self.refresh_table()
        print(instance.text)
        self.delete_dialog.dismiss()
        self.delete_dialog = None

    def ok_button_pressed_for_add(self, instance):

        self.key_input = self.key_text_field.text
        self.key_text_field.text= ""

        try:
            try:
                account = w3.eth.account.from_key(self.key_input)
            except Exception as e:
                print("Ошибка при создании аккаунта 1 :", e)
            try:
                add_new_key(self.key_input)
            except Exception as e:
                print("Ошибка при создании аккаунта2 :", e)
            if (account and account.address):
                wallets.append(account.address)
                private_keys.append(self.key_input)
                try:
                    self.refresh_table()
                except Exception as e:
                    print("Ошибка при создании аккаунта3:", e)
        except Exception as e:
            print("Ошибка при создании аккаунта:", e)

        self.add_dialog.dismiss()

    def cancel_button_pressed(self, instance):
        # Реализуйте логику для нажатия кнопки "CANCEL" здесь
        self.add_dialog.dismiss()  # Закрыть диалоговое окно после выполнения действий
        self.delete_dialog = None
    def cancel_button_pressed_for_delete(self, instance):
        # Реализуйте логику для нажатия кнопки "CANCEL" здесь
        self.delete_dialog.dismiss()  # Закрыть диалоговое окно после выполнения действий
        self.delete_dialog = None



    def on_wallet_click(self, instance):
        global current_wallet
        current_wallet = get_key_on_address(instance.text)
        print(current_wallet)
        self.stop()
        CryptoWalletApp().run()


# #######

class CryptoWalletPage(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        main_layout = MDGridLayout(cols=1, padding=10, spacing=10)

        # Создание и настройка кнопки "Назад"
        # .back_button = Button(text="Назад", size_hint=(None, None), size=(100, 50), background_color=(1, 0.5, 0, 1))
        back_button = MDFillRoundFlatButton(MDTextButton(text="Back"), size_hint=(None, None), size=(100, 50))
        back_button.bind(on_press=self.on_back_button_pressed)  # Привязываем функцию к нажатию кнопки

        # Обернем кнопку "Назад" в AnchorLayout для позиционирования в левом верхнем углу
        back_button_layout = MDAnchorLayout(anchor_x='left', anchor_y='top')
        back_button_layout.add_widget(back_button)

        # Создание и настройка виджета, содержащего информацию о балансе и переводе
        balance_layout = MDGridLayout(cols=1, padding=('170px', '0pd'))  # Два столбца для текста и значений

        balance_value = MDLabel(text="10.00 ETH", size_hint=(None, None), size=(150, 50), valign='middle',
                                halign='center', padding=('50pd'))
        balance_layout.add_widget(balance_value)

        transfer_value = MDLabel(text="$100.00", size_hint=(None, None), size=(150, 50), valign='middle',
                                 halign='center')
        balance_layout.add_widget(transfer_value)

        # Создание и настройка кнопки "Отправить"
        send_button = MDFillRoundFlatButton(MDTextButton(text="Send"), size_hint=(None, None), size=(120, 60),
                                            valign='center',
                                            halign='center')

        # Обернем кнопку "Отправить" в AnchorLayout для центрирования
        send_button_layout = MDAnchorLayout(anchor_x='center', anchor_y='center')
        send_button_layout.add_widget(send_button)

        # Добавляем все виджеты на страницу
        main_layout.add_widget(back_button_layout)
        main_layout.add_widget(balance_layout)
        main_layout.add_widget(send_button_layout)
        self.add_widget(main_layout)

    # Функция обработки нажатия кнопки "Назад"
    def on_back_button_pressed(self, instance):
        print("Button 'Назад' pressed")

    # Обновление размеров и положения прямоугольника при изменении размера виджета


class CryptoWalletApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"
        sm = MDScreenManager()
        sm.add_widget(WalletsCatalog(name="walletcatalog"))
        sm.add_widget(CryptoWalletPage(name="cryptowalletpage"))
        sm.current = "walletcatalog"

        return sm


# Запуск приложения
if __name__ == "__main__":
    CryptoWalletApp().run()
