# pyeliza

Python implementation of the 1966 Eliza program by Joseph Weizenbaum. This program is based on the 
[implementation by Charles Hayden](http://chayden.net/eliza/Eliza.html).

## Usage

### At the command line

If you just want to have a chat with Eliza, then simply clone this repository and run 
```
python3 app.py
```
to get chatting.

### On Discord

To run Eliza on Discord you will need to create a bot and get an access token; instructions on how
to do this are rampant on the internet (e.g. [here](https://www.freecodecamp.org/news/create-a-discord-bot-with-python/)).

Then you just need to run
```
python3 discordapp.py <your-token-here>
```

### From another Python script

The best way to learn how the basic API works is to look in the source code of `app.py` and the `run_program`
method of `ElizaMain`; you will need to import the `ElizaMain` class and use the `read_script` method to read 
in a script (a default one is provided in the `scripts/` directory. You then use the `respond` method to 
generate a response to an input string.