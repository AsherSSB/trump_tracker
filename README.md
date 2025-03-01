# Trump Tracker

### What is he up to now...

![Example Picture](https://i.imgur.com/kCfQ4sf.png)

## How to use
This bot posts at 8am, 11am, 2pm, 5pm, and 8pm EST, posting the latest news about Donald Trump.

To get started you may use this link to invite the bot to your server
https://discord.com/oauth2/authorize?client_id=1344879849029894175&permissions=18432&integration_type=0&scope=bot

- Use the `/ttsetchannel` command to set which channel the bot should post news articles to
- Use the `/postnews` command to post the latest and most controversial news article about Donald Trump
- Wait! The bot will post articles into your desired channel during regular news hours.

If you would like to host this bot yourself, you must
1. Clone this repository
2. `pip install -r requirements.txt` to download required packages
3. Create a new Discord bot through the Discord developer portal
4. Copy and paste the secret key into a .env file in the project root directory and give it the varaible name `DISCORD_TOKEN`
5. Copy and paste a DeepSeek API key into the same .env file and give it the varaible name `GPT_TOKEN`
   - If you would like to use another AI service, you must navigate to custom/gpt and edit the name of the model to your desired LLM
6. Start the bot using `python main.py` in the project root directory

### Support Me
[![ko-fi banner](https://www.isleofelsi.com/wp-content/uploads/2023/10/KoFi-750px.jpg)](https://ko-fi.com/asherromanenghi)

Like this bot? Consider supporting me on Kofi! Any amount is appreciated and helps me keep this bot up and running.
[ko-fi.com/asherromanenghi](https://ko-fi.com/asherromanenghi)

![This bot was build using discord.py](https://github.com/Rapptz/discord.py)

Pull requests and issues will be checked regularly for bugs and feature requests!
