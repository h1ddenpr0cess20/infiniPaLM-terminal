#infiniPaLM terminal version
#Dustin Whyte
#August 2023

import google.generativeai as palm
from rich.console import Console
import os

#text formatting with Rich
console = Console()
console.width=80
console.wrap_text = True
soft_wrap=True

class infiniPaLM:
    def __init__(self, personality) -> None:
        #set personality
        self.personality = personality
        #store default personality 
        self.default_personality = personality
        #prompt parts
        self.prompt = (f"adopt the personality of ", " and respond as them at all times. keep your responses short and conversational. it is very important that you never repeat phrases. stay in character at all times.  it is extremely important that you never tell me that you are a language model.")
        #assembled prompt
        self.context = self.prompt[0]+self.personality+self.prompt[1]

    def start(self):
        #introduction to the current personality
        self.response = palm.chat(context=self.context,
        messages="briefly introduce yourself",
        temperature=1)

        if self.response.filters != []:
            console.print("error")
            
        else:
            console.print(self.response.last + "\n", style="gold3", justify="full")

    def respond(self, message):
        self.response = self.response.reply(message)

    def persona(self, persona):
        self.personality = persona
        #reset the context in case stock function was used previously
        self.context = self.prompt[0]+self.personality+self.prompt[1]
        #restart bot
        self.start()

    def main(self):
        #start bot
        self.start()

        #empty string for prompt input
        prompt = "" 
        
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
                #input new personality
                persona = console.input("[grey66]Persona: [/]")
                #set personality
                self.persona(persona) 
                
            
            # reset   
            elif prompt == "reset":
                #reset to preset personality
                self.personality = self.default_personality
                #reset the context in case stock function was used previously
                self.context = self.prompt[0]+self.personality+self.prompt[1]
                #restart bot
                self.start()
                
            # stock PaLM
            elif prompt == "default" or prompt == "stock":
                #remove the context (it is an optional parameter)
                self.context=None
                #restart bot
                self.start()

            # normal response
            elif prompt != None:
                try:
                    #get response and print
                    self.respond(prompt)
                    console.print(self.response.last + "\n", style="gold3", justify="full") #print response
                except:
                    #restart bot if fail
                    self.start()
            
            # no message
            else:
                continue

if __name__ == "__main__":
    # Initialize OpenAI
    palm.configure(api_key='API_KEY')

    #set the default personality
    personality = "InfiniPaLM, the AI that can become anything"
    #start bot
    bot = infiniPaLM(personality)
    bot.main()
