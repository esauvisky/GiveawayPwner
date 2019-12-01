# GiveawayPwner

Wins guess-type giveaways on Discord by keeping a log of unique answers while prioritising answers from a truncated normal standard distribution to increase the odds of winning.

## Config

- You need node and python3

- Install python dependencies

```console
$ pip install -r requirements.txt
```

- Node dependencies should work out of the box (node modules is built in). Try it out by running:

```console
$ node index.js
```

  – In case some error happens, try `npm install` or search the web because I'm a noob at node.

- Get an account with some score on 001xédekoP. Can be your main. **Must be the same account that's gonna participate on the giveaway.**

– Get its token by following the [Token](#token) section below.

- Edit `config.json.js` and add your token in there.

- Run `node index.js` and check if it properly detects the account, it should output its name#tag.

### Token
See [GetToken.gif]().

Make sure you get the `messages` XHR request, and not another one.

## Usage

- Clear `messages.log`

- Run `node index.js` as soon as the giveaway announcement is made. Keep it running on the background.
  - The process will keep a log of each message sent to the #giveaway channel, so our giveaway pwner only guesses unique answers.
  - Every dash `(–)` means an user sent a non-unique message.

– Open another terminal or tab and prepare the giveaway command:
```console
$ python giveaway.py -t 2 300...800
```
> _That would send answers from 300 to 800 each 2 seconds, following a normal standard gaussian truncated distrubution, that is, giving priority to numbers in the middle, but never using an answer that was previously used._

- As soon as the giveaway starts and the message box in the channel is open to input, run the command and quickly click the input text box.
  - The bot will literally press Esc, Ctrl+A, Write the answer it chose, and Enter.
  - The first two are safe checks for if discord begins to stop you for being too fast (1.5 seconds between messages is approx. the quickest you can send without getting noticed).

- Check `python giveaway.py --help` for more options.

### More Examples
```console
$ ./giveaway.py -f /text-answers/gens1-4/gen3rev.txt ...
$ ./giveaway.py -t 2 -f text-answers/items.txt -n ... , ... , ... , ... , ...
```

## Issues:

- When using -z (leading zeros) alongside -n (strip spaces), something doesn't work quite well.
