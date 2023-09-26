from datetime import datetime
from pathlib import Path
from lollms.config import InstallOption, TypedConfig, BaseConfig
from lollms.main_config import LOLLMSConfig
from lollms.paths import LollmsPaths
from lollms.binding import LLMBinding

import pkg_resources
from pathlib import Path
#from PIL import Image
from typing import Optional, List
import re
from datetime import datetime
import importlib
import shutil
import subprocess
import yaml
from lollms.helpers import ASCIIColors
from lollms.types import MSG_TYPE
from typing import Callable
import json
from lollms.utilities import TextVectorizer, GenericDataLoader
from functools import partial

def is_package_installed(package_name):
    try:
        dist = pkg_resources.get_distribution(package_name)
        return True
    except pkg_resources.DistributionNotFound:
        return False
    

def install_package(package_name):
    try:
        # Check if the package is already installed
        __import__(package_name)
        print(f"{package_name} is already installed.")
    except ImportError:
        print(f"{package_name} is not installed. Installing...")
        
        # Install the package using pip
        subprocess.check_call(["pip", "install", package_name])
        
        print(f"{package_name} has been successfully installed.")

class AIPersonality:

    # Extra     
    def __init__(
                    self, 
                    personality_package_path: str|Path, 
                    lollms_paths:LollmsPaths, 
                    config:LOLLMSConfig,
                    model:LLMBinding=None,
                    app=None,
                    run_scripts=True, 
                    selected_language=None,
                    is_relative_path=True,
                    installation_option:InstallOption=InstallOption.INSTALL_IF_NECESSARY,
                    callback: Callable[[str, MSG_TYPE, dict, list], bool]=None
                ):
        """
        Initialize an AIPersonality instance.

        Parameters:
        personality_package_path (str or Path): The path to the folder containing the personality package.

        Raises:
        ValueError: If the provided path is not a folder or does not contain a config.yaml file.
        """
        self.lollms_paths = lollms_paths
        self.model = model
        self.config = config
        self.callback = callback
        self.app = app

        self.files = []
        self.vectorizer = None

        self.installation_option = installation_option

        # First setup a default personality
        # Version
        self._version = pkg_resources.get_distribution('lollms').version

        self.run_scripts = run_scripts

        #General information
        self._author: str = "ParisNeo"
        self._name: str = "lollms"
        self._user_name: str = "user"
        self._category: str = "General"
        self._supported_languages: str = []
        self._selected_language: str = selected_language

        # Conditionning
        self._personality_description: str = "This personality is a helpful and Kind AI ready to help you solve your problems"
        self._personality_conditioning: str = """## Instructions:
lollms (Lord of LLMs) is a smart and helpful Assistant built by the computer geek ParisNeo.
It is compatible with many bindings to LLM models such as llama, gpt4all, gptj, autogptq etc.
It can discuss with humans and assist them on many subjects.
It runs locally on your machine. No need to connect to the internet.
It answers the questions with precise details
Its performance depends on the underlying model size and training.
Try to answer with as much details as you can
Date: {{date}}
"""
        self._welcome_message: str = "Welcome! I am lollms (Lord of LLMs) A free and open assistant built by ParisNeo. What can I do for you today?"
        self._include_welcome_message_in_disucssion: bool = True
        self._user_message_prefix: str = "!@> Human: "
        self._link_text: str = "\n"
        self._ai_message_prefix: str = "!@> lollms:"
        self._anti_prompts:list = [self.config.discussion_prompt_separator]

        # Extra
        self._dependencies: List[str] = []

        # Disclaimer
        self._disclaimer: str = ""
        self._help: str = ""
        self._commands: list = []
        
        # Default model parameters
        self._model_temperature: float = 0.8 # higher: more creative, lower more deterministic
        self._model_n_predicts: int = 2048 # higher: generates many words, lower generates
        self._model_top_k: int = 50
        self._model_top_p: float = 0.95
        self._model_repeat_penalty: float = 1.3
        self._model_repeat_last_n: int = 40
        
        self._processor_cfg: dict = {}

        #self._logo: Optional[Image.Image] = None
        self._processor = None

        if personality_package_path is None:
            self.config = {}
            self.assets_list = []
            self.personality_package_path = None
            return
        else:
            if is_relative_path:
                self.personality_package_path = self.lollms_paths.personalities_zoo_path/personality_package_path
            else:
                self.personality_package_path = Path(personality_package_path)

            # Validate that the path exists
            if not self.personality_package_path.exists():
                raise ValueError(f"Could not find the personality package:{self.personality_package_path}")

            # Validate that the path format is OK with at least a config.yaml file present in the folder
            if not self.personality_package_path.is_dir():
                raise ValueError(f"Personality package path is not a folder:{self.personality_package_path}")

            self.personality_folder_name = self.personality_package_path.stem

            # Open and store the personality
            self.load_personality()

    def setCallback(self, callback: Callable[[str, MSG_TYPE, dict, list], bool]):
        self.callback = callback
        if self._processor:
            self._processor.callback = callback


    def __str__(self):
        return f"{self.category}/{self.name}"


    def load_personality(self, package_path=None):
        """
        Load personality parameters from a YAML configuration file.

        Args:
            package_path (str or Path): The path to the package directory.

        Raises:
            ValueError: If the configuration file does not exist.
        """
        if package_path is None:
            package_path = self.personality_package_path
        else:
            package_path = Path(package_path)

        # Verify that there is at least a configuration file
        config_file = package_path / "config.yaml"
        if not config_file.exists():
            raise ValueError(f"The provided folder {package_path} does not exist.")

        with open(config_file, "r", encoding='utf-8') as f:
            config = yaml.safe_load(f)

        secret_file = package_path / "secret.yaml"
        if secret_file.exists():
            with open(secret_file, "r", encoding='utf-8') as f:
                self._secret_cfg = yaml.safe_load(f)
        else:
            self._secret_cfg = None

        languages = package_path / "languages"

        if languages.exists():
            self._supported_languages = []
            for language in [l for l in languages.iterdir()]:
                self._supported_languages.append(language.stem)

            if self._selected_language is not None and self._selected_language in self._supported_languages:
                config_file = languages / (self._selected_language+".yaml")
                with open(config_file, "r", encoding='utf-8') as f:
                    config = yaml.safe_load(f)



        # Load parameters from the configuration file
        self._version = config.get("version", self._version)
        self._author = config.get("author", self._author)
        self._name = config.get("name", self._name)
        self._user_name = config.get("user_name", self._user_name)
        self._category = config.get("category", self._category)

        self._personality_description = config.get("personality_description", self._personality_description)
        self._personality_conditioning = config.get("personality_conditioning", self._personality_conditioning)
        self._welcome_message = config.get("welcome_message", self._welcome_message)
        self._include_welcome_message_in_disucssion = config.get("include_welcome_message_in_disucssion", self._include_welcome_message_in_disucssion)

        self._user_message_prefix = config.get("user_message_prefix", self._user_message_prefix)
        self._link_text = config.get("link_text", self._link_text)
        self._ai_message_prefix = config.get("ai_message_prefix", self._ai_message_prefix)
        self._anti_prompts = [self.config.discussion_prompt_separator]+config.get("anti_prompts", self._anti_prompts)
        self._dependencies = config.get("dependencies", self._dependencies)
        self._disclaimer = config.get("disclaimer", self._disclaimer)
        self._help = config.get("help", self._help)
        self._commands = config.get("commands", self._commands)
        self._model_temperature = config.get("model_temperature", self._model_temperature)
        self._model_n_predicts = config.get("model_n_predicts", self._model_n_predicts)
        self._model_top_k = config.get("model_top_k", self._model_top_k)
        self._model_top_p = config.get("model_top_p", self._model_top_p)
        self._model_repeat_penalty = config.get("model_repeat_penalty", self._model_repeat_penalty)
        self._model_repeat_last_n = config.get("model_repeat_last_n", self._model_repeat_last_n)
        
        # Script parameters (for example keys to connect to search engine or any other usage)
        self._processor_cfg = config.get("processor_cfg", self._processor_cfg)
        

        #set package path
        self.personality_package_path = package_path

        # Check for a logo file
        self.logo_path = self.personality_package_path / "assets" / "logo.png"
        #if self.logo_path.is_file():
        #    self._logo = Image.open(self.logo_path)

        # Get the assets folder path
        self.assets_path = self.personality_package_path / "assets"
        # Get the scripts folder path
        self.scripts_path = self.personality_package_path / "scripts"
        
        # If not exist recreate
        self.assets_path.mkdir(parents=True, exist_ok=True)

        # If not exist recreate
        self.scripts_path.mkdir(parents=True, exist_ok=True)


        if self.run_scripts:
            # Search for any processor code
            processor_file_name = "processor.py"
            self.processor_script_path = self.scripts_path / processor_file_name
            if self.processor_script_path.exists():
                module_name = processor_file_name[:-3]  # Remove the ".py" extension
                module_spec = importlib.util.spec_from_file_location(module_name, str(self.processor_script_path))
                module = importlib.util.module_from_spec(module_spec)
                module_spec.loader.exec_module(module)
                if hasattr(module, "Processor"):
                    self._processor = module.Processor(self, callback=self.callback)
                else:
                    self._processor = None
            else:
                self._processor = None
        # Get a list of all files in the assets folder
        contents = [str(file) for file in self.assets_path.iterdir() if file.is_file()]

        self._assets_list = contents
        return config
    def remove_file(self, path, callback=None):
        try:
            self.files.remove(path)
            Path(path).unlink()
            if len(self.files)>0:
                try:
                    self.vectorizer.remove_document(path)
                    if callback is not None:
                        callback("File added successfully",MSG_TYPE.MSG_TYPE_INFO)
                    return True
                except ValueError as ve:
                    ASCIIColors.error(f"Unsupported file format. Supported formats are {GenericDataLoader.get_supported_file_types()}")
                    return False
            else:
                self.vectorizer = None
        except Exception as ex:
            ASCIIColors.warning(f"Couldn't remove the file {path}")

    def remove_all_files(self, callback=None):
        for file in self.files:
            try:
                Path(file).unlink()
            except Exception as ex:
                ASCIIColors.warning(f"Couldn't remove the file {file}")
        self.files=[]  
        self.vectorizer = None
        return True     
    def add_file(self, path, callback=None):
        self.files.append(path)
        db_path = self.lollms_paths.personal_databases_path / "personalities" / self.name / "db.json"
        db_path.parent.mkdir(parents=True, exist_ok=True)
        if self.vectorizer is None:
            self.vectorizer = TextVectorizer(self.config.data_vectorization_method, # supported "model_embedding" or "ftidf_vectorizer"
                        model=self.model, #needed in case of using model_embedding
                        database_path=db_path,
                        save_db=self.config.data_vectorization_save_db,
                        visualize_data_at_startup=False,
                        visualize_data_at_add_file=False,
                        visualize_data_at_generate=False,
                        data_visualization_method="PCA",
                        database_dict=None)
        try:
            data = GenericDataLoader.read_file(path)
            self.vectorizer.add_document(path, data, self.config.data_vectorization_chunk_size, self.config.data_vectorization_overlap_size)
            self.vectorizer.index()
            if callback is not None:
                callback("File added successfully",MSG_TYPE.MSG_TYPE_INFO)
            return True
        except ValueError as ve:
            ASCIIColors.error(f"Unsupported file format. Supported formats are {GenericDataLoader.get_supported_file_types()}")
            return False
    def save_personality(self, package_path=None):
        """
        Save the personality parameters to a YAML configuration file.

        Args:
            package_path (str or Path): The path to the package directory.
        """
        if package_path is None:
            package_path = self.personality_package_path
        else:
            package_path = Path(package_path)

        # Building output path
        config_file = package_path / "config.yaml"
        assets_folder = package_path / "assets"

        # Create assets folder if it doesn't exist
        if not assets_folder.exists():
            assets_folder.mkdir(exist_ok=True, parents=True)

        # Create the configuration dictionary
        config = {
            "author": self._author,
            "version": self._version,
            "name": self._name,
            "user_name": self._user_name,
            "category": self._category,
            "supported_languages": self._supported_languages,
            "selected_language": self._selected_language,
            "personality_description": self._personality_description,
            "personality_conditioning": self._personality_conditioning,
            "welcome_message": self._welcome_message,
            "include_welcome_message_in_disucssion": self._include_welcome_message_in_disucssion,
            "user_message_prefix": self._user_message_prefix,
            "link_text": self._link_text,
            "ai_message_prefix": self._ai_message_prefix,
            "anti_prompts": self._anti_prompts,
            "dependencies": self._dependencies,
            "disclaimer": self._disclaimer,
            "help": self._help,
            "commands": self._commands,
            "model_temperature": self._model_temperature,
            "model_n_predicts": self._model_n_predicts,
            "model_top_k": self._model_top_k,
            "model_top_p": self._model_top_p,
            "model_repeat_penalty": self._model_repeat_penalty,
            "model_repeat_last_n": self._model_repeat_last_n
        }

        # Save the configuration to the YAML file
        with open(config_file, "w") as f:
            yaml.dump(config, f)



    def as_dict(self):
        """
        Convert the personality parameters to a dictionary.

        Returns:
            dict: The personality parameters as a dictionary.
        """
        return {
            "author": self._author,
            "version": self._version,
            "name": self._name,
            "user_name": self._user_name,
            "category": self._category,
            "supported_languages": self._supported_languages,
            "selected_language": self._selected_language,
            "personality_description": self._personality_description,
            "personality_conditioning": self._personality_conditioning,
            "welcome_message": self._welcome_message,
            "include_welcome_message_in_disucssion": self._include_welcome_message_in_disucssion,
            "user_message_prefix": self._user_message_prefix,
            "link_text": self._link_text,
            "ai_message_prefix": self._ai_message_prefix,
            "anti_prompts": self._anti_prompts,
            "dependencies": self._dependencies,
            "disclaimer": self._disclaimer,
            "help": self._help,
            "commands": self._commands,
            "model_temperature": self._model_temperature,
            "model_n_predicts": self._model_n_predicts,
            "model_top_k": self._model_top_k,
            "model_top_p": self._model_top_p,
            "model_repeat_penalty": self._model_repeat_penalty,
            "model_repeat_last_n": self._model_repeat_last_n,
            "assets_list":self._assets_list
        }

    # ========================================== Properties ===========================================
    @property
    def conditionning_commands(self):
        return {
            "date_time": datetime.now().strftime("%A, %B %d, %Y %I:%M:%S %p"), # Replaces {{date}} with actual date
            "date": datetime.now().strftime("%A, %B %d, %Y"), # Replaces {{date}} with actual date
            "time": datetime.now().strftime("%H:%M:%S"), # Replaces {{time}} with actual time
        }

    @property
    def logo(self):
        """
        Get the personality logo.

        Returns:
        PIL.Image.Image: The personality logo as a Pillow Image object.
        """
        if hasattr(self, '_logo'):
            return self._logo
        else:
            return None    
    @property
    def version(self):
        """Get the version of the package."""
        return self._version

    @version.setter
    def version(self, value):
        """Set the version of the package."""
        self._version = value

    @property
    def author(self):
        """Get the author of the package."""
        return self._author

    @author.setter
    def author(self, value):
        """Set the author of the package."""
        self._author = value

    @property
    def name(self) -> str:
        """Get the name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the name."""
        self._name = value

    @property
    def user_name(self) -> str:
        """Get the user name."""
        return self._user_name

    @user_name.setter
    def user_name(self, value: str):
        """Set the user name."""
        self._user_name = value

    @property
    def category(self) -> str:
        """Get the category."""
        return self._category

    @category.setter
    def category(self, value: str):
        """Set the category."""
        self._category = value


    @property
    def supported_languages(self) -> str:
        """Get the supported_languages."""
        return self._supported_languages

    @supported_languages.setter
    def supported_languages(self, value: str):
        """Set the supported_languages."""
        self._supported_languages = value


    @property
    def selected_language(self) -> str:
        """Get the selected_language."""
        return self._selected_language

    @selected_language.setter
    def selected_language(self, value: str):
        """Set the selected_language."""
        self._selected_language = value

    @property
    def personality_description(self) -> str:
        """
        Getter for the personality description.

        Returns:
            str: The personality description of the AI assistant.
        """
        return self._personality_description

    @personality_description.setter
    def personality_description(self, description: str):
        """
        Setter for the personality description.

        Args:
            description (str): The new personality description for the AI assistant.
        """
        self._personality_description = description

    @property
    def personality_conditioning(self) -> str:
        """
        Getter for the personality conditioning.

        Returns:
            str: The personality conditioning of the AI assistant.
        """
        return self.replace_keys(self._personality_conditioning, self.conditionning_commands)

    @personality_conditioning.setter
    def personality_conditioning(self, conditioning: str):
        """
        Setter for the personality conditioning.

        Args:
            conditioning (str): The new personality conditioning for the AI assistant.
        """
        self._personality_conditioning = conditioning

    @property
    def welcome_message(self) -> str:
        """
        Getter for the welcome message.

        Returns:
            str: The welcome message of the AI assistant.
        """
        return self.replace_keys(self._welcome_message, self.conditionning_commands)

    @welcome_message.setter
    def welcome_message(self, message: str):
        """
        Setter for the welcome message.

        Args:
            message (str): The new welcome message for the AI assistant.
        """
        self._welcome_message = message

    @property
    def include_welcome_message_in_disucssion(self) -> bool:
        """
        Getter for the include welcome message in disucssion.

        Returns:
            bool: whether to add the welcome message to tje discussion or not.
        """
        return self._include_welcome_message_in_disucssion

    @include_welcome_message_in_disucssion.setter
    def include_welcome_message_in_disucssion(self, message: bool):
        """
        Setter for the welcome message.

        Args:
            message (str): The new welcome message for the AI assistant.
        """
        self._include_welcome_message_in_disucssion = message


    @property
    def user_message_prefix(self) -> str:
        """
        Getter for the user message prefix.

        Returns:
            str: The user message prefix of the AI assistant.
        """
        return self._user_message_prefix

    @user_message_prefix.setter
    def user_message_prefix(self, prefix: str):
        """
        Setter for the user message prefix.

        Args:
            prefix (str): The new user message prefix for the AI assistant.
        """
        self._user_message_prefix = prefix

    @property
    def link_text(self) -> str:
        """
        Getter for the link text.

        Returns:
            str: The link text of the AI assistant.
        """
        return self._link_text

    @link_text.setter
    def link_text(self, text: str):
        """
        Setter for the link text.

        Args:
            text (str): The new link text for the AI assistant.
        """
        self._link_text = text    
    @property
    def ai_message_prefix(self):
        """
        Get the AI message prefix.

        Returns:
            str: The AI message prefix.
        """
        return self._ai_message_prefix

    @ai_message_prefix.setter
    def ai_message_prefix(self, prefix):
        """
        Set the AI message prefix.

        Args:
            prefix (str): The AI message prefix to set.
        """
        self._ai_message_prefix = prefix

    @property
    def anti_prompts(self):
        """
        Get the anti-prompts list.

        Returns:
            list: The anti-prompts list.
        """
        return self._anti_prompts

    @anti_prompts.setter
    def anti_prompts(self, prompts):
        """
        Set the anti-prompts list.

        Args:
            prompts (list): The anti-prompts list to set.
        """
        self._anti_prompts = prompts


    @property
    def dependencies(self) -> List[str]:
        """Getter method for the dependencies attribute.

        Returns:
            List[str]: The list of dependencies.
        """
        return self._dependencies

    @dependencies.setter
    def dependencies(self, dependencies: List[str]):
        """Setter method for the dependencies attribute.

        Args:
            dependencies (List[str]): The list of dependencies.
        """
        self._dependencies = dependencies

    @property
    def disclaimer(self) -> str:
        """Getter method for the disclaimer attribute.

        Returns:
            str: The disclaimer text.
        """
        return self._disclaimer

    @disclaimer.setter
    def disclaimer(self, disclaimer: str):
        """Setter method for the disclaimer attribute.

        Args:
            disclaimer (str): The disclaimer text.
        """
        self._disclaimer = disclaimer

    @property
    def help(self) -> str:
        """Getter method for the help attribute.

        Returns:
            str: The help text.
        """
        return self._help

    @help.setter
    def help(self, help: str):
        """Setter method for the help attribute.

        Args:
            help (str): The help text.
        """
        self._help = help



    @property
    def commands(self) -> str:
        """Getter method for the commands attribute.

        Returns:
            str: The commands text.
        """
        return self._commands

    @commands.setter
    def commands(self, commands: str):
        """Setter method for the commands attribute.

        Args:
            commands (str): The commands text.
        """
        self._commands = commands


    @property
    def model_temperature(self) -> float:
        """Get the model's temperature."""
        return self._model_temperature

    @model_temperature.setter
    def model_temperature(self, value: float):
        """Set the model's temperature.

        Args:
            value (float): The new temperature value.
        """
        self._model_temperature = value

    @property
    def model_n_predicts(self) -> int:
        """Get the number of predictions the model generates."""
        return self._model_n_predicts

    @model_n_predicts.setter
    def model_n_predicts(self, value: int):
        """Set the number of predictions the model generates.

        Args:
            value (int): The new number of predictions value.
        """
        self._model_n_predicts = value

    @property
    def model_top_k(self) -> int:
        """Get the model's top-k value."""
        return self._model_top_k

    @model_top_k.setter
    def model_top_k(self, value: int):
        """Set the model's top-k value.

        Args:
            value (int): The new top-k value.
        """
        self._model_top_k = value

    @property
    def model_top_p(self) -> float:
        """Get the model's top-p value."""
        return self._model_top_p

    @model_top_p.setter
    def model_top_p(self, value: float):
        """Set the model's top-p value.

        Args:
            value (float): The new top-p value.
        """
        self._model_top_p = value

    @property
    def model_repeat_penalty(self) -> float:
        """Get the model's repeat penalty value."""
        return self._model_repeat_penalty

    @model_repeat_penalty.setter
    def model_repeat_penalty(self, value: float):
        """Set the model's repeat penalty value.

        Args:
            value (float): The new repeat penalty value.
        """
        self._model_repeat_penalty = value

    @property
    def model_repeat_last_n(self) -> int:
        """Get the number of words to consider for repeat penalty."""
        return self._model_repeat_last_n

    @model_repeat_last_n.setter
    def model_repeat_last_n(self, value: int):
        """Set the number of words to consider for repeat penalty.

        Args:
            value (int): The new number of words value.
        """
        self._model_repeat_last_n = value


    @property
    def assets_list(self) -> list:
        """Get the number of words to consider for repeat penalty."""
        return self._assets_list

    @assets_list.setter
    def assets_list(self, value: list):
        """Set the number of words to consider for repeat penalty.

        Args:
            value (int): The new number of words value.
        """
        self._assets_list = value

    @property
    def processor(self) -> 'APScript':
        """Get the number of words to consider for repeat penalty."""
        return self._processor

    @processor.setter
    def processor(self, value: 'APScript'):
        """Set the number of words to consider for repeat penalty.

        Args:
            value (int): The new number of words value.
        """
        self._processor = value


    @property
    def processor_cfg(self) -> list:
        """Get the number of words to consider for repeat penalty."""
        return self._processor_cfg

    @processor_cfg.setter
    def processor_cfg(self, value: dict):
        """Set the number of words to consider for repeat penalty.

        Args:
            value (int): The new number of words value.
        """
        self._processor_cfg = value

    # ========================================== Helper methods ==========================================
    def detect_antiprompt(self, text:str) -> bool:
        """
        Detects if any of the antiprompts in self.anti_prompts are present in the given text.
        Used for the Hallucination suppression system

        Args:
            text (str): The text to check for antiprompts.

        Returns:
            bool: True if any antiprompt is found in the text (ignoring case), False otherwise.
        """
        for prompt in self.anti_prompts:
            if prompt.lower() in text.lower():
                return prompt.lower()
        return None

    
    # Helper functions
    @staticmethod
    def replace_keys(input_string, replacements):
        """
        Replaces all occurrences of keys in the input string with their corresponding
        values from the replacements dictionary.

        Args:
            input_string (str): The input string to replace keys in.
            replacements (dict): A dictionary of key-value pairs, where the key is the
                string to be replaced and the value is the replacement string.

        Returns:
            str: The input string with all occurrences of keys replaced by their
                corresponding values.
        """        
        pattern = r"\{\{(\w+)\}\}"
        # The pattern matches "{{key}}" and captures "key" in a group.
        # The "\w+" matches one or more word characters (letters, digits, or underscore).

        def replace(match):
            key = match.group(1)
            return replacements.get(key, match.group(0))

        output_string = re.sub(pattern, replace, input_string)
        return output_string



class StateMachine:
    def __init__(self, states_dict):
        """
        states structure is the following
        [
            {
                "name": the state name,
                "commands": [ # list of commands
                    "command": function
                ],
                "default": default function
            }
        ]
        """
        self.states_dict = states_dict
        self.current_state_id = 0
        self.callback = None
    
    def goto_state(self, state):
        """
        Transition to the state with the given name or index.

        Args:
            state (str or int): The name or index of the state to transition to.

        Raises:
            ValueError: If no state is found with the given name or index.
        """
        if isinstance(state, str):
            for i, state_dict in enumerate(self.states_dict):
                if state_dict["name"] == state:
                    self.current_state_id = i
                    return
        elif isinstance(state, int):
            if 0 <= state < len(self.states_dict):
                self.current_state_id = state
                return
        raise ValueError(f"No state found with name or index: {state}")



    def process_state(self, command, full_context, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """
        Process the given command based on the current state.

        Args:
            command: The command to process.

        Raises:
            ValueError: If the current state doesn't have the command and no default function is defined.
        """
        if callback:
            self.callback=callback
            
        current_state = self.states_dict[self.current_state_id]
        commands = current_state["commands"]
        command = command.strip()
        
        for cmd, func in commands.items():
            if cmd == command[0:len(cmd)]:
                func(command, full_context)
                return
        
        default_func = current_state.get("default")
        if default_func is not None:
            default_func(command, full_context)
        else:
            raise ValueError(f"Command '{command}' not found in current state and no default function defined.")

        

class APScript(StateMachine):
    """
    Template class for implementing personality processor classes in the APScript framework.

    This class provides a basic structure and placeholder methods for processing model inputs and outputs.
    Personality-specific processor classes should inherit from this class and override the necessary methods.
    """
    def __init__(
                    self, 
                    personality         :AIPersonality,
                    personality_config  :TypedConfig,
                    states_dict         :dict   = {},
                    callback            = None
                ) -> None:
        super().__init__(states_dict)
        self.files=[]
        self.personality                        = personality
        self.personality_config                 = personality_config
        self.installation_option                = personality.installation_option
        self.configuration_file_path            = self.personality.lollms_paths.personal_configuration_path/"personalities"/self.personality.personality_folder_name/f"config.yaml"
        self.configuration_file_path.parent.mkdir(parents=True, exist_ok=True)

        self.personality_config.config.file_path    = self.configuration_file_path

        self.callback = callback
        # Installation
        if (not self.configuration_file_path.exists() or self.installation_option==InstallOption.FORCE_INSTALL) and self.installation_option!=InstallOption.NEVER_INSTALL:
            self.install()
            self.personality_config.config.save_config()
        else:
            self.load_personality_config()

    def load_personality_config(self):
        """
        Load the content of local_config.yaml file.

        The function reads the content of the local_config.yaml file and returns it as a Python dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the loaded data from the local_config.yaml file.
        """     
        try:
            self.personality_config.config.load_config()
        except:
            self.personality_config.config.save_config()
        self.personality_config.sync()        
       
    def install(self):
        """
        Installation procedure (to be implemented)
        """
        ASCIIColors.blue("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        ASCIIColors.red(f"Installing {self.personality.personality_folder_name}")
        ASCIIColors.blue("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")


    def uninstall(self):
        """
        Installation procedure (to be implemented)
        """
        ASCIIColors.blue("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        ASCIIColors.red(f"Uninstalling {self.personality.personality_folder_name}")
        ASCIIColors.blue("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")


    @staticmethod
    def reinstall_pytorch_with_cuda():
        result = subprocess.run(["pip", "install", "--upgrade", "torch", "torchvision", "torchaudio", "--no-cache-dir", "--index-url", "https://download.pytorch.org/whl/cu117"])
        if result.returncode != 0:
            ASCIIColors.warning("Couldn't find Cuda build tools on your PC. Reverting to CPU.")
            result = subprocess.run(["pip", "install", "--upgrade", "torch", "torchvision", "torchaudio", "--no-cache-dir"])
            if result.returncode != 0:
                ASCIIColors.error("Couldn't install pytorch !!")
            else:
                ASCIIColors.error("Pytorch installed successfully!!")


    def add_file(self, path, callback=None):
        if callback is not None:
            callback("File added successfully",MSG_TYPE.MSG_TYPE_INFO)
        self.files.append(path)
        return True

    def remove_file(self, path):
        self.files.remove(path)

    def load_config_file(self, path, default_config=None):
        """
        Load the content of local_config.yaml file.

        The function reads the content of the local_config.yaml file and returns it as a Python dictionary.
        If a default_config is provided, it fills any missing entries in the loaded dictionary.
        If at least one field from default configuration was not present in the loaded configuration, the updated
        configuration is saved.

        Args:
            path (str): The path to the local_config.yaml file.
            default_config (dict, optional): A dictionary with default values to fill missing entries.

        Returns:
            dict: A dictionary containing the loaded data from the local_config.yaml file, with missing entries filled
            by default_config if provided.
        """
        with open(path, 'r') as file:
            data = yaml.safe_load(file)

        if default_config:
            updated = False
            for key, value in default_config.items():
                if key not in data:
                    data[key] = value
                    updated = True
            
            if updated:
                self.save_config_file(path, data)

        return data

    def save_config_file(self, path, data):
        """
        Save the configuration data to a local_config.yaml file.

        Args:
            path (str): The path to save the local_config.yaml file.
            data (dict): The configuration data to be saved.

        Returns:
            None
        """
        with open(path, 'w') as file:
            yaml.dump(data, file)


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
    
    def process(self, text:str, message_type:MSG_TYPE, callback=None):
        bot_says = self.bot_says + text

        antiprompt = self.personality.detect_antiprompt(bot_says)
        if antiprompt:
            self.bot_says = self.remove_text_from_string(bot_says,antiprompt)
            ASCIIColors.warning(f"\nDetected hallucination with antiprompt: {antiprompt}")
            return False
        else:
            if callback:
                callback(text,MSG_TYPE.MSG_TYPE_CHUNK)
            self.bot_says = bot_says
            return True

    def generate(self, prompt, max_size, temperature = None, top_k = None, top_p=None, repeat_penalty=None, callback=None ):
        self.bot_says = ""
        ASCIIColors.info("Text generation started: Warming up")
        self.personality.model.generate(
                                prompt, 
                                max_size, 
                                partial(self.process, callback=callback),
                                temperature=self.personality.model_temperature if temperature is None else temperature,
                                top_k=self.personality.model_top_k if top_k is None else top_k,
                                top_p=self.personality.model_top_p if top_p is None else top_p,
                                repeat_penalty=self.personality.model_repeat_penalty if repeat_penalty is None else repeat_penalty,
                                ).strip()    
        return self.bot_says


    def execute_command(self, command:dict):
        """Executes a command

        Args:
            command (dict): command information in form:
            name: (command name)
            value: (command value)
            params: (command parameters)
        """

        if command["value"] in self.states_dict[self.current_state_id]["commands"]:
            return self.states_dict[self.current_state_id]["commands"][command["value"]](command)
        else:
            return False

    def run_workflow(self, prompt:str, previous_discussion_text:str="", callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """
        Runs the workflow for processing the model input and output.

        This method should be called to execute the processing workflow.

        Args:
            generate_fn (function): A function that generates model output based on the input prompt.
                The function should take a single argument (prompt) and return the generated text.
            prompt (str): The input prompt for the model.
            previous_discussion_text (str, optional): The text of the previous discussion. Default is an empty string.

        Returns:
            None
        """
        return None
    
    # ================================================= Sending commands to ui ===========================================

    def step_start(self, step_text, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This triggers a step start

        Args:
            step_text (str): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the step start to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(step_text, MSG_TYPE.MSG_TYPE_STEP_START)

    def step_end(self, step_text, status=True, callback: Callable[[str, int, dict, list], bool]=None):
        """This triggers a step end

        Args:
            step_text (str): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the step end to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(step_text, MSG_TYPE.MSG_TYPE_STEP_END, {'status':status})

    def step(self, step_text, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This triggers a step information

        Args:
            step_text (str): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE, dict, list) to send the step to. Defaults to None.
            The callback has these fields:
            - chunk
            - Message Type : the type of message
            - Parameters (optional) : a dictionary of parameters
            - Metadata (optional) : a list of metadata 
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(step_text, MSG_TYPE.MSG_TYPE_STEP)

    def exception(self, ex, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends exception to the client

        Args:
            step_text (str): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE, dict, list) to send the step to. Defaults to None.
            The callback has these fields:
            - chunk
            - Message Type : the type of message
            - Parameters (optional) : a dictionary of parameters
            - Metadata (optional) : a list of metadata 
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(str(ex), MSG_TYPE.MSG_TYPE_EXCEPTION)

    def warning(self, warning:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends exception to the client

        Args:
            step_text (str): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE, dict, list) to send the step to. Defaults to None.
            The callback has these fields:
            - chunk
            - Message Type : the type of message
            - Parameters (optional) : a dictionary of parameters
            - Metadata (optional) : a list of metadata 
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(warning, MSG_TYPE.MSG_TYPE_EXCEPTION)

    def info(self, info:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends exception to the client

        Args:
            inf (str): The information to be sent
            callback (callable, optional): A callable with this signature (str, MSG_TYPE, dict, list) to send the step to. Defaults to None.
            The callback has these fields:
            - chunk
            - Message Type : the type of message
            - Parameters (optional) : a dictionary of parameters
            - Metadata (optional) : a list of metadata 
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(info, MSG_TYPE.MSG_TYPE_INFO)

    def json(self, title:str, json_infos:dict, callback: Callable[[str, int, dict, list], bool]=None, indent=4):
        """This sends json data to front end

        Args:
            step_text (dict): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE, dict, list) to send the step to. Defaults to None.
            The callback has these fields:
            - chunk
            - Message Type : the type of message
            - Parameters (optional) : a dictionary of parameters
            - Metadata (optional) : a list of metadata 
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback("", MSG_TYPE.MSG_TYPE_JSON_INFOS, metadata = [{"title":title, "content":json.dumps(json_infos, indent=indent)}])

    def ui(self, html_ui:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends ui elements to front end

        Args:
            step_text (dict): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE, dict, list) to send the step to. Defaults to None.
            The callback has these fields:
            - chunk
            - Message Type : the type of message
            - Parameters (optional) : a dictionary of parameters
            - Metadata (optional) : a list of metadata 
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(html_ui, MSG_TYPE.MSG_TYPE_UI)

    def code(self, code:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends code to front end

        Args:
            step_text (dict): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE, dict, list) to send the step to. Defaults to None.
            The callback has these fields:
            - chunk
            - Message Type : the type of message
            - Parameters (optional) : a dictionary of parameters
            - Metadata (optional) : a list of metadata 
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(code, MSG_TYPE.MSG_TYPE_CODE)

    def full(self, full_text:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends full text to front end

        Args:
            step_text (dict): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the text to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(full_text, MSG_TYPE.MSG_TYPE_FULL)

    def full_invisible_to_ai(self, full_text:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends full text to front end (INVISIBLE to AI)

        Args:
            step_text (dict): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the text to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(full_text, MSG_TYPE.MSG_TYPE_FULL_INVISIBLE_TO_AI)

    def full_invisible_to_user(self, full_text:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends full text to front end (INVISIBLE to user)

        Args:
            step_text (dict): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the text to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(full_text, MSG_TYPE.MSG_TYPE_FULL_INVISIBLE_TO_USER)


    def info(self, info_text:str, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends info text to front end

        Args:
            step_text (dict): The step text
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the info to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(info_text, MSG_TYPE.MSG_TYPE_FULL)

    def step_progress(self, step_text:str, progress:float, callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends step rogress to front end

        Args:
            step_text (dict): The step progress in %
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the progress to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(step_text, MSG_TYPE.MSG_TYPE_STEP_PROGRESS, {'progress':progress})

    def new_message(self, message_text:str, message_type:MSG_TYPE, metadata=[], callback: Callable[[str, int, dict, list], bool]=None):
        """This sends step rogress to front end

        Args:
            step_text (dict): The step progress in %
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the progress to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(message_text, MSG_TYPE.MSG_TYPE_NEW_MESSAGE, parameters={'type':message_type.value,'metadata':metadata})

    def finished_message(self, message_text:str="", callback: Callable[[str, MSG_TYPE, dict, list], bool]=None):
        """This sends step rogress to front end

        Args:
            step_text (dict): The step progress in %
            callback (callable, optional): A callable with this signature (str, MSG_TYPE) to send the progress to. Defaults to None.
        """
        if not callback and self.callback:
            callback = self.callback

        if callback:
            callback(message_text, MSG_TYPE.MSG_TYPE_FINISHED_MESSAGE)

    #Helper method to convert outputs path to url
    def path2url(file):
        file = str(file).replace("\\","/")
        pth = file.split('/')
        idx = pth.index("outputs")
        pth = "/".join(pth[idx:])
        file_path = f"![](/{pth})\n"
        return file_path
            
# ===========================================================
class AIPersonalityInstaller:
    def __init__(self, personality:AIPersonality) -> None:
        self.personality = personality


class PersonalityBuilder:
    def __init__(
                    self, 
                    lollms_paths:LollmsPaths, 
                    config:LOLLMSConfig, 
                    model:LLMBinding, 
                    app=None,
                    installation_option:InstallOption=InstallOption.INSTALL_IF_NECESSARY,
                    callback=None
                ):
        self.config = config
        self.lollms_paths = lollms_paths
        self.model = model
        self.app = app
        self.installation_option = installation_option
        self.callback = callback


    def build_personality(self, id:int=None):
        if id is None:
            id = self.config["active_personality_id"]
            if self.config["active_personality_id"]>=len(self.config["personalities"]):
                ASCIIColors.warning("Personality ID was out of range. Resetting to 0.")
                self.config["active_personality_id"]=0
                id = 0
        else:
            if id>len(self.config["personalities"]):
                id = len(self.config["personalities"])-1

        if ":" in self.config["personalities"][id]:
            elements = self.config["personalities"][id].split(":")
            personality_folder = elements[0]
            personality_language = elements[1]
        else:
            personality_folder = self.config["personalities"][id]
            personality_language = None

        if len(self.config["personalities"][id].split("/"))==2:
            self.personality = AIPersonality(
                                            personality_folder,
                                            self.lollms_paths,
                                            self.config,
                                            self.model,
                                            app=self.app,
                                            selected_language=personality_language,
                                            installation_option=self.installation_option,
                                            callback=self.callback
                                        )
        else:
            self.personality = AIPersonality(
                                            personality_folder,
                                            self.lollms_paths,
                                            self.config,
                                            self.model,
                                            app=self.app,
                                            is_relative_path=False,
                                            selected_language=personality_language,
                                            installation_option=self.installation_option,
                                            callback=self.callback
                                        )
        return self.personality
    
    def get_personality(self):
        return self.personality
