# Telegram Secure Chat

This repository contains a simple Python script for sending and receiving secret messages on Telegram using the Telethon library. This project is a part of a larger project with the same purpose of secure communication.

## Features

- **Send Secret Messages**: Encrypt a message using a simple XOR cipher and send it to a specified Telegram user.
- **Receive Secret Messages**: Decrypt received secret messages from specific or all Telegram users.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ashkanajrian/telegram_secure_chat.git
    cd telegram_secure_chat
    ```

2. **Install the required packages**:
    ```sh
    pip install telethon tqdm
    ```

## Usage

1. **Run the script**:
    ```sh
    python main.py
    ```

2. **Sign in**:
    - Enter your phone number associated with your Telegram account.
    - Enter the verification code received on your Telegram.

3. **Choose your role**:
    - **Sender**: Enter the secret message, a key for encryption, and the receiver's username.
    - **Receiver**: Choose to check messages from a specific user or all users, and provide the decryption key when prompted.

## How It Works

- **Encryption**: The script uses an XOR cipher to encrypt the message with a provided key.
- **Decryption**: The same XOR cipher is used to decrypt received messages with the provided key.

## Example

### Sending a Secret Message
```plaintext
Enter your phone number: +123456789
Enter the code you received: 12345
Successfully signed in! Your username is exampleuser
Are you a sender or receiver of a secret message? (sender/receiver): sender
Enter the secret message: Hello, this is a secret!
Enter the key: mysecretkey
Enter the receiver's username: friendusername
Secret message sent!
```
### Receiving a Secret Message
```plaintext
Enter your phone number: +123456789
Enter the code you received: 12345
Successfully signed in! Your username is exampleuser
Are you a sender or receiver of a secret message? (sender/receiver): receiver
Do you want to check messages from a particular username? (yes/no): yes
Enter the username: friendusername
Enter the key: mysecretkey
Decoded message from friendusername: Hello, this is a secret!