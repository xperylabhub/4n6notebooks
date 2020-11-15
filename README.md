# 4n6notebooks
Sharing some notebooks I use for forensic research or examinations.
Use as you want, credit and thanks are is always welcome :)

## 1. SQLCipher decrypt - signal iOS DB 12.4.1
Notebook to decrypt database encrypted with SQLCipher.
Full python - 

### Dependencies :
- Python 3.7+
- PyCrypto

## 2. Chat rendering : 
Rendering extracted chats to dynamic HTML like an instant message app
(docs/chat_rendering.gif)
Rely on a formatted Dataframe: 

input : df with following columns:
  * data-name str : contact name / number
  * data-time dt : time of message (needs to be datetime format)
  * message str : text message
  * content-type str : mime type of atachement or None (ex : 'image/jpeg')
  * file-path str : path of attachment to render
  * from_me bool : 0 if received, 1 if sent
output :
  * str including script and data to include in report html

Example can be found in the Signal parsing notebook

### Dependencies:
- Pandas

## 3. Signal parsing
Notebook to parse Signal database decrypted with Notebook #1
Renders chat as HTML using Chat rendering #2
