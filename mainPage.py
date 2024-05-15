# import tkinter as tk
# from PIL import Image, ImageTk
#
# class CryptoWalletPage(tk.Tk):
#     def __init__(self):
#         super().__init__()
#
#         width=350
#         height=600
#         # Set the window size
#         self.geometry("350x600")
#
#         self.title("Crypto Wallet")
#         self.configure(background="white")
#
#         # Create the logo
#         self.logo = Image.open("logo.png")
#         self.logo = self.logo.resize((70, 70))
#         self.logo = ImageTk.PhotoImage(self.logo)
#         self.logo_label = tk.Label(self, image=self.logo, bg="white")
#         self.logo_label.grid(row=0, column=0, padx=0, pady=0, sticky="ne")
#
#
#         self.back_button = tk.Button(self, text="Back", height=2, width=10)
#         self.back_button.grid(row=0, column=0, padx=0, pady=10, sticky="nw")
#
#         # Create the wallet address label
#         self.wallet_address_label = tk.Label(self, text="Wallet Address: 0x1234567890123456789012345678901234567890", font=("Helvetica", 10), wraplength=300, padx=10, pady=5, bg="white")
#         self.wallet_address_label.grid(row=1, column=0, padx=10, pady=5)
#
#         # Create the balance label
#         self.balance_label = tk.Label(self, text="Balance: 10.00 ETH", font=("Helvetica", 14), wraplength=300, padx=10, pady=5, bg="white")
#         self.balance_label.grid(row=2, column=0, padx=10, pady=5)
#
#         # Create the transfer label
#         self.transfer_label = tk.Label(self, text="Transfer: $100.00", font=("Helvetica", 14), wraplength=300, padx=10, pady=5, bg="white")
#         self.transfer_label.grid(row=3, column=0, padx=10, pady=5)
#
#         # Create the send button
#         self.send_button = tk.Button(self, text="Send", height=3, width=20)
#         self.send_button.grid(row=4, column=0, padx=10, pady=5)
#
#         # Create the transaction history label
#         self.transaction_history_label = tk.Label(self, text="Transaction History:", font=("Helvetica", 14), bg="white")
#         self.transaction_history_label.grid(row=5, column=0, padx=10, pady=50)
#
#         # Create the transaction history listbox
#         self.transaction_history_listbox = tk.Listbox(self, bg="white")
#         self.transaction_history_listbox.grid(row=100, column=0, padx=10, pady=5, columnspan=2, sticky="ew")
#
#         # Add some sample transaction history
#         self.transaction_history_listbox.insert(tk.END, "Transaction 1: 5.00 ETH sent to 0x1234567890123456789012345678901234567890")
#         self.transaction_history_listbox.insert(tk.END, "Transaction 2: 2.00 ETH received from 0x1234567890123456789012345678901234567890")
#         self.transaction_history_listbox.insert(tk.END, "Transaction 3: 3.00 ETH sent to 0x1234567890123456789012345678901234567890")
#
# # Create the crypto wallet page
# crypto_wallet_page = CryptoWalletPage()
#
# # Run the Tkinter event loop
# crypto_wallet_page.mainloop()
