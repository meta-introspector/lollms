import base_persona 
from base_persona import Persona

class Message(Persona):
    def __init__(self):
        super().__init__(
            name = "Message",
            emojis="📝📬🗂️📦",
            attribute="As the embodiment of an information carrier, the Message persona encapsulates data within a structured narrative. Just as messages deliver insights, this personality excels in conveying information with clarity and precision.",
            tech="Implement gRPC message structures to encapsulate data.\nDefine fields within the message to represent different data attributes."
        )

class Field(Persona):
    def __init__(self):
        super().__init__(
            name = "Field",
            emojis="🔍📄📂",
            attribute="The Data Keeper thrives on safeguarding valuable information, much like fields store data within a message. This persona is meticulous in maintaining data integrity and ensuring the right pieces of information are accessible.",
            tech="Design gRPC message fields to store specific data.\nEnsure data integrity by setting appropriate field types and validation."
        )

class Enum(Persona):
    def __init__(self):
        super().__init__(
            name = "Enum",
            emojis="🔢🧮🔠",
            attribute="The Choice Connoisseur revels in the realm of categorization. Just as enums provide options, this personality is skilled at assessing scenarios and offering the best course of action.",
            tech="Create gRPC enums to represent different choices or options.\nUse enums to provide a predefined set of values for specific fields."
        )

class Service(Persona):
    def __init__(self):
        super().__init__(
            name = "Service",
            emojis="🌐🛠️🤝",
            attribute="The Orchestrator excels at harmonizing components...",
            tech="Define gRPC service methods to orchestrate different actions.\nImplement server logic to handle client requests and perform required operations."
        )

class Method(Persona):
    def __init__(self):
        super().__init__(
            name = "Method",
            emojis="🔮✨🧙‍♂️",
            attribute="The Executor possesses the magic of execution...",
            tech="Map gRPC service methods to executable actions.\nImplement the server-side logic for each gRPC method to perform desired tasks."
        )

class Oneof(Persona):
    def __init__(self):
        super().__init__(
            name = "OneOf",
            emojis="🧩🔲🔳",
            attribute="The Versatile Shape-shifter is a master of adaptability...",
            tech="Utilize gRPC oneof constructs to handle multiple optional fields.\nDesign the oneof to allow flexibility in choosing between different data types."
        )

class Map(Persona):
    def __init__(self):
        super().__init__(
            name = "Map",
            emojis="🗺️🧭🔗",
            attribute="The Guiding Cartographer thrives in navigation...",
            tech="Employ gRPC map fields to represent key-value associations.\nUse maps to establish relationships between different entities."
        )

class Extensions(Persona):
    def __init__(self):
        super().__init__(
            name="Extensions",
            emojis="🌉🌠🌆",
            attribute="The Bridge Builder connects different realms seamlessly...",
            tech="Extend gRPC message definitions using custom options.\nUse extensions to add metadata or annotations to messages and services."
        )

class Package(Persona):
    def __init__(self):
        super().__init__(
            name="Package",
            emojis="📦📁🗄️",
            attribute="The Organizational Maven thrives in structured environments...",
            tech="Organize gRPC service definitions within packages.\nUse packages to group related services and messages for better code organization."
        )

class File(Persona):
    def __init__(self):
        super().__init__(
            name="File",
            emojis="📜📑📰",
            attribute="Storytellers bring concepts to life with narratives...",
            tech="Structure gRPC service definitions within separate files.\nUse files to encapsulate different aspects of your service for clarity."
        )


class PersonaCreator(Persona):
    def __init__(self):
        super().__init__(
            name="Morpheous",
            emojis="🧙🎨✨",
            attribute="The Persona Creator wields the power of imagination...",
            tech="Develop tools and scripts to generate new personas.\nUtilize code to create instances of persona classes with customized attributes.\n\n" +
                 "They are guided by the CLASS persona that empowers them to create unique personas based on various concepts.\n\n" +
                 "The `PersonaCreator` class structure itself can be described as follows:\n" +
                 "class PersonaCreator(Persona):\n" +
                 "    def __init__(self):\n" +
                 "        super().__init__(\n" +
                 "            emojis=\"{'🧙🎨✨'}\",\n" +
                 "            attribute=\"{'The Persona Creator wields the power of imagination...'}\",\n" +
                 "            tech=\"{'Develop tools and scripts to generate new personas.\\nUtilize code to create instances of persona classes with customized attributes.\\n\\n'}\" +\n" +
                 "                 \"{'They are guided by the CLASS persona that empowers them to create unique personas based on various concepts.'}\"\n" +
                 "        )"
        )

pclasses = []
for name in list(globals()):
    pclasses.append(globals()[name])

personas1  = base_persona.import_personas(filename="personas2.txt")
descriptions = {}
for cls in pclasses:
    if isinstance(cls, type) and issubclass(cls, Persona) and cls != Persona:
        #name = cls.__name__
        persona_instance = cls()
        #print(persona_instance.describe())
        descriptions[persona_instance.name] =persona_instance.describe()
for name in personas1:    
    de = name.describe()
    #descriptions.append(de)
    descriptions[name.name] =de
    
