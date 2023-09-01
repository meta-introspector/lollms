######
# Project       : lollms
# File          : binding.py
# Author        : ParisNeo with the help of the community
# Supported by Nomic-AI
# license       : Apache 2.0
# Description   : 
# This is an interface class for lollms bindings.
######
from pathlib import Path
from typing import Callable
from lollms.paths import LollmsPaths
from lollms.helpers import ASCIIColors

import tempfile
import requests
import shutil
import os
import yaml
from tqdm import tqdm
import importlib
import subprocess
from lollms.config import TypedConfig, InstallOption
from lollms.main_config import LOLLMSConfig
import traceback
import urllib

__author__ = "parisneo"
__github__ = "https://github.com/ParisNeo/lollms_bindings_zoo"
__copyright__ = "Copyright 2023, "
__license__ = "Apache 2.0"


class LLMBinding:
    
    def __init__(
                    self,
                    binding_dir:Path,
                    lollms_paths:LollmsPaths,
                    config:LOLLMSConfig, 
                    binding_config:TypedConfig,
                    installation_option:InstallOption=InstallOption.INSTALL_IF_NECESSARY,
                    file_extension='*.bin'
                ) -> None:
        
        self.binding_dir            = binding_dir
        self.binding_folder_name    = binding_dir.stem
        self.lollms_paths           = lollms_paths
        self.config                 = config
        self.binding_config         = binding_config
        self.file_extension         = file_extension
        self.seed                   = config["seed"]

        self.configuration_file_path = lollms_paths.personal_configuration_path/f"binding_{self.binding_folder_name}.yaml"
        self.binding_config.config.file_path = self.configuration_file_path

        # Installation
        if (not self.configuration_file_path.exists() or installation_option==InstallOption.FORCE_INSTALL) and installation_option!=InstallOption.NEVER_INSTALL:
            self.install()
            self.binding_config.config.save_config()
        else:
            self.load_binding_config()

        self.models_folder = config.lollms_paths.personal_models_path / self.binding_folder_name
        self.models_folder.mkdir(parents=True, exist_ok=True)

    def __str__(self) -> str:
        return self.config["binding_name"]+f"({self.config['model_name']})"
    
    def download_and_install_wheel(self, url):
        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        try:
            # Download the wheel file
            response = requests.get(url)
            if response.status_code == 200:
                # Save the downloaded file to the temporary directory
                wheel_path = os.path.join(temp_dir, 'package.whl')
                with open(wheel_path, 'wb') as file:
                    file.write(response.content)

                # Install the wheel file using pip
                subprocess.check_call(['pip', 'install', wheel_path])

                # Clean up the temporary directory
                shutil.rmtree(temp_dir)
                print('Installation completed successfully.')
            else:
                print('Failed to download the file.')

        except Exception as e:
            print('An error occurred during installation:', str(e))
            shutil.rmtree(temp_dir)

    def get_file_size(self, url):
        # Send a HEAD request to retrieve file metadata
        response = urllib.request.urlopen(url)
        
        # Extract the Content-Length header value
        file_size = response.headers.get('Content-Length')
        
        # Convert the file size to integer
        if file_size:
            file_size = int(file_size)
        
        return file_size
    
    def build_model(self):
        """
        Build the model.

        This method is responsible for constructing the model for the LOLLMS class.

        Returns:
            the model
        """        
        return None
    
    def destroy_model(self):
        """
        destroys the current model
        """
        pass

    def install(self):
        """
        Installation procedure (to be implemented)
        """
        ASCIIColors.blue("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")
        ASCIIColors.red(f"Installing {self.binding_folder_name}")
        ASCIIColors.blue("*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*")


    def get_model_path(self):
        """
        Retrieves the path of the model based on the configuration.

        If the model name ends with ".reference", it reads the model path from a file.
        Otherwise, it constructs the model path based on the configuration.

        Returns:
            str: The path of the model.
        """
        if self.config.model_name is None:
            return None
        
        if self.config.model_name.endswith(".reference"):
            ASCIIColors.yellow("Loading a reference model:")
            file_path = self.lollms_paths.personal_models_path / f"{self.binding_folder_name}/{self.config.model_name}"
            if file_path.exists():
                with open(str(file_path), 'r') as f:
                    model_path = Path(f.read())
                ASCIIColors.yellow(model_path)
            else:
                return None
        else:
            model_path = Path(self.lollms_paths.personal_models_path / f"{self.binding_folder_name}/{self.config.model_name}")

        return model_path

    
    def get_current_seed(self):
        return self.seed
    
    def load_binding_config(self):
        """
        Load the content of local_config.yaml file.

        The function reads the content of the local_config.yaml file and returns it as a Python dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the loaded data from the local_config.yaml file.
        """
        try:
            self.binding_config.config.load_config()
        except:
            self.binding_config.config.save_config()
        self.binding_config.sync()

    def save_config_file(self, path):
        """
        Load the content of local_config.yaml file.

        The function reads the content of the local_config.yaml file and returns it as a Python dictionary.

        Args:
            None

        Returns:
            dict: A dictionary containing the loaded data from the local_config.yaml file.
        """
        raise Exception("NO!")
        #self.binding_config.config.save_config(self.configuration_file_path)

    


    def generate(self, 
                 prompt:str,
                 n_predict: int = 128,
                 callback: Callable[[str, int, dict], bool] = None,
                 verbose: bool = False,
                 **gpt_params ):
        """Generates text out of a prompt
        This should ber implemented by child class

        Args:
            prompt (str): The prompt to use for generation
            n_predict (int, optional): Number of tokens to prodict. Defaults to 128.
            callback (Callable[[str, int, dict], None], optional): A callback function that is called everytime a new text element is generated. Defaults to None.
            verbose (bool, optional): If true, the code will spit many informations about the generation process. Defaults to False.
        """
        pass
    def tokenize(self, prompt:str):
        """
        Tokenizes the given prompt using the model's tokenizer.

        Args:
            prompt (str): The input prompt to be tokenized.

        Returns:
            list: A list of tokens representing the tokenized prompt.
        """
        return prompt.split(" ")

    def detokenize(self, tokens_list:list):
        """
        Detokenizes the given list of tokens using the model's tokenizer.

        Args:
            tokens_list (list): A list of tokens to be detokenized.

        Returns:
            str: The detokenized text as a string.
        """
        return " ".join(tokens_list)


    def embed(self, text):
        """
        Computes text embedding
        Args:
            text (str): The text to be embedded.
        Returns:
            List[float]
        """
        pass

    def list_models(self, config:dict):
        """Lists the models for this binding
        """
        models_dir = self.lollms_paths.personal_models_path/config["binding_name"]  # replace with the actual path to the models folder
        return [f.name for f in models_dir.iterdir() if f.suffix == self.file_extension.replace("*","") or f.suffix==".reference"]

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


    # To implement by children
    # @staticmethod
    # def get_available_models():


# ===============================

class BindingBuilder:
    def build_binding(
                        self, 
                        config: LOLLMSConfig, 
                        lollms_paths:LollmsPaths,
                        installation_option:InstallOption=InstallOption.INSTALL_IF_NECESSARY
                    )->LLMBinding:
        
        if len(str(config.binding_name).split("/"))>1:
            binding_path = Path(config.binding_name)
        else:
            binding_path = lollms_paths.bindings_zoo_path / config["binding_name"]

        # define the full absolute path to the module
        absolute_path = binding_path.resolve()
        # infer the module name from the file path
        module_name = binding_path.stem
        # use importlib to load the module from the file path
        loader = importlib.machinery.SourceFileLoader(module_name, str(absolute_path / "__init__.py"))
        binding_module = loader.load_module()
        binding:LLMBinding = getattr(binding_module, binding_module.binding_name)
        return binding(
                config,
                lollms_paths=lollms_paths,
                installation_option = installation_option
                )
    
class ModelBuilder:
    def __init__(self, binding:LLMBinding):
        self.binding = binding
        self.model = None
        self.build_model() 

    def build_model(self):
        self.model = self.binding.build_model()

    def get_model(self):
        return self.model

