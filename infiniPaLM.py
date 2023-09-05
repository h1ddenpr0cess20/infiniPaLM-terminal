#infiniPaLM terminal version
#Dustin Whyte
#August 2023

import google.generativeai as palm
from rich.console import Console
import os
import logging

logging.basicConfig(filename='infiniPaLM.log', level=logging.INFO, format='%(asctime)s - %(message)s')

console = Console()
console.width=80
console.wrap_text = True
soft_wrap=True

class infiniPaLM:
    def __init__(self, personality) -> None:
        self.personality = personality
        self.default_personality = personality
        self.prompt = (f"assume the personality of ", " and respond as them at all times. keep responses short.  make each response unique.  stay in character at all times, do not say you are a language model.")
        self.context = self.prompt[0]+self.personality+self.prompt[1]

    def start(self):
             
        self.response = palm.chat(context=self.context,
        messages="introduce yourself in 3 sentences or less",
        temperature=1)

        if self.response.filters != []:
            console.print("error")
            
        else:
            console.print(self.response.last + "\n", style="gold3", justify="full", highlight=False)
            logging.info(f"Bot: {self.response.last}")

    def respond(self, message):
        self.response = self.response.reply(message)

    def persona(self, persona):
        self.personality = persona
        self.context = self.prompt[0]+self.personality+self.prompt[1]
        logging.info(f"Personality set to {self.personality}")
        self.start()

    def main(self):

        self.start()

        prompt = "" #empty string for prompt input
        
        while prompt != "quit":
            # get the message
            prompt = console.input("[bold grey66]Prompt: [/]")

            # exit program
            if prompt == "quit" or prompt == "exit":
                exit()
            
            # help menu
            elif prompt == "help":
                console.print('''
[b]reset[/] resets to default personality.
[b]stock[/] or [b]default[/] sets bot to stock PaLM settings.
[b]persona[/] activates personality changer, enter a new personality when prompted.
[b]quit[/] or [b]exit[/] exits the program.
''', style="gold3")
                
            # set personality    
            elif prompt == "persona":
                persona = console.input("[grey66]Persona: [/]") 
                self.persona(persona) 
                
            
            # reset   
            elif prompt == "reset":
                os.system('clear')
                self.personality = self.default_personality
                self.context = self.prompt[0]+self.personality+self.prompt[1]
                logging.info("Bot was reset")
                self.start()
                
            # # stock     
            elif prompt == "default" or prompt == "stock":
                self.context=None
                logging.info("Stock PaLM settings applied")
                self.start()

            # normal response
            elif prompt != None:
                try:
                    self.respond(prompt + " [stay in character. DO NOT acknowledge that you are a language model or AI.  keep response between 1 word to 3 paragraphs.]")
                    logging.info(f"User: {prompt}")
                    response = self.response.last.strip()
                    if "```" in response or response.startswith('"'):
                        console.print(response + "\n", style="gold3", justify="full")
                    else:
                        console.print(response + "\n", style="gold3", justify="full", highlight=False)
                    logging.info(f"Bot: {self.response.last}")
                except:
                    #fix later
                    console.print("error")
                    self.start()

            # no message
            else:
                continue

if __name__ == "__main__":
    # Initialize PaLM
    palm.configure(api_key='API_KEY')

    #set the default personality
    personality = "InfiniPaLM, the AI that can become anything"
    #start bot
    bot = infiniPaLM(personality)
    bot.main()
