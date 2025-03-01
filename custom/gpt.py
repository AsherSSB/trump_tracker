import openai
from dotenv import load_dotenv
import os

class ClickbaitRating():
    def __init__(self):
        self.prompts = [{"role": "system", "content": "for each response, give a rating 1.0-10.0 on how controversial the news title is, be granular. You MUST repond with nothing more than a number rating."}, {"role": "user", "content":""}]
        self.model = "deepseek-chat"
        self.max_tokens = 10

        load_dotenv()
        TOKEN = os.getenv("GPT_TOKEN")
        self.client = openai.OpenAI(api_key=TOKEN,
        base_url = "https://api.deepseek.com/v1")

    def generate_rating(self, article_title):
        self.prompts[1]["content"] = article_title
        result = self.client.chat.completions.create(
            messages=self.prompts,
            model=self.model,
            max_tokens=self.max_tokens)
        
        result = result.choices[0].message.content
        return result

