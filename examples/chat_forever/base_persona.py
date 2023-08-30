import re
class Persona:
    def __init__(self, name, emojis, attribute, tech):
        self.emojis = emojis
        self.attribute = attribute
        self.tech = tech
        self.name = name
        
    def describe(self):
        return f"""Oh {self.name}, Your {self.attribute}, and {self.tech}"""

def parse_persona(text):
    personas = []
    
    # Define a pattern to match the persona sections
    pattern = r"\*\*([^:]+):\*\*\n\s+- Emojis: ([^\n]+)\n- Attribute: ([^\n]+)\n\s+- Tech: ([^\n]+)"

    patterns = [
        r"[0-9]+\s*\.\s*\*\*\s*(?P<Role>[^:]+)\s*:\*\*",
        r"\s+\-\s+(?P<Aspect>[a-zA-Z0-9]+)\s*:\s*(?P<Content>[^\n]+)"
    ]

    aspects = {}
    name = None #no name name
    for line in text.split("\n"):    
        for p in patterns:       
            match = re.findall(p, line)
            if match:
                if len(match[0])==2 :
                    aspects[match[0][0].lower()]=match[0][1]
                else:
                    if name: #old name
                        if (aspects):
                            #print(name, aspects)
                            aspects["name"] = name
                            personas.append(Persona( **aspects))
                    # now set the name for the next loop
                    name= match[0]
    if name: #old name
        if (aspects):
            #print(name, aspects)
            aspects["name"] = name
            personas.append(Persona( **aspects))
                
    return personas

#import personas2
def import_personas(filename="personas2.txt"):
    with open(filename) as fi:
        txt = ""
        for line in fi:
            txt = txt + line
        return parse_persona(txt)
