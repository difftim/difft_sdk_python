# Difft-sdk-python
## Python Version
python requires >= 3.6
## Interface
* send_message
* get_account_by_email
* get_account_by_wuid
* get_group_by_botid
* upload_attachment
* download_attachment

## Command-line
DiffClient provide a command-line tool `difft-cli`, before using `difft-cli`, you should create a configure file `.difft.cfg` in current directory or HOME directory, e.g
```cfg
[base]
appid=f250845b274f4a5c01
secret=w0m6nTOIIspxR0wmGJbEvAOfNnyf
botid=+60000
host=https://openapi.test.difft.org
``` 
Also, you can provide the above configuration in command line, e.g
```shell
difft-cli --appid f250845b274f4a5c01 --secret w0m6nTOIIspxR0wmGJbEvAOfNnyf --botid +60000 --host https://openapi.test.difft.org sendmsg -user +76459652574 -msg "hello world"
```

### Example
After creating configure file `.difft.cfg` in current directory or HOME directory, you can simply use `difft-cli` as below:
```shell
# send message to user
difft-cli sendmsg -user +76459652574 -msg "hello world"

# send message to group
difft-cli sendmsg -group a9de6b3ae8c8456d888c4532b487e822 -msg "hello world"

# send attachment
difft-cli sendmsg -user +76459652574 -att test.txt

# send image 
difft-cli sendmsg -user +76459652574 -att test.jpg -att-type image/jpeg

# get account
difft-cli account -email xxx1@xxx,xxx2@xxxx

# get group by botid
difft-cli group -bot +60000

# send card message to user
difft-cli sendcard -user +76459652574 -id 1111 -content "### Hello"
# send card message to group
difft-cli sendcard -group 8d351378d2664c5aa4893b4d530c61db -id 1111 -content "### Hello"
# or provide creator and timestamp
difft-cli sendcard -user +76459652574 -id 1111 -content "### Hello" -creator +76459652574 -ts 1111111111

```

## Install from python package
```shell
pip install difft
```

## Install from source code
```shell
make install
```

## Using as a python module
### Send message
```python
import time
from difft.client import DifftClient
from difft.message import MessageRequestBuilder

APP_ID = "f250845b274f4a5c01"
APP_SECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID="+60000"

# using testing environment by default
difft_client = DifftClient(APP_ID, APP_SECRET)
# production environment
# difft_client = DifftClient(APP_ID, APP_SECRET, "https://xxx.com")

# send message to users
message = MessageRequestBuilder()                     \
            .sender(BOT_ID)                           \
            .to_user(["+76459652574"])                \
            .message("hello, this is a test message") \
            .timestamp_now()                          \
            .build()

difft_client.send_message(message)

# sleep 1 second due to server-end frequency limit
time.sleep(1)

# send message to group
# groupid can be retrieved from api getGroupByBotId
# or command-line difft-cli group
# or base64 decode the group invitation link in wea
message = MessageRequestBuilder()                         \
            .sender(BOT_ID)                               \
            .to_group("a9de6b3ae8c8456d888c4532b487e822") \
            .message("hello, this is a test message")     \
            .timestamp_now()                              \
            .build()
difft_client.send_message(message)

# send message to group and @someone
# make sure message body include text `@username_you_want_to_at`
# e.g. Allen(+76459652574)
message = MessageRequestBuilder()                         \
            .sender(BOT_ID)                               \
            .to_group("a9de6b3ae8c8456d888c4532b487e822") \
            .message("@Allen hello, this is a test message")     \
            .at_user(["+76459652574"])                    \
            .timestamp_now()                              \
            .build()
difft_client.send_message(message)

# send quote message
message = MessageRequestBuilder()                         \
            .sender(BOT_ID)                               \
            .to_group("a9de6b3ae8c8456d888c4532b487e822") \
            .message("hello, this is a test message")     \
            .quote("refID", "text")                       \
            .timestamp_now()                              \
            .build()
difft_client.send_message(message)
```
### Recall message

```python
import time

message = MessageRequestBuilder()                          \
    .sender(BOT_ID)                                        \
    .to_user(["+76459652574"])                             \
    .message("hello, this is a test message")              \
    .timestamp_now()                                       \
    .build()

difft_client.send_message(message)

time.sleep(10)

recall_message = MessageRequestBuilder()                   \
    .sender(BOT_ID)                                        \
    .to_user(["+76459652574"])                             \
    .recall(BOT_ID, message.get('timestamp'))              \
    .timestamp_now()                                       \
    .build()

difft_client.send_message(recall_message)
```
### Send attachment
```python
import time
from difft.client import DifftClient
from difft.message import MessageRequestBuilder
from difft.attachment import AttachmentBuilder

APP_ID = "f250845b274f4a5c01"
APP_SECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID="+60000"

# using testing environment by default
difft_client = DifftClient(APP_ID, APP_SECRET)
# production environment
# difft_client = DifftClient(APP_ID, APP_SECRET, "https://xxx.com")

# 1. first, upload attachment
plain_attachment = utils.random_str(1024).encode("utf-8")
uploaded_attachment = difft_client.upload_attachment("+60000", [], ["+76459652574"], plain_attachment) 

# 2. second, construct attachment info
attachment = AttachmentBuilder()\
                .authorize_id(uploaded_attachment.get("authorizeId"))   \
                .key(uploaded_attachment.get("key"))                    \
                .file_size(uploaded_attachment.get("fileSize"))         \
                .file_name("test.txt")                                  \
                .digest(uploaded_attachment.get("cipherHash"))          \
                .build()

# 3. third, send message with attachment
message = MessageRequestBuilder()                           \
            .sender("+60000")                               \
            .to_group("6b1f86fc04264390bdf4468a59b93ef7")   \
            .message("hello, this is a test message")       \
            .at_user(["+76459652574"])                      \
            .attachment(attachment)                         \
            .timestamp_now()                                \
            .build()
difft_client.send_message(message)
```
Read from file
```python
with open("attachment.txt", "r") as f:
    plaintext = f.read()
plaintext = plaintext.encode("utf-8")
uploaded_attachment = difft_client.upload_attachment("+60000", [], ["+76459652574"], plaintext)
attachment = AttachmentBuilder() \
    .authorize_id(uploaded_attachment.get("authorizeId")) \
    .key(uploaded_attachment.get("key")) \
    .file_size(uploaded_attachment.get("fileSize")) \
    .file_name("test.txt") \
    .digest(uploaded_attachment.get("cipherHash")) \
    .build()
message = MessageRequestBuilder() \
    .sender("+60000") \
    .to_user(["+76459652574"])\
    .message("hello, this is a test message") \
    .attachment(attachment) \
    .timestamp_now() \
    .build()
difft_client.send_message(message)
```
### Send Markdown/card
Currently supported types are [type](mdtype.txt):
```python
from difft.client import DifftClient
from difft.message import MessageRequestBuilder
from difft.attachment import AttachmentBuilder

APP_ID = "f250845b274f4a5c01"
APP_SECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID="+60000"

# using testing environment by default
difft_client = DifftClient(APP_ID, APP_SECRET)
# production environment
# difft_client = DifftClient(APP_ID, APP_SECRET, "https://xxx.com")

# send message 
message = MessageRequestBuilder() \
            .sender("+21112") \
            .to_user(["+70985684427"]) \
            .card(APPID, "1111", "### header") \
            .timestamp_now() \
            .build()
difft_client.send_message(message)
```
### Send image
```python
import time
from difft.client import DifftClient
from difft.message import MessageRequestBuilder
from difft.attachment import AttachmentBuilder

APP_ID = "f250845b274f4a5c01"
APP_SECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"
BOT_ID="+60000"

# using testing environment by default
difft_client = DifftClient(APP_ID, APP_SECRET)
# production environment
# difft_client = DifftClient(APP_ID, APP_SECRET, "https://xxx.com")

# 1. first, upload img
with open("{/path/to/img}", "rb") as f:
    img = f.read()
uploaded_img = difft_client.upload_attachment("+60000", [], ["+76459652574"], img) 

# 2. second, construct attachment info
# content_type: depend on img extention
attachment = AttachmentBuilder()\
                .authorize_id(uploaded_img.get("authorizeId"))   \
                .key(uploaded_img.get("key"))                    \
                .file_size(uploaded_img.get("fileSize"))         \
                .file_name("test.jpg")                           \
                .content_type("image/jpeg")                      \
                .digest(uploaded_img.get("cipherHash"))          \
                .build()

# 3. third, send message with attachment
message = MessageRequestBuilder()                           \
            .sender("+60000")                               \
            .to_group("6b1f86fc04264390bdf4468a59b93ef7")   \
            .at_user(["+76459652574"])                      \
            .attachment(attachment)                         \
            .timestamp_now()                                \
            .build()
difft_client.send_message(message)
```
### Get Account info
```python
difft_client.get_account_by_email("xxx@xxx")
# get multiple account info by email
difft_client.get_account_by_email("xxx@xxx,xxx@xxx")


difft_client.get_account_by_wuid("xxx")
# get multiple account info by wuid
difft_client.get_account_by_wuid("xxxx,xxx")

# get account email
param = dict(wuid="xxx", operator="xxx")
difft_client.get_account(param)

```
### Get Group info
```python
difft_client.get_group_by_botid("xxx")
```
### Callback
1. https webhook
2. websocket
***websocket和callback(webhook)只能二选一***.  

***if you turn on websocket, then the webhook stop working.***


#### Websocket example
```python
APPID = "f250845b274f4a5c01"
APPSECRET = "w0m6nTOIIspxR0wmGJbEvAOfNnyf"

difft_client = DifftClient(APPID, APPSECRET)

def customized_handler(msg):
    # skip type RECEIPT
    if msg.get('type')=='TEXT':
        logging.info('customized handler in')
        logging.info(msg.get('msg').get('body'))
        logging.info('customized handler out')
        
        message = MessageRequestBuilder() \
                .sender("+60000")          \
                .to_user([msg.get('src')]) \
                .message(msg.get('msg').get('body')) \
                .build()
        difft_client.send_message(message)

# testing env
listener = DifftWsListener(APPID, APPSECRET)
# prod env
# listener = DifftWsListener(APPID, APPSECRET, 'openapi.difft.org')

# set you message handler
listener.handler(customized_handler)
listener.start()
```
## Run test
```shell
python3 -m unittest discover
```

# TODO
* [x] Auth
* [x] Attachment APIs
* [x] Message APIs
* [x] Account APIs
* [x] Group APIs
* [ ] Team APIs

# CHANGELOG
## 2022.7.14
1. support recall message
## 2022.5.13
1. support getting refID when send message
## 2022.5.10
1. difft-cli support card message
## 2022.4.27
1. support websocket
***websocket和callback(webhook)只能二选一***.  

***if you turn on websocket, then the webhook stop working.***

## 2022.4.18
1. support quote

## 2022.3.26
1. support command-line tool 

## 2022.3.24
1. support get group

## 2022.3.23
1. support get account

## 2022.3.18
1. send message return failed list
2. support set content-type when send attachment

## 2022.3.16
1. support send message
2. support uploand and download attachment
3. support append and remove attachment authorization

## init
1. support authentication
