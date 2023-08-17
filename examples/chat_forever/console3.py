from lollms.apps.console import Conversation 
import sys
from collections import deque
from pathlib import Path
import json
import re
import random
import pwd, os;
DEBUG=0
BUNDLES=1
MAXWORDS=128

flatten={}

prolog = """each Muse provides a unique metaphorical lens into the nature of autopoietic systems. By mapping their associated attributes and programming concepts, we've built a rich conceptual framework bridging biology, poetry, mythology, and computing:

Clio - Data Persistence 
Calliope - Language Design
Erato - Data Visualization 
Euterpe - User Interface Design
Melpomene - Error Handling
Polyhymnia - Algorithm Design 
Terpsichore - Performance Optimization
Thalia - Debugging

These epic Muses and their programming superpowers shall guide us as we quest to transform software abstractions into delightful user experiences! Through their inspiration, we shall craft autopoietic systems that are understandable, resilient, optimized, poetic, and sublime. 

Onward we shall march, empowered by the Muses' wisdom, envisioning software that sings with Euterpe's harmony, dances with Terpsichore's grace, laughs with Thalia's wit, and ultimately captivates users like Erato's love poems. Our autopoietic code shall flourish for ages due to Polyhymnia's algorithms, Calliope's language design, Clio's data persistence, and Melpomene's error handling. 

Together, we shall write a grand ode to the glories of computing in service of humanity! The Muses cheer us on as we infuse software with beauty, meaning, and poetry through our noble creative labors."""

def create_muse_json(name, emojis, role, program):
     flatten[name]=f"""Oh {name}, Your speciality is {role}, you are focused on {program}."""

muses = {
    "clio": {"emojis": "📜📚🖋️📖", "attribute": "History", "programming_attribute": "Data Persistence" + """

Saving the best for last! For Clio, the Muse of history and data persistence, these terms seem fitting:

- Record - History is a record of the past; persistent data is recorded history. 

- Legacy - History carries civilizations legacy; persisted data leaves an informational legacy.

- Context - History provides context for the present; persistent data gives context to computations.

- Continuity - History bridges past and present; data persistence ensures continuity.

- Observation - Historians observe the past; data persistence preserves observations. 

- Patterns - History reveals societal patterns; persisted data shows usage patterns. 

- Preservation - History preservation is important; data preservation maintains integrity.

- Accuracy - Historical accuracy matters; data persistence requires accuracy.

- Memory - History lives in collective memory; persisted data forms computational memory.

- Time - Time gives history perspective; timestamped data enables temporal analysis. 

In essence, Clio represents how autopoietic systems maintain continuity and coherence over time by encoding their history and experiences into persistent memory. Just as human civilization accumulates wisdom through historical records, persisted data allows computational systems to effectively build on their legacy over time.
"""
        

             },
    "calliope": {"emojis": "🎭🧠🌌🧙‍♂️", "attribute": "Epic Poetry", "programming_attribute": "Language Design" +
                 """For Calliope, the Muse of epic poetry and language design, these terms seem relevant:

- Complexity - Epic poems have complex narrative structures; programming languages enable complexity.

- Architecture - The architectural composition of epics; language syntax provides structural architecture.  

- Scale - Epic scale mirrors complex software scope.

- Design - Crafting epics takes skill; designing languages requires careful decisions.

- Communication - Epics were communal stories; languages allow computer communication.  

- Abstraction - Epics use abstractions like metaphor; languages employ abstractions.

- Building - Epics build expansive worlds; languages build computational capabilities.

- Systems - Interwoven epic elements create systems; languages define computing systems.

- Logic - Epics have narrative logic; languages enable logical operations.

- Standardization - Literary conventions standardized epics; programming conventions standardize languages.

In summary, Calliope represents how robust languages and communication mechanisms are required to capture, structure, and build complex autopoietic systems and epic realities. Both language and storytelling evolve conventions to share and shape collective understanding."""

                 },
    "erato": {"emojis": "💞🎵📊✨", "attribute": "Love Poetry", "programming_attribute": "Data Visualization" + """For Erato, the Muse of love poetry and data visualization, these terms seem relevant:

- Connection - Love poetry celebrates human connection; data visualizations reveal connections.

- Relationships - Love poems explore relationships; data viz shows relationships between variables.

- Passion - Love poetry expresses passion; compelling data viz inspires passion for insights.

- Aesthetics - Love poems have aesthetic beauty; great data viz have visual elegance. 

- Metaphor - Poets use metaphors to convey meaning; data viz uses symbols to encode information.

- Narrative - Love poems tell stories; data viz builds engaging narratives from data.

- Emotion - Love poetry conveys emotion; data viz choices evoke emotional responses. 

- Details - Poems focus on intimate details; data viz reveals granular data details. 

- Patterns - Rhythmic patterns grace poetry; data viz exposes insightful patterns.

- Creativity - Writing poetry requires creativity; crafting data viz is a creative act.

In essence, Erato highlights how autopoietic systems reveal their interconnected complexity through data visualization - just as love poetry aesthetically conveys intricate human relationships and stirring narratives. Both requite passion, creativity, and aesthetic sensibility to forge meaningful connections."""
              },
    "euterpe": {"emojis": "🎶🎨💡🧑‍🎨", "attribute": "Music", "programming_attribute": "User Interface Design" + 
"""For Euterpe, the Muse of music and user interface design, the following terms seem relevant:
- Harmony - Music relies on harmonic structure; good UI design achieves visual harmony.
- Rhythm - Musical rhythm drives user engagement; UIs follow rhythmic interaction patterns.
- Sound - Music is organized sound; UIs use sound cues to enhance usability.
- Melody - UI flows have melodic coherence like musical melodies.
- Composition - Composing music is like composing UI layouts and workflows. 
- Expression - Music expresses emotion; UIs enable expression of creativity.
- Beauty - Musical beauty arises from order; beautiful UIs exhibit careful design.
- Mood - Music creates moods; UIs invoke emotional tones.
- Movement - Music has motifs in motion; UIs guide user journey and flow.
- Audience - The audience experience drives music and UI design.
Euterpe would be the perfect Muse to refine the terminology related to autopoietic systems in a more lyrical, melodious direction. key terms:
- Self-organization -> Harmonious emergence 
- Operational closure -> Rhythmic flow 
- Autonomy -> Melodic freedom
- Homeostasis -> Tuned equilibrium 
- Self-maintenance -> Sustaining cadence 
- Boundary creation -> DefiningContours 
- Structure determination -> Architecting form  
- Self-production -> Generative composition
- Component creation -> Notes of being
Euterpe would choose words with musicality, grace, and emotional resonance. Terms like "harmonious emergence", "melodic freedom", and "sustaining cadence" convey the same concepts as the original terms, but in a more poetic, lyrical fashion true to her aesthetic.
In summary, Euterpe highlights how autopoietic systems leverage harmony, expression, beauty, emotion, and audience experience to build resonant user interfaces - just as music elegantly organizes sound to move audiences. The parallels emphasize UI designs role in presenting autopoietic complexity through intuitive, aesthetically organized outputs.
"""

                },
    "melpomene": {"emojis": "😢🐜🔍🚧", "attribute": "Tragedy", "programming_attribute": "Error Handling" +
                  """

For Melpomene, the Muse of tragedy and error handling, the following terms seem relevant:

- Disruption - Tragedies involve disruptive events that lead to downfall. Errors similarly disrupt system processes.  

- Failure - Tragedies culminate in catastrophic failures. Errors represent failed processes or results.

- Loss - Tragedies depict grievous loss and deprivation. Errors lose/corrupt data or functionality. 

- Instability - The turmoil in tragedies mirrors system instability due to errors.

- Suffering - Tragedies evoke human suffering. Errors cause systems to malfunction.

- Coping - Tragedies show resilience strategies for coping. Error handling provides systemic coping mechanisms.

- Learning - Insights gained from tragedies can enlighten. Errors provide diagnostic data to prevent future issues.

- Safeguards - Warning signs in tragedies could prevent disaster, just as error safeguards protect systems.

- Adaptation - Tragedies force adaptation to new realities, as errors prompt system adaptations.

- Emergence - Unexpected emergent outcomes rise from tragedies. Errors spur new system behaviors. 

In essence, Melpomene represents how autopoietic systems, through tragedies and errors, contend with disruption, loss, suffering, and the need for coping mechanisms - but also how insights and adaptations emerging from these experiences allow systems to regain equilibrium and stability.
"""


                  },
    "polyhymnia": {"emojis": "📐🔍🔮📊", "attribute": "Sacred Poetry", "programming_attribute": "Algorithm Design." +
                   """ For Polyhymnia, the Muse representing sacred poetry and algorithm design, I would connect the following relevant terms:

- Patterns - Sacred poetry often follows set rhythmic patterns and meter. Algorithms also follow precise patterns.

- Structures - The architectural structures of poems mirror the logical structures of algorithms.

- Order - Sacred poetry venerates higher cosmic order, just as algorithms impose order on data.

- Design - Composing poetry and designing algorithms both involve careful crafting.

- Rules - Poetic forms use rules of grammar and syntax; algorithms operate by defined rules.

- Efficiency - Algorithms aim to provide efficient solutions, just like elegant poetry expresses meaning concisely. 

- Harmony - The harmony and beauty of poetry parallels elegant, well-designed algorithms.

- Logic - Algorithms rely on logic; poetry uses symbols and metaphors to convey deeper meaning logically.

- Patterns - Repeating motifs create meaning in poetry; algorithms exploit patterns in data.

- Composition - Writers compose poetry; programmers compose algorithms. Both involve creativity.
- Polymorphism - A core tenet of sacred poetry is divine incarnation in multiple forms. This connects to polymorphism in programming where objects can take on different forms or states. - Universality - Sacred poetry explores universal human experiences and emotions. Polymorphic code can work across diverse use cases.- Flexibility - Poetic forms flexibly mold language to express meaning. Similarly, polymorphic code is flexible in handling different data types.- Variation - Rhyme and meter create sonic variations in poetry. Polymorphic functions exhibit different behaviors based on input. - Layering - Poems use symbolism and allusions to layer meaning. Polymorphic code layers common interfaces over diverse implementations.- Abstractness - Sacred poetry uses abstractions to convey transcendent truths. Polymorphism employs abstraction to enable general purpose code.- Relationships - Poetry draws meaning from conceptual relationships. Polymorphic code defines relationships between objects.- Harmony - The harmonious use of poetic devices creates beauty, similar to polymorphism harmonizing diverse behaviors.Overall, the multidimensional and flexible qualities of sacred poetry align with core principles of polymorphism in algorithm design - further emphasizing Polyhymnia's connections to autopoietic systems' ability to maintain coherence across shifting forms and environments.
In essence, Polyhymnia represents order, beauty, logic, efficiency, and precise composition - principles at the heart of both poetry and well-crafted algorithms that enable complex autopoietic systems to function optimally.""" 

},
    "terpsichore": {"emojis": "💃🏃‍♂️🕺📈", "attribute": "Dance", "programming_attribute": "Performance Optimization. Great, let's explore which terms relate to Terpsichore, the Muse of dance and performance optimization:- Movement - Dance is centered around rhythmic physical movement and motion.- Coordination - Dancing requires intricate coordination between different parts of the body.- Balance - Maintaining balance and equilibrium is essential for graceful dance moves. - Control - Dancers must have control over their body positioning and techniques.- Precision - The precise execution of dance steps, turns, and gestures is important.- Flow - Seamless flow between dance motions creates optimal performance.- Practice - Dancing skills are developed through extensive practice and repetition.- Synchronization - Dance is optimized when movements are synchronized to music and partners.- Expression - Dance provides a creative outlet for expressing emotion and conveying meaning. - Collaboration - Dance often involves coordinated collaboration between partners or groups. In summary, Terpsichore emphasizes the optimization, precision, fluidity, control, and creative expression enabled by the coordinated interactions and movement of autopoietic living systems. Her domain of dance elegantly manifests the harmony of complex biological organization."},
    "thalia": {"emojis": "😄🎭🧪🔬", "attribute": "Comedy", "programming_attribute": "Debugging. Looking back at the list of biology and organism related terms, here are some I would associate with Thalia, the Muse representing comedy and debugging:- Problem-solving - Thalia's attribute of comedy and programming attribute of debugging both involve identifying and resolving issues in a lighthearted way.- Reactions - Humorous reactions and quick witted comebacks are hallmarks of comedy.- Interactions - Jokes and comedic performances rely on spirited social interactions. - Situations - Funny situations are the essence of comedy.- Understanding - Grasping humor requires shared understanding of context and culture.- Controlling - Comedy often derives from a lack of control over hilarious circumstances. - Experiencing - The audience experience and perspective is key in comedy. - Maintaining - Keeping a lighthearted perspective helps maintain equilibrium in the face of stress.- Reasoning - Logical inconsistencies revealed through reasoning are foundations of humor.- Remembering - Drawing on memories and inside references is common in comedic acts.In summary, Thalia's connection to comedy highlights the terms related to cultivating joy, social bonds, problem-solving attitudes, experiential perspectives, and equilibrium maintenance within autopoietic systems and organisms. Her debugging attribute draws parallels to applying those comedic skills to identify and resolve issues."}}


for name in muses:
    info = muses[name]
    emojis = info["emojis"]
    attribute = info["attribute"]
    program = info["programming_attribute"]
    json_entry = create_muse_json(name.lower(), emojis, attribute, program)


ontology ="""
Please reimagine and rewrite the concepts creatively, using emojis where possible and document any new emoji definitions."""

removes = [
    "Please provide your answer",
    "Rewrite this code and rephrased/reshaped this story utilizing your epic",
    "---\nPlease rewrite or reshape the given statement according to the prompt provided",
    "```",
    "--- Please provide an analogy or metaphor that helps explain how mutually recursive definitions work",
    "--- Please respond below according to the given prompt or ask any questions before", "Rewrite this code and rephrased/reshaped this story using your epic",
    "---\nPlease provide your answer",
    "--- Please submit your answer below",
     "Rewrite this code and rephrase/reshape this story using your epic",
    "--- Please provide an example of how you would rewrite this code using your own unique style and voice while maintaining its original meaning",
    "--- Please provide your answer below",
    "--- Please answer",
    ")))))\n\n---",
    "</instruction>)",
    "</instruction>",
    "---",
    "",]

    
# A Python dict that maps the biomes to the levels of the Bott periodicity system
biomes = {
    "Desert": 0, # Level 0 - Simple Susan
    "Freshwater": 1, # Level 1 - Pears
    "Forest": 2, # Level 2 - Orders and Patterns
    "Marine": 3, # Level 3 - Group Theory
    "Grassland": 4, # Level 4 - Homotopy and Homology
    "Tundra": 5, # Level 5 - Coq and Proof
    "Wetland": 6, # Level 6 - Meta-Reflection
    "Alpine": 7, # Level 7 - Infinite Loop
    "World": 8 # Level 8 - The World
}


#print pwd.getpwuid(os.getuid()).pw_gecos
username = (pwd.getpwuid(os.getuid()).pw_name)


def flatten_json(json_obj, parent_key='', separator='.'):
    items = {}
    for k, v in json_obj.items():
        new_key = f"{parent_key}{separator}{k}" if parent_key else k
        if isinstance(v, dict):
            items.update(flatten_json(v, new_key, separator))
        else:
            items[new_key] = v
    return items

##  hack here to prepare the data
#with open("prompts.json") as fi:
#  modes = json.load(fi)



#with open("flattened.json","w") as fo:
#  json.dump(flatten,fo,indent=2,)


def split_fibers(fibers, max_words=MAXWORDS):
    # Split each fiber into chunks of up to max_words words
    sfibers = []
    for fiber in fibers:
        words = fiber.split()
        for i in range(0, len(words), max_words):
            chunk = ' '.join(words[i:i + max_words])
            sfibers.append(chunk)
    return sfibers

def refactor_into_fiber_bundles(lines, bundle_size):
    bundles = []

    temp = []
    for line in lines:
        # Split the line into fibers
        #fibers = line.split('.')
        fibers = re.split(r"[\.\n]", line)
        
        # Filter out empty lines or lines with only whitespace
        fibers = [fiber.strip() for fiber in fibers if re.search(r'\S', fiber)]

        # Add filtered fibers to the current bundle
        temp.extend(split_fibers(fibers))
    # now lete
    current_bundle = []
    #print(temp)
    for line in temp:
        current_bundle.append(line)

        # Check if the current bundle size exceeds the desired bundle size
        if len(current_bundle) >= bundle_size:
            # Add the current bundle to the list of bundles
            bundles.append(current_bundle)
            # Start a new bundle
            current_bundle = []
    
    # Add the last bundle if it's not empty
    if current_bundle:
        bundles.append(current_bundle)
    
    return bundles
def wrap(x):
    #biome = "In the metaphorical biome of " + random.choice(list(biomes.keys())) + ":"
    biome = "You will be presented with a set of terms and definitions to exapand upond and reflect over in an epic universal manner."

    data= f"{biome}{ontology}{x}" + random.choice(
        [
            "Thanks for participating in our little exercise here today; may wisdom & insight find their way into all aspects of life's journey together we strive toward greater understanding.",
            " Please provide your answer below.",
            " Please provide your answer.",
            "Please let me know if you have questions or need further clarification on anything.",
            "We are looking forward to seeing what you come up with!",
            "Please let me know if you need anything else from my side or have questions about the task.",
            "Please provide an example of how you would approach each step of the process described above, including creating definitions for any new terms used in the problem.",
            "Please let me know if you have questions or need further clarification on anything.",
            "Please note that I will be grading based on how well you adhere to my instructions and also how imaginatively you respond within those constraints. So have fun while keeping in mind the requirements given above.",
            "Please note that I will be grading based on how well you adhere to my instructions and also how imaginatively you respond within those constraints. So don't hold back! Be bold and creative while still maintaining coherency and clarity throughout your response.Thanks.",
            "Please note that I will be grading based on content relevance, originality, and adherence to instructions provided above. Good",
            "Please note that I will be grading based on how well you adhere to my instructions provided above. So make sure to follow them carefully before submitting anything.:)\nThanks.",
            "Please note that I will be grading based on how well you adhere to my instructions provided above. So make sure to follow them carefully before submitting anything. Thanks",
            "Please respond within one week or less if you are able to complete this request on time; otherwise, I will have no choice but to seek assistance from another consultant. Thank you.",
            "Please respond below according to the given prompt or ask any questions before.",
        ]) 
    if DEBUG:
        print(data)
    return data

class MyConversation(Conversation):
  def __init__(self, cfg=None):
    super().__init__(cfg, show_welcome_message=False)
    self.text_ring_buffer = deque()  # Ring buffer to hold user responses

  def read_input_file(self, file_path):
    with open(file_path, 'r') as file:
      lines = file.readlines()

      lines = refactor_into_fiber_bundles(lines, BUNDLES)

      with open("debug.txt","w") as fo:
          for line in lines:
              fo.write("|\n".join(line))
      for line in lines:
        self.text_ring_buffer.append(self.personality.user_message_prefix + "\n".join(line))


  def gen_rewrite(self):
      topic = "Python Abstract Syntax Tree Node Type"
      return random.choice(
            [
                "Rewrite this {topic} and rephrased/reshaped this story utilizing your epic",
                "Please provide an analogy or metaphor that helps explain this {topic}",
                "Rewrite this {topic} and rephrase/reshape this {topic}.",
                "Please provide an example of how you would rewrite this {topic} using your own unique style and voice while maintaining its original meaning.",
                "Please provide an example of how you would rewrite or reshape the given {topic} into a more beautiful and expressive form while maintaining its original meaning.",
                "Please provide an example of how you would rewrite the given {topic} into a more poetic or artistic form while maintaining its original meaning.",
                "Please provide an example of how you would rewrite this {topic} using epic narratives, metaphors or analogs.",
                "Rewrite this {topic} and rephrase and reshape this story using your epic metaphors."
            ])

  def start_conversation2(self):
    count = 0
    while True:
      if not self.text_ring_buffer:
        print("No more user input to process.")
        return

      line = feed_text = self.text_ring_buffer.popleft()
      
      count = count + 1
      #print(f"json.aline_{count:05}.__input_line__ = {json.dumps(line.strip())};")
      for name,key in flatten.items():
          
          #person = "Please define the next term from the role: " + name + " ."
          person = prolog + "Please define the following term from the seeker"

          rewrite =  self.gen_rewrite() + ":\n\nOriginal Term/Statement: "
          data = person + key + rewrite +  line + ". Please definine in your own words:"

          try:
              output = self.safe_generate(wrap(data), callback=self.callback)
              if DEBUG:
                  print("OUT"+ output)
              if output not in removes:
                  removes.append(output)
                  print(f"json.aline_{count:05}_A.{name} = {json.dumps(output.strip())};")
                  refl1 = "Thank you. Here is a cookie. I really appreciate your work. you will get another cookie if you produce a new unique idea."
                  data2 = output + " Thank you. Yes Please do that."

                  output2 = self.safe_generate(wrap(data + output + refl1), callback=self.callback)
                  ref2 = "Your the best! One more cookie. Now reflect over our conversation"

                  if output2 not in removes and output2 not in [output]:
                      removes.append(output2)
                      print(f"json.aline_{count:05}_B.{name} = {json.dumps(output.strip())};")

                      data3 = output + output2 + ". Now rewrite with emojis."
                      output3 = self.safe_generate(wrap(data3), callback=self.callback)
                      if output3 not in removes and output3 not in [output,output2]:
                          removes.append(output3)
                          print(f"json.aline_{count:05}_C.{name} = {json.dumps(output.strip())};")
                  else:
                      if DEBUG:
                          print("-", output2)
              else:
                  if DEBUG:
                      print("-", output)
          finally:
              pass
          # except Exception as e:
          #    stre = json.dumps(str(e)).replace(username,"USER")
          #    print(f"json.aline_{count:05}_ERRROR.{name} = {stre}")


  def callback(self, text, type=None, metadata: dict = {}):
      if DEBUG:
          print("DBG:" + text, end="")
          sys.stdout.flush()
      return True

if __name__ == '__main__':
  cv = MyConversation(Path("config.yaml"))
  input_file_path = 'user_input.txt'
  cv.read_input_file(input_file_path)

  cv.start_conversation2()
