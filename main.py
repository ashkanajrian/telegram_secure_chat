from telethon import TelegramClient, events
import asyncio
import os
from tqdm.asyncio import tqdm

api_id = 'YOUR_API_ID'
api_hash = 'YOUR_API_HASH'

class TelegramSecretMessage:
    def __init__(self):
        self.client = None
        self.loop = asyncio.get_event_loop()

    async def start_client(self, phone):
        self.client = TelegramClient('session_name', api_id, api_hash)
        await self.client.connect()
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(phone)
            code = input('Enter the code you received: ')
            await self.client.sign_in(phone, code)

    async def get_username(self):
        me = await self.client.get_me()
        return me.username

    def xor_cipher(self, message, key):
        return ''.join(chr(ord(c) ^ ord(k)) for c, k in zip(message, key * len(message)))

    async def send_secret_message(self, message, key, receiver_username):
        receiver = await self.client.get_entity(receiver_username)
        encoded_message = self.xor_cipher(message, key)
        secret_message = f'This is a secret message: {encoded_message}'
        await self.client.send_message(receiver, secret_message)
        print("Secret message sent!")

    async def receive_secret_message(self):
        specific_sender = input("Do you want to check messages from a particular username? (yes/no): ").strip().lower()

        if specific_sender == 'yes':
            username = input("Enter the username: ")
            try:
                sender = await self.client.get_entity(username)
                sender_id = sender.id

                key = input('Enter the key: ')

                async for message in self.client.iter_messages(sender_id):
                    if message.text and message.text.startswith("This is a secret message:"):
                        encoded_message = message.text.replace('This is a secret message: ', '')
                        decoded_message = self.xor_cipher(encoded_message, key)
                        print(f'Decoded message from {username}: {decoded_message}')
                        return

                print('No secret messages found from this user.')
            except:
                print('User not found or you have no messages from this user.')
        else:
            senders = {}

            print('Searching for secret messages...')
            
            async for dialog in self.client.iter_dialogs():
                if dialog.is_user:
                    async for message in tqdm(self.client.iter_messages(dialog.id), desc=f"Checking messages in {dialog.name}"):
                        if message.text and message.text.startswith("This is a secret message:"):
                            senders[dialog.name] = dialog.id
                            break  # We only need the first secret message to know the user sent one

            if not senders:
                print('There are no secret messages for you.')
                return

            print('Secret messages from:')
            for i, sender in enumerate(senders.keys(), 1):
                print(f'{i}. {sender}')

            choice = int(input('Choose a sender by number: ')) - 1
            chosen_sender = list(senders.keys())[choice]
            sender_id = senders[chosen_sender]

            key = input('Enter the key: ')
            
            async for message in self.client.iter_messages(sender_id):
                if message.text and message.text.startswith("This is a secret message:"):
                    encoded_message = message.text.replace('This is a secret message: ', '')
                    decoded_message = self.xor_cipher(encoded_message, key)
                    print(f'Decoded message from {chosen_sender}: {decoded_message}')
                    break

    def run(self):
        phone = input('Enter your phone number: ')
        self.loop.run_until_complete(self.start_client(phone))
        username = self.loop.run_until_complete(self.get_username())
        print(f'Successfully signed in! Your username is {username}')

        role = input('Are you a sender or receiver of a secret message? (sender/receiver): ').strip().lower()

        if role == 'sender':
            message = input('Enter the secret message: ')
            key = input('Enter the key: ')
            receiver_username = input('Enter the receiver\'s username: ')
            self.loop.run_until_complete(self.send_secret_message(message, key, receiver_username))
        elif role == 'receiver':
            self.loop.run_until_complete(self.receive_secret_message())
        else:
            print('Invalid role specified.')

if __name__ == "__main__":
    telegram_secret_message = TelegramSecretMessage()
    telegram_secret_message.run()
