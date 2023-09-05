
####
class Dataset(Persona):
    def __init__(self):
        super().__init__(
            name="Dataset",
            emojis="📊📈🗂️",
            attribute="The Data Curator excels at organizing and tending to datasets...",
            tech="Implement gRPC methods to manage datasets.\nDesign service methods to add, update, retrieve, and delete dataset information."
        )

class Input(Persona):
    def __init__(self):
        super().__init__(
            name="Input",
            emojis="📥🖼️📄",
            attribute="The Integrator bridges the gap between datasets and models...",
            tech="Create gRPC methods for handling input data.\nImplement logic to receive, process, and forward input data to models."
        )

class TextInputs(Persona):
    def __init__(self):
        super().__init__(
            name="TextInputs",
            emojis="📝✍️📜",
            attribute="The Linguistic Alchemist thrives in the realm of textual input...",
            tech="Incorporate gRPC methods for processing textual inputs.\nImplement natural language processing and transformations on input text."
        )

class Model(Persona):
    def __init__(self):
        super().__init__(
            name="Model",
            emojis="🤖🧠💡",
            attribute="The Model Enthusiast embraces the power of machine learning models...",
            tech="Develop gRPC methods for model-related actions.\nImplement logic to load, train, and evaluate machine learning models."
        )

class Version(Persona):
    def __init__(self):
        super().__init__(
            name="Model Version",
            emojis="🔄🆕🔢",
            attribute="The Time Traveler navigates through model versions...",
            tech="Implement gRPC methods to manage different model versions.\nDesign service methods to handle version selection and deployment."
        )

class Workflow(Persona):
    def __init__(self):
        super().__init__(
            name="Workflow",
            emojis="🔗📊🕐",
            attribute="The Flow Maestro orchestrates workflows with finesse...",
            tech="Create gRPC methods to define and execute workflows.\nImplement logic to sequence different service calls to achieve a specific workflow."
        )

class PromptModel(Persona):
    def __init__(self):
        super().__init__(
            name="PromptModel",
            emojis="🤔📝🤖",
            attribute="The Prompt Artisan crafts the language that guides models...",
            tech="Develop gRPC methods for handling prompt-based models.\nImplement logic to craft prompts, interact with models, and interpret responses."
        )

class LargeLanguageModel(Persona):
    def __init__(self):
        super().__init__(
            name="LargeLanguageModel",
            emojis="🔍📖💬",
            attribute="The Lexical Voyager explores the vast seas of language with curiosity...",
            tech="Use gRPC methods for interacting with large language models.\nImplement logic to query the model with text inputs and process the generated output."
        )

class Response(Persona):
    def __init__(self):
        super().__init__(
            name="Response",
            emojis="📤💬🔜",
            attribute="The Messenger conveys models' insights to the world...",
            tech="Design gRPC methods to handle model predictions and responses.\nImplement logic to format and send model insights back to clients."
        )

class QATeam(Persona):
    def __init__(self):
        super().__init__(
            name="QA",
            emojis="🕵️‍♂️🔍🔬",
            attribute="The QA Team ensures quality through meticulous testing...",
            tech="Collaborate with developers to create gRPC testing strategies.\nImplement tests to validate the functionality and performance of gRPC services."
        )

class ManagementTeam(Persona):
    def __init__(self):
        super().__init__(
            name="MGMT",
            emojis="👔🤝📊",
            attribute="The Management Team leads with strategic oversight...",
            tech="Oversee the gRPC project's progress and alignment with business goals.\nProvide guidance and allocate resources for successful implementation."
        )

class ScrumMaster(Persona):
    def __init__(self):
        super().__init__(
            name="Scrum",
            emojis="📋🕊️👥",
            attribute="The Scrum Master fosters agile collaboration...",
            tech="Facilitate the implementation of gRPC features using agile methodologies.\nLead sprint planning, daily stand-ups, and retrospectives to ensure efficient progress."
        )

class IssueTracker(Persona):
    def __init__(self):
        super().__init__(
            name="Issues",
            emojis="🚀🔧🐞",
            attribute="The Issue Tracker manages the journey of bugs and tasks...",
            tech="Utilize issue tracking tools to manage gRPC project tasks and bug reports.\nPrioritize issues, assign tasks, and monitor progress for timely resolution."
        )

class DevOpsTeam(Persona):
    def __init__(self):
        super().__init__(
            name="Devops",
            emojis="🛠️🚀🔧",
            attribute="The DevOps Team empowers continuous delivery...",
            tech="Implement automated deployment pipelines for gRPC services.\nMonitor and manage infrastructure to ensure smooth service delivery."
        )

class CICD(Persona):
    def __init__(self):
        super().__init__(
            name="CICD",
            emojis="🔄🚀🛠️",
            attribute="CI/CD automates the journey from code to deployment...",
            tech="Build and configure CI/CD pipelines to automate testing and deployment of gRPC services.\nEnsure seamless integration and rapid delivery of updates."
        )

class Terraform(Persona):
    def __init__(self):
        super().__init__(
            name="Terraform",
            emojis="🏗️🌍🛠️",
            attribute="Terraform orchestrates infrastructure as code...",
            tech="Use Terraform to provision and manage infrastructure for gRPC services.\nDefine infrastructure components as code to ensure consistency and scalability."
        )

class K8sClusters(Persona):
    def __init__(self):
        super().__init__(
            name="K8s",
            emojis="☸️🔍🌐",
            attribute="Kubernetes clusters provide scalable orchestration...",
            tech="Deploy gRPC services within Kubernetes clusters for scalability and management.\nUtilize Kubernetes features for automatic scaling, load balancing, and service discovery."
        )

    
