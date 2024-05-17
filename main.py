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


from kivymd.app import MDApp
from kivy.uix.image import Image, AsyncImage
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivymd.uix.toolbar import MDTopAppBar
from kivy.uix.floatlayout import FloatLayout


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
sm = MDScreenManager()


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
        # text_input = MDMDTextField(text='close_key', size_hint=(1, 0.2))
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

    # В классе WalletsCatalog, метод on_wallet_click

    def on_wallet_click(self, instance):
        global current_wallet
        current_wallet = get_key_on_address(instance.text)
        print(current_wallet, " On wallet")  # Убедитесь, что current_wallet устанавливается правильно
        sm.current = "cryptowalletpage"


# #######


#####

# class SendMoneyApp(MDScreen):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#         layout = MDGridLayout(cols=1, padding=10)
#         layout.add_widget(self.address_textfield)
#         layout.add_widget(self.amount_textfield)
#         if not self.add_dialog:
#             self.dialog = MDDialog(
#                 title="Private Key:",
#                 type="custom",
#                 content_cls=layout,
#
#                 buttons=[
#                     MDFillRoundFlatButton(
#                         text="SEND", on_release=self.send_button_pressed
#                     ),
#                     MDFillRoundFlatButton(
#                         text="CANCEL", on_release=self.cancel_button_pressed
#                     ),
#                 ],
#             )
#
#     def on_entry_click(self, instance, value):
#         if value:
#             if instance.text == 'Sending Address:':
#                 instance.text = ''
#
#     def on_focusout(self, instance, value):
#         if not value and instance.text.strip() == '':
#             instance.text = 'Sending Address:'
#
#     def on_entry_click_amount_sending(self, instance, value):
#         if value:
#             if instance.text == 'Amount Sending:':
#                 instance.text = ''
#
#     def on_focusout_amount_sending(self, instance, value):
#         if not value and instance.text.strip() == '':
#             instance.text = 'Amount Sending:'
#
#     def send_money(self, instance):
#         sending_address = self.entry_sending_address.text
#         amount_sending = self.entry_amount_sending.text
#         amount_commission = self.entry_amount_commission.text
#
#         if not sending_address.startswith("0x"):
#             print("not 0x")
#             return False
#
#         if len(sending_address) != 42:
#             print("not 42")
#             return False
#
#         if not all(c in "0123456789abcdefABCDEF" for c in sending_address[2:]):
#             print("not 0123456789abcdefABCDEF")
#             return False
#
#         data = {
#             "sending_address": sending_address,
#             "amount_sending": amount_sending,
#             "amount_commission": amount_commission
#         }
#
#         # Отправляем данные на сервер
#         # response = requests.post("http://example.com/send_money", data=data)
#         #
#         # # Печатаем ответ сервера
#         # print(response.text)
#         return data
#
#     def get_eth_gas_price_in_wei(self):
#         try:
#             etherscan_api_url = f"https://api.etherscan.io/api?module=gastracker&action=gasoracle&apikey=YourApiKeyToken"
#             response = requests.get(etherscan_api_url)
#
#             if response.status_code == 200:
#                 gas_price_data = response.json()
#                 if gas_price_data['status'] == '1':
#                     gas_price_in_wei = int(gas_price_data['result']['SafeGasPrice'])
#                     return gas_price_in_wei
#                 else:
#                     print("Ошибка при получении данных о цене газа:", gas_price_data['message'])
#                     return None
#             else:
#                 print("Ошибка при отправке запроса к Etherscan API")
#                 return None
#         except Exception as e:
#             print("Произошла ошибка:", e)
#             return None
#
#     def convert_gas_to_eth(self, gas_price_in_wei):
#         if gas_price_in_wei is not None:
#             gas_price_in_eth = gas_price_in_wei / 10 ** 9 * 21000  # Поменять на 200000 в Arb
#             gas_price_in_eth = round(gas_price_in_eth, 7)
#             formatted_gas_price = "{:.7f}".format(gas_price_in_eth)
#             print(f"Текущая средняя цена газа: {formatted_gas_price} ETH")
#             self.entry_amount_commission.text = "Fee: " + str(formatted_gas_price) + " ETH"
#
#     def perform_actions(self, dt):
#         gas_price_in_wei = self.get_eth_gas_price_in_wei()
#         self.convert_gas_to_eth(gas_price_in_wei)
#         Clock.schedule_once(self.perform_actions, 10)  # Вызываем perform_actions() каждые 5 секунд


class CryptoWalletPage(MDScreen):
    dialog = None
    amount_textfield = None
    address_textfield = None
    balance_value = None
    transfer_value = None
    test = CryptoWork()
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.address_textfield = MDTextField(hint_text="Enter address")
        self.amount_textfield = MDTextField(hint_text="Enter amount")

        main_layout = MDGridLayout(cols=1, padding=10, spacing=10)

        toolbar = MDTopAppBar(title="DronozavRR")
        toolbar.left_action_items = [
            ["arrow-left", lambda x: self.on_back_button_pressed()],
             ["email", lambda x: self.on_send_press()]
        ]
        main_layout.add_widget(toolbar)

        balance_layout = MDGridLayout(cols=1, padding=('170px', '0pd'))  # Два столбца для текста и значений

        self.balance_value = MDLabel( size_hint=(None, None), size=(150, 50), valign='middle',
                                halign='center', padding=('50pd'))
        balance_layout.add_widget(self.balance_value)

        self.transfer_value = MDLabel( size_hint=(None, None), size=(150, 50), valign='middle',
                                 halign='center')
        balance_layout.add_widget(self.transfer_value)

        main_layout.add_widget(balance_layout)
        self.add_widget(main_layout)




    def on_back_button_pressed(self):
        print("Button 'Назад' pressed")
        sm.current = "walletcatalog"

    def on_send_press(self):
        print("Button 'Назад' pressed")

        layout = MDGridLayout(cols=1, padding=10)
        layout.add_widget(self.address_textfield)
        layout.add_widget(self.amount_textfield)
        if not self.dialog:
            self.dialog = MDDialog(
                title="Private Key:",
                type="custom",
                content_cls=layout,

                buttons=[
                    MDFillRoundFlatButton(
                        text="SEND", on_release=self.send_button_in_dialog
                    ),
                    MDFillRoundFlatButton(
                        text="CANCEL", on_release=self.cancel_button_in_dialog
                    ),
                ],
            )
        self.dialog.update_height()
        self.dialog.open()

    def send_button_in_dialog(self, instance):
        self.test.send_eth(current_wallet, self.address_textfield.text, self.amount_textfield.text)
        self.dialog.dismiss()
        self.dialog = None
    def cancel_button_in_dialog(self, instance):
        self.dialog.dismiss()
        self.dialog = None
    # Обновление размеров и положения прямоугольника при изменении размера виджета
    def on_enter(self):

        global current_wallet
        if current_wallet != "":
            print(current_wallet, "on enter")
            self.balance_value.text = f'{"{:.10f}".format(self.test.get_eth_balance_from_wallet(current_wallet, "https://arbitrum.drpc.org"))} ETH'
            self.transfer_value.text = f'{"{:.10f}".format(float(self.test.get_eth_price_from_bybit()) * float(self.test.get_eth_balance_from_wallet(current_wallet, "https://arbitrum.drpc.org")))} $'
            print(self.balance_value.text)


class CryptoWalletApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Green"

        sm.add_widget(WalletsCatalog(name="walletcatalog"))
        sm.add_widget(CryptoWalletPage(name="cryptowalletpage"))

        sm.current = "walletcatalog"

        return sm

# Запуск приложения
if __name__ == "__main__":
    CryptoWalletApp().run()




#############
