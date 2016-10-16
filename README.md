# wat-bridge

A bridge between WhatsApp and Telegram.

This creates two listeners, one for WhatsApp and another for a Telegram bot. When the WhatsApp listener receives a message it relays the content to the Telegram bot, which sends it to the owner. In order to send a message to WhatsApp, the owner must do so through the Telegram bot.

## Usage

```
$ virtualenv -p python3 venv
$ . venv/bin/activate
$ pip install -r requirements.txt
$ WAT_CONF=path_to_conf_file python watbridge.py
```

**NOTE:** For some reason, yowsup has issues when receiving messages. The workaround mentioned at <https://github.com/tgalal/yowsup/issues/1613#issuecomment-247801568> works, so instead of installing yowsup from requirements, use:

```
$ pip install -U git+https://github.com/tawanda/yowsup.git
```

## Configuration

```conf
[tg]
owner = ONWER_ID
token = TOKEN

[wa]
phone = PHONE_NUMBER
password = PASSWORD

[db]
path = PATH_TO_DB
```

The Telegram token is obtained by talking to the *BotFather* through Telegram and creating a bot, while the owner ID can be obtained by using the `/me` command.

The WhatsApp phone must include the country code (only two digits) followed by the number, for instance `49xxxxxxxxx`, and the password can be obtained through the [Yowsup cli interface](https://github.com/tgalal/yowsup/wiki/yowsup-cli-2.0).

Lastly, the database path is the full path to the file that will contain blacklist and contacts. Note that this path should be readable/writable by the user that executes the application.

## License

This code is released under the MIT license (see LICENSE).

```
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
