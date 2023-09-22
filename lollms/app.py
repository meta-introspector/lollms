from lollms.main_config import LOLLMSConfig
from lollms.helpers import ASCIIColors
from lollms.paths import LollmsPaths
from lollms.personality import PersonalityBuilder
from lollms.binding import LLMBinding, BindingBuilder, ModelBuilder
from lollms.config import InstallOption
from lollms.helpers import trace_exception
from lollms.terminal import MainMenu
from typing import Callable
import pprint
import subprocess

class LollmsApplication:
    def __init__(
                    self, 
                    app_name:str, 
                    config:LOLLMSConfig, 
                    lollms_paths:LollmsPaths, 
                    load_binding=True, 
                    load_model=True, 
                    try_select_binding=False, 
                    try_select_model=False,
                    callback=None
                ) -> None:
        """
        Creates a LOLLMS Application
        """
        self.app_name               = app_name
        self.config                 = config
        self.lollms_paths           = lollms_paths

        self.menu                   = MainMenu(self, callback)
        self.mounted_personalities  = []
        self.personality            = None

        self.binding=None
        self.model=None

        try:
            if config.auto_update:
                pprint.pprint(config.to_dict())
                #pprint.pprint(dir(config))
                raise Exception("why is this on?")
                ASCIIColors.info("Bindings zoo found in your personal space.\nPulling last personalities zoo")
                subprocess.run(["git", "-C", self.lollms_paths.bindings_zoo_path, "pull"])            
                # Pull the repository if it already exists
                ASCIIColors.info("Personalities zoo found in your personal space.\nPulling last personalities zoo")
                subprocess.run(["git", "-C", self.lollms_paths.personalities_zoo_path, "pull"])            
                # Pull the repository if it already exists
                ASCIIColors.info("Extensions zoo found in your personal space.\nPulling last Extensions zoo")
                subprocess.run(["git", "-C", self.lollms_paths.extensions_zoo_path, "pull"])            
                # Pull the repository if it already exists
                ASCIIColors.info("Qlora found in your personal space.\nPulling last qlora code")
                subprocess.run(["git", "-C", self.lollms_paths.gptqlora_path, "pull"])            
        except Exception as ex:
            ASCIIColors.error("Couldn't pull zoos. Please contact the main dev on our discord channel and report the problem.")
            trace_exception(ex)

        if self.config.binding_name is None:
            ASCIIColors.warning(f"No binding selected")
            if try_select_binding:
                ASCIIColors.info("Please select a valid model or install a new one from a url")
                self.menu.select_binding()
        else:
            if load_binding:
                try:
                    ASCIIColors.info(f">Loading binding {self.config.binding_name}. Please wait ...")
                    self.binding            = self.load_binding()
                except Exception as ex:
                    ASCIIColors.error(f"Failed to load binding.\nReturned exception: {ex}")
                    trace_exception(ex)

                if self.binding is not None:
                    ASCIIColors.success(f"Binding {self.config.binding_name} loaded successfully.")
                    if load_model:
                        if self.config.model_name is None:
                            ASCIIColors.warning(f"No model selected")
                            if try_select_model:
                                print("Please select a valid model")
                                self.menu.select_model()
                                
                        if self.config.model_name is not None:
                            try:
                                ASCIIColors.info(f">Loading model {self.config.model_name}. Please wait ...")
                                self.model          = self.load_model()
                                if self.model is not None:
                                    ASCIIColors.success(f"Model {self.config.model_name} loaded successfully.")

                            except Exception as ex:
                                ASCIIColors.error(f"Failed to load model.\nReturned exception: {ex}")
                                trace_exception(ex)
                else:
                    ASCIIColors.warning(f"Couldn't load binding {self.config.binding_name}.")

            
        self.mount_personalities()

    def load_binding(self):
        try:
            binding = BindingBuilder().build_binding(self.config, self.lollms_paths)
            return binding    
        except Exception as ex:
            print(ex)
            print(f"Couldn't find binding. Please verify your configuration file at {self.lollms_paths.personal_configuration_path}/local_configs.yaml or use the next menu to select a valid binding")
            print(f"Trying to reinstall binding")
            try:
                binding = BindingBuilder().build_binding(self.config, self.lollms_paths,installation_option=InstallOption.FORCE_INSTALL)
            except Exception as ex:
                ASCIIColors.error("Couldn't reinstall model")
                trace_exception(ex)
            return None    

    
    def load_model(self):
        try:
            model = ModelBuilder(self.binding).get_model()
                
            for personality in self.mounted_personalities:
                if personality is not None:
                    personality.model = model
        except Exception as ex:
            ASCIIColors.error(f"Couldn't load model. Please verify your configuration file at {self.lollms_paths.personal_configuration_path} or use the next menu to select a valid model")
            ASCIIColors.error(f"Binding returned this exception : {ex}")
            trace_exception(ex)
            ASCIIColors.error(f"{self.config.get_model_path_infos()}")
            print("Please select a valid model or install a new one from a url")
            model = None

        return model


    def mount_personality(self, id:int, callback=None):
        try:
            personality = PersonalityBuilder(self.lollms_paths, self.config, self.model, self, callback=callback).build_personality(id)
            if personality.model is not None:
                self.cond_tk = personality.model.tokenize(personality.personality_conditioning)
                self.n_cond_tk = len(self.cond_tk)
                ASCIIColors.success(f"Personality  {personality.name} mounted successfully")
            else:
                if personality.selected_language is not None:
                    ASCIIColors.success(f"Personality  {personality.name} : {personality.selected_language} mounted successfully but no model is selected")
                else:
                    ASCIIColors.success(f"Personality  {personality.name} mounted successfully but no model is selected")
        except Exception as ex:
            ASCIIColors.error(f"Couldn't load personality. Please verify your configuration file at {self.lollms_paths.personal_configuration_path} or use the next menu to select a valid personality")
            ASCIIColors.error(f"Binding returned this exception : {ex}")
            trace_exception(ex)
            ASCIIColors.error(f"{self.config.get_personality_path_infos()}")
            if id == self.config.active_personality_id:
                self.config.active_personality_id=len(self.config.personalities)-1
            personality = None
        
        self.mounted_personalities.append(personality)

        return personality
    
    def mount_personalities(self, callback = None):
        #import pdb
        #pdb.set_trace()
        self.mounted_personalities = []
        to_remove = []
        for i in range(len(self.config["personalities"])):
            print("mounting", i)
            p = self.mount_personality(i, callback = None)
            if p is None:
                to_remove.append(i)
        to_remove.sort(reverse=True)
        for i in to_remove:
            self.unmount_personality(i)


        if self.config.active_personality_id>=0 and self.config.active_personality_id<len(self.mounted_personalities):
            self.personality = self.mounted_personalities[self.config.active_personality_id]
        else:
            if len(self.mounted_personalities)>0:
                self.config["personalities"].insert(0, "generic/lollms")
                self.mount_personality(0, callback = None)
                self.config.active_personality_id = 0
                self.personality = self.mounted_personalities[self.config.active_personality_id]

        if not self.personality:
            raise Exception("missing personality")

    def set_personalities_callbacks(self, callback: Callable[[str, int, dict], bool]=None):
        for personality in self.mount_personalities:
            personality.setCallback(callback)

            
    def unmount_personality(self, id:int)->bool:
        if id<len(self.config.personalities):
            del self.config.personalities[id]
            del self.mounted_personalities[id]
            if self.config.active_personality_id>=id:
                self.config.active_personality_id-=1

            self.config.save_config()
            return True
        else:
            return False


    def select_personality(self, id:int):
        if id<len(self.config.personalities):
            self.config.active_personality_id = id
            self.personality = self.mounted_personalities[id]
            self.config.save_config()
            return True
        else:
            return False


    def load_personality(self, callback=None):
        try:
            personality = PersonalityBuilder(self.lollms_paths, self.config, self.model, self, callback=callback).build_personality()
        except Exception as ex:
            ASCIIColors.error(f"Couldn't load personality. Please verify your configuration file at {self.configuration_path} or use the next menu to select a valid personality")
            ASCIIColors.error(f"Binding returned this exception : {ex}")
            ASCIIColors.error(f"{self.config.get_personality_path_infos()}")
            print("Please select a valid model or install a new one from a url")
            personality = None
        return personality

    @staticmethod   
    def reset_paths(lollms_paths:LollmsPaths):
        lollms_paths.resetPaths()

    @staticmethod   
    def reset_all_installs(lollms_paths:LollmsPaths):
        ASCIIColors.info("Removeing all configuration files to force reinstall")
        ASCIIColors.info(f"Searching files from {lollms_paths.personal_configuration_path}")
        for file_path in lollms_paths.personal_configuration_path.iterdir():
            if file_path.name!=f"{lollms_paths.tool_prefix}local_config.yaml" and file_path.suffix.lower()==".yaml":
                file_path.unlink()
                ASCIIColors.info(f"Deleted file: {file_path}")
