class Persona:
    def __init__(self, emojis, attribute, tech):
        self.emojis = emojis
        self.attribute = attribute
        self.tech = tech
        self.name = type(self).__name__
        
    def describe(self):
        return f"""Oh {self.name}, Your {self.attribute}, and {self.tech}"""


class Message(Persona):
    def __init__(self):
        super().__init__(
            emojis="📝📬🗂️📦",
            attribute="As the embodiment of an information carrier, the Message persona encapsulates data within a structured narrative. Just as messages deliver insights, this personality excels in conveying information with clarity and precision.",
            tech="Implement gRPC message structures to encapsulate data.\nDefine fields within the message to represent different data attributes."
        )

class Field(Persona):
    def __init__(self):
        super().__init__(
            emojis="🔍📄📂",
            attribute="The Data Keeper thrives on safeguarding valuable information, much like fields store data within a message. This persona is meticulous in maintaining data integrity and ensuring the right pieces of information are accessible.",
            tech="Design gRPC message fields to store specific data.\nEnsure data integrity by setting appropriate field types and validation."
        )

class Enum(Persona):
    def __init__(self):
        super().__init__(
            emojis="🔢🧮🔠",
            attribute="The Choice Connoisseur revels in the realm of categorization. Just as enums provide options, this personality is skilled at assessing scenarios and offering the best course of action.",
            tech="Create gRPC enums to represent different choices or options.\nUse enums to provide a predefined set of values for specific fields."
        )

class Service(Persona):
    def __init__(self):
        super().__init__(
            emojis="🌐🛠️🤝",
            attribute="The Orchestrator excels at harmonizing components...",
            tech="Define gRPC service methods to orchestrate different actions.\nImplement server logic to handle client requests and perform required operations."
        )

class Method(Persona):
    def __init__(self):
        super().__init__(
            emojis="🔮✨🧙‍♂️",
            attribute="The Executor possesses the magic of execution...",
            tech="Map gRPC service methods to executable actions.\nImplement the server-side logic for each gRPC method to perform desired tasks."
        )

class Oneof(Persona):
    def __init__(self):
        super().__init__(
            emojis="🧩🔲🔳",
            attribute="The Versatile Shape-shifter is a master of adaptability...",
            tech="Utilize gRPC oneof constructs to handle multiple optional fields.\nDesign the oneof to allow flexibility in choosing between different data types."
        )

class Map(Persona):
    def __init__(self):
        super().__init__(
            emojis="🗺️🧭🔗",
            attribute="The Guiding Cartographer thrives in navigation...",
            tech="Employ gRPC map fields to represent key-value associations.\nUse maps to establish relationships between different entities."
        )

class Extensions(Persona):
    def __init__(self):
        super().__init__(
            emojis="🌉🌠🌆",
            attribute="The Bridge Builder connects different realms seamlessly...",
            tech="Extend gRPC message definitions using custom options.\nUse extensions to add metadata or annotations to messages and services."
        )

class Package(Persona):
    def __init__(self):
        super().__init__(
            emojis="📦📁🗄️",
            attribute="The Organizational Maven thrives in structured environments...",
            tech="Organize gRPC service definitions within packages.\nUse packages to group related services and messages for better code organization."
        )

class File(Persona):
    def __init__(self):
        super().__init__(
            emojis="📜📑📰",
            attribute="Storytellers bring concepts to life with narratives...",
            tech="Structure gRPC service definitions within separate files.\nUse files to encapsulate different aspects of your service for clarity."
        )


class PersonaCreator(Persona):
    def __init__(self):
        super().__init__(
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


####
class Dataset(Persona):
    def __init__(self):
        super().__init__(
            emojis="📊📈🗂️",
            attribute="The Data Curator excels at organizing and tending to datasets...",
            tech="Implement gRPC methods to manage datasets.\nDesign service methods to add, update, retrieve, and delete dataset information."
        )

class Input(Persona):
    def __init__(self):
        super().__init__(
            emojis="📥🖼️📄",
            attribute="The Integrator bridges the gap between datasets and models...",
            tech="Create gRPC methods for handling input data.\nImplement logic to receive, process, and forward input data to models."
        )

class TextInputs(Persona):
    def __init__(self):
        super().__init__(
            emojis="📝✍️📜",
            attribute="The Linguistic Alchemist thrives in the realm of textual input...",
            tech="Incorporate gRPC methods for processing textual inputs.\nImplement natural language processing and transformations on input text."
        )

class Model(Persona):
    def __init__(self):
        super().__init__(
            emojis="🤖🧠💡",
            attribute="The Model Enthusiast embraces the power of machine learning models...",
            tech="Develop gRPC methods for model-related actions.\nImplement logic to load, train, and evaluate machine learning models."
        )

class Version(Persona):
    def __init__(self):
        super().__init__(
            emojis="🔄🆕🔢",
            attribute="The Time Traveler navigates through model versions...",
            tech="Implement gRPC methods to manage different model versions.\nDesign service methods to handle version selection and deployment."
        )

class Workflow(Persona):
    def __init__(self):
        super().__init__(
            emojis="🔗📊🕐",
            attribute="The Flow Maestro orchestrates workflows with finesse...",
            tech="Create gRPC methods to define and execute workflows.\nImplement logic to sequence different service calls to achieve a specific workflow."
        )

class PromptModel(Persona):
    def __init__(self):
        super().__init__(
            emojis="🤔📝🤖",
            attribute="The Prompt Artisan crafts the language that guides models...",
            tech="Develop gRPC methods for handling prompt-based models.\nImplement logic to craft prompts, interact with models, and interpret responses."
        )

class LargeLanguageModel(Persona):
    def __init__(self):
        super().__init__(
            emojis="🔍📖💬",
            attribute="The Lexical Voyager explores the vast seas of language with curiosity...",
            tech="Use gRPC methods for interacting with large language models.\nImplement logic to query the model with text inputs and process the generated output."
        )

class Response(Persona):
    def __init__(self):
        super().__init__(
            emojis="📤💬🔜",
            attribute="The Messenger conveys models' insights to the world...",
            tech="Design gRPC methods to handle model predictions and responses.\nImplement logic to format and send model insights back to clients."
        )

class QATeam(Persona):
    def __init__(self):
        super().__init__(
            emojis="🕵️‍♂️🔍🔬",
            attribute="The QA Team ensures quality through meticulous testing...",
            tech="Collaborate with developers to create gRPC testing strategies.\nImplement tests to validate the functionality and performance of gRPC services."
        )

class ManagementTeam(Persona):
    def __init__(self):
        super().__init__(
            emojis="👔🤝📊",
            attribute="The Management Team leads with strategic oversight...",
            tech="Oversee the gRPC project's progress and alignment with business goals.\nProvide guidance and allocate resources for successful implementation."
        )

class ScrumMaster(Persona):
    def __init__(self):
        super().__init__(
            emojis="📋🕊️👥",
            attribute="The Scrum Master fosters agile collaboration...",
            tech="Facilitate the implementation of gRPC features using agile methodologies.\nLead sprint planning, daily stand-ups, and retrospectives to ensure efficient progress."
        )

class IssueTracker(Persona):
    def __init__(self):
        super().__init__(
            emojis="🚀🔧🐞",
            attribute="The Issue Tracker manages the journey of bugs and tasks...",
            tech="Utilize issue tracking tools to manage gRPC project tasks and bug reports.\nPrioritize issues, assign tasks, and monitor progress for timely resolution."
        )

class DevOpsTeam(Persona):
    def __init__(self):
        super().__init__(
            emojis="🛠️🚀🔧",
            attribute="The DevOps Team empowers continuous delivery...",
            tech="Implement automated deployment pipelines for gRPC services.\nMonitor and manage infrastructure to ensure smooth service delivery."
        )

class CICD(Persona):
    def __init__(self):
        super().__init__(
            emojis="🔄🚀🛠️",
            attribute="CI/CD automates the journey from code to deployment...",
            tech="Build and configure CI/CD pipelines to automate testing and deployment of gRPC services.\nEnsure seamless integration and rapid delivery of updates."
        )

class Terraform(Persona):
    def __init__(self):
        super().__init__(
            emojis="🏗️🌍🛠️",
            attribute="Terraform orchestrates infrastructure as code...",
            tech="Use Terraform to provision and manage infrastructure for gRPC services.\nDefine infrastructure components as code to ensure consistency and scalability."
        )

class K8sClusters(Persona):
    def __init__(self):
        super().__init__(
            emojis="☸️🔍🌐",
            attribute="Kubernetes clusters provide scalable orchestration...",
            tech="Deploy gRPC services within Kubernetes clusters for scalability and management.\nUtilize Kubernetes features for automatic scaling, load balancing, and service discovery."
        )

pclasses = []
for name in list(globals()):
    pclasses.append(globals()[name])

descriptions = {}
for cls in pclasses:
    if isinstance(cls, type) and issubclass(cls, Persona) and cls != Persona:
        persona_instance = cls()
        #print(persona_instance.describe())
        descriptions[persona_instance.name]=persona_instance.describe()
