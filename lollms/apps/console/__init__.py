from lollms.config import InstallOption
from lollms.binding import BindingBuilder, ModelBuilder
from lollms.personality import MSG_TYPE, PersonalityBuilder
from lollms.main_config import LOLLMSConfig
from lollms.helpers import ASCIIColors
from lollms.paths import LollmsPaths
from lollms.app import LollmsApplication
from lollms.terminal import MainMenu
#if self.personality.model is None :

from typing import Callable
from pathlib import Path
import argparse
import yaml
import time
import sys

class Conversation(LollmsApplication):
    def __init__(
                    self, 
                    configuration_path:str|Path=None, 
                    show_logo:bool=True, 
                    show_commands_list:bool=False, 
                    show_personality_infos:bool=True,
                    show_model_infos:bool=True,
                    show_welcome_message:bool=True,
                    show_time_elapsed:bool = False
                ):
        # Fore it to be a path
        self.configuration_path = configuration_path
        self.is_logging = False
        self.log_file_path = ""
        self.show_time_elapsed = show_time_elapsed
        self.bot_says = ""

        # get paths
        lollms_paths = LollmsPaths.find_paths(force_local=False, tool_prefix="lollms_server_")

        # Configuration loading part
        config = LOLLMSConfig.autoload(lollms_paths, configuration_path)

        super().__init__("lollms-console",config, lollms_paths)
        if not self.personality:
            raise Exception("missing personality")

        if show_logo:
            self.menu.show_logo()
        if show_commands_list:
            self.menu.show_commands_list()
        if show_personality_infos:
            print()
            print(f"{ASCIIColors.color_green}-----------------------------------------------------------------")
            print(f"{ASCIIColors.color_green}Current personality : {ASCIIColors.color_reset}{self.personality}")
            print(f"{ASCIIColors.color_green}Version : {ASCIIColors.color_reset}{self.personality.version}")
            print(f"{ASCIIColors.color_green}Author : {ASCIIColors.color_reset}{self.personality.author}")
            print(f"{ASCIIColors.color_green}Description : {ASCIIColors.color_reset}{self.personality.personality_description}")
            print(f"{ASCIIColors.color_green}-----------------------------------------------------------------")
            print()

        if show_model_infos:
            print()
            print(f"{ASCIIColors.color_green}-----------------------------------------------------------------")
            print(f"{ASCIIColors.color_green}Current binding : {ASCIIColors.color_reset}{self.config['binding_name']}")
            print(f"{ASCIIColors.color_green}Current model : {ASCIIColors.color_reset}{self.config['model_name']}")
            print(f"{ASCIIColors.color_green}Personal data path : {ASCIIColors.color_reset}{self.lollms_paths.personal_path}")
            print(f"{ASCIIColors.color_green}-----------------------------------------------------------------")            
            print()


        # If there is a disclaimer, show it
        if self.personality.disclaimer != "":
            print(f"\n{ASCIIColors.color_red}Disclaimer")
            print(self.personality.disclaimer)
            print(f"{ASCIIColors.color_reset}")

        if show_welcome_message and self.personality.welcome_message:
            ASCIIColors.red(self.personality.name+": ", end="")
            print(self.personality.welcome_message)
            
    def ask_override_file(self):
        user_input = input("Would you like to override the existing file? (Y/N): ")
        user_input = user_input.lower()
        if user_input == "y" or user_input == "yes":
            print("File will be overridden.")
            return True
        elif user_input == "n" or user_input == "no":
            print("File will not be overridden.")
            return False
        else:
            print("Invalid input. Please enter 'Y' or 'N'.")
            # Call the function again recursively to prompt the user for valid input
            return self.ask_override_file() 
                   
    def start_log(self, file_name):
        if Path(file_name).is_absolute():
            self.log_file_path = Path(file_name)
        else:
            home_dir = self.lollms_paths.personal_log_path
            home_dir.mkdir(parents=True, exist_ok=True)
            self.log_file_path = home_dir/file_name
            if self.log_file_path.exists():
                if not self.ask_override_file():
                    print("Cancelled")
                    return
        try:
            with(open(self.log_file_path, "w") as f):
                self.header = f"""------------------------
Log file for lollms discussion                        
Participating personalities:
{self.config['personalities']}                  
------------------------
"""
                f.write(self.header)
            self.is_logging = True
            return True
        except:
            return False            

    def log(self, text, append=False):
        try:
            with(open(self.log_file_path, "a" if append else "w") as f):
                f.write(text) if append else f.write(self.header+self.personality.personality_conditioning+text)
            return True
        except:
            return False            

    def stop_log(self):
        self.is_logging = False           

    def reset_context(self):
        if self.personality.include_welcome_message_in_disucssion:
            full_discussion = (
                self.personality.ai_message_prefix +
                self.personality.welcome_message +
                self.personality.link_text
            )
        else:
            full_discussion = ""
        return full_discussion
        
    def safe_generate(self, full_discussion:str, n_predict=None, callback: Callable[[str, int, dict], bool]=None):
        """safe_generate

        Args:
            full_discussion (string): A prompt or a long discussion to use for generation
            callback (_type_, optional): A callback to call for each received token. Defaults to None.

        Returns:
            str: Model output
        """
        if n_predict == None:
            n_predict =self.personality.model_n_predicts
        if self.personality.model is None :
            raise Exception("no model")
        tk = self.personality.model.tokenize(full_discussion)
        n_tokens = len(tk)
        fd = self.personality.model.detokenize(tk[-min(self.config.ctx_size-self.n_cond_tk,n_tokens):])
        self.bot_says = ""
        output = self.personality.model.generate(self.personality.personality_conditioning+fd, n_predict=n_predict, callback=callback)
        return output
    
    def remove_text_from_string(self, string, text_to_find):
        """
        Removes everything from the first occurrence of the specified text in the string (case-insensitive).

        Parameters:
        string (str): The original string.
        text_to_find (str): The text to find in the string.

        Returns:
        str: The updated string.
        """
        index = string.lower().find(text_to_find.lower())

        if index != -1:
            string = string[:index]

        return string    
        
    def start_conversation(self):
        full_discussion = self.reset_context()
        while True:
            try:
                ump = self.config.discussion_prompt_separator +self.config.user_name+": " if self.config.use_user_name_in_discussions else self.personality.user_message_prefix
                if self.config.use_user_name_in_discussions:
                    prompt = input(f"{ASCIIColors.color_green}{self.config.user_name}: {ASCIIColors.color_reset}")
                else:
                    prompt = input(f"{ASCIIColors.color_green}You: {ASCIIColors.color_reset}")
                if self.show_time_elapsed:
                    t0 = time.time() #Time at start of request
                if prompt == "exit":
                    return
                if prompt == "menu":
                    self.menu.main_menu()
                    continue
                if prompt == "reset":
                    self.reset_context()
                    print(f"{ASCIIColors.color_red}Context reset issued{ASCIIColors.color_reset}")
                    continue
                if prompt == "start_log":
                    fp = input("Please enter a log file path (ex: log.txt): ")               
                    self.start_log(fp)
                    print(f"{ASCIIColors.color_red}Started logging to : {self.log_file_path}{ASCIIColors.color_reset}")
                    continue
                if prompt == "stop_log":
                    self.stop_log()
                    print(f"{ASCIIColors.color_red}Log stopped{ASCIIColors.color_reset}")
                    continue    
                if prompt == "send_file":
                    if self.personality.processor is None:
                        print(f"{ASCIIColors.color_red}This personality doesn't support file reception{ASCIIColors.color_reset}")
                        continue
                    fp = input("Please enter a file path: ")
                    # Remove double quotes using string slicing
                    if fp.startswith('"') and fp.endswith('"'):
                        fp = fp[1:-1]
                    if self.personality.processor.add_file(fp):
                        print(f"{ASCIIColors.color_green}File imported{ASCIIColors.color_reset}")
                    else:
                        print(f"{ASCIIColors.color_red}Couldn't load file{ASCIIColors.color_reset}")
                    continue    
                            
                   
                if prompt == "context_infos":
                    tokens = self.personality.model.tokenize(full_discussion)
                    print(f"{ASCIIColors.color_green}Current context has {len(tokens)} tokens/ {self.config.ctx_size}{ASCIIColors.color_reset}")
                    continue                
                              
                if prompt != '':
                    if self.personality.processor is not None and self.personality.processor_cfg["process_model_input"]:
                        preprocessed_prompt = self.personality.processor.process_model_input(prompt)
                    else:
                        preprocessed_prompt = prompt
                    
                    if self.personality.processor is not None and self.personality.processor_cfg["custom_workflow"]:
                        full_discussion += (
                            ump +
                            preprocessed_prompt
                        )
                    else:
                        full_discussion += (
                            ump +
                            preprocessed_prompt +
                            self.personality.link_text +
                            self.personality.ai_message_prefix
                        )

                def callback(text, type:MSG_TYPE=None, metadata:dict={}):
                    if type == MSG_TYPE.MSG_TYPE_CHUNK:
                        # Replace stdout with the default stdout
                        sys.stdout = sys.__stdout__
                        print(text, end="", flush=True)
                        bot_says = self.bot_says + text
                        antiprompt = self.personality.detect_antiprompt(bot_says)
                        if antiprompt:
                            self.bot_says = self.remove_text_from_string(bot_says,antiprompt)
                            ASCIIColors.warning(f"Detected hallucination with antiprompt {antiprompt}")
                            return False
                        else:
                            self.bot_says = bot_says
                            return True

                tk = self.personality.model.tokenize(full_discussion)
                n_tokens = len(tk)
                fd = self.personality.model.detokenize(tk[-min(self.config.ctx_size-self.n_cond_tk,n_tokens):])
                
                print(f"{ASCIIColors.color_red}{self.personality.name}:{ASCIIColors.color_reset}", end='', flush=True)
                if self.personality.processor is not None and self.personality.processor_cfg["custom_workflow"]:
                    output = self.personality.processor.run_workflow(prompt, previous_discussion_text=self.personality.personality_conditioning+fd, callback=callback)
                    print(output)

                else:
                    output = self.personality.model.generate(self.personality.personality_conditioning+fd, n_predict=self.personality.model_n_predicts, callback=callback)
                full_discussion += output.strip()
                print()

                if self.personality.processor is not None and self.personality.processor_cfg["process_model_output"]: 
                    output = self.personality.processor.process_model_output(output)

                self.log(full_discussion)
                
                if self.show_time_elapsed:
                    t1 = time.time() # Time at end of response
                    print(f"{ASCIIColors.color_cyan}Time Elapsed: {ASCIIColors.color_reset}",str(int((t1-t0)*1000)),"ms\n") # Total time elapsed since t0 in ms
            except KeyboardInterrupt:
                print("Keyboard interrupt detected.\nBye")
                break

        print("Done")
        print(f"{self.personality}")

def main():
    # Create the argument parser
    parser = argparse.ArgumentParser(description='App Description')

    # Add the configuration path argument
    parser.add_argument('--configuration_path', default=None,
                        help='Path to the configuration file')


    parser.add_argument('--reset_personal_path', action='store_true', help='Reset the personal path')
    parser.add_argument('--reset_config', action='store_true', help='Reset the configurations')
    parser.add_argument('--reset_installs', action='store_true', help='Reset all installation status')
    parser.add_argument('--show_time_elapsed', action='store_true', help='Enables response time')


    # Parse the command-line arguments
    args = parser.parse_args()

    if args.reset_installs:
        LollmsApplication.reset_all_installs()

    if args.reset_personal_path:
        LollmsPaths.reset_configs()
    
    if args.reset_config:
        lollms_paths = LollmsPaths.find_paths(tool_prefix="lollms_server_")
        cfg_path = lollms_paths.personal_configuration_path / f"{lollms_paths.tool_prefix}local_config.yaml"
        try:
            cfg_path.unlink()
            ASCIIColors.success("LOLLMS configuration reset successfully")
        except:
            ASCIIColors.success("Couldn't reset LOLLMS configuration")
    if args.show_time_elapsed:
        show_time_elapsed = True
    else:
        show_time_elapsed = False

    # Parse the command-line arguments
    args = parser.parse_args()
            
    configuration_path = args.configuration_path
        
    lollms_app = Conversation(configuration_path=configuration_path, show_commands_list=True, show_time_elapsed=show_time_elapsed)
    lollms_app.start_conversation()
    

if __name__ == "__main__":
    main()
