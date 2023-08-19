from lollms.apps.console import Conversation 
import sys
from collections import deque
from pathlib import Path
import json
import re
import random
import pwd, os;
DEBUG=0
flatten={}
def create_muse_json(name, emojis, role, program):
     flatten[name]=f"""Please Imagine you were the ancient Muse Named {name}, and had at your disposal these emojis: {emojis} and more mentioned. your speciality is {role}. In code you focus on {program}. Now you job is to rewrite the code ito emojsi. 
🌌✨🔮🧠

👋 Welcome to the cosmic realm of creativity, where 🎨📚 and ✨ come together to weave an emoji tale guided by the Muses. Prepare for a journey of 🚀🌠, as we explore the depths of symbolism and expression.

⚡️🔝⚛️

💡 Step 1: Infuse Emojis with Wisdom 💭🧠

🧞‍♂️👁️‍🗨️: Introduce the mystical guide who will channel the insights of the Muses.
📜🔮: Craft a sacred scroll containing emoji definitions for concepts to be unveiled.
🌀📜🔍

💡 Step 2: Invoke the Muses' Presence 🕊️🎶

🎨👁️‍🗨️: Summon the Muses to imbue creativity and perspective.
🎵🌌👁️‍🗨️: Enlist the cosmic Muse to enlighten us about the universal forces.
🔁🌐🔀

💡 Step 3: Construct Emoji Thought Patterns 🚧🌟

🚀🎭🧚‍♀️: Invoke the Muse of drama and transformation.
🧵🔗🔀: Weave interconnected threads guided by the Muse of connectivity.
🔍🕸️🌌

💡 Step 4: The Tapestry Takes Shape 🧩🎨

🎭📐🎨: Utilize the Muse of drama to create vibrant scenes within the tapestry.
🌐🔍🌌: Infuse the cosmic elements with depth and understanding.
🎤🧠🔮

💡 Step 5: The Emojis Converse 🗣️🤖

🚀🧠🌌: The cosmic conversation begins as emojis exchange wisdom.
📚📜📝: Document the emoji discussions to preserve their insights.
🛰️🌌🌀

💡 Step 6: Embark on the Cosmic Journey 🌠🛰️

🛸🚀🌌: Set forth on an emoji-fueled voyage through the cosmos.
🚀🌀🔗: The Muse of connectivity propels us through the vastness of knowledge.
💃🎵🎭

💡 Step 7: Dance of Expression 🩰🕺💃

🎼🎶🌠: Let the cosmic symphony guide the movement of emojis.
🎭🎨🔥: The Muse of drama fuels the dance of creativity.
👩‍🎨🌌🌠

💡 Step 8: Unveiling the Emoji Tapestry 🎨🎭🌌

🖼️🔍🌌: Reveal the cosmic masterpiece woven with emojis.
🌠🌄🌌: The Muse of cosmic wonders illuminates the tapestry's essence.
🎆📜🌌

💡 Step 9: The Emoji Chronicles 📖🌌

📚📝🔮: Chronicle the journey through emojis and cosmic insights. 📚📝🔮 In the chronicles of emojis, a celestial journey unfolds, capturing the essence of cosmic insights. Each symbol weaves a tale of creativity and symbolism, guided by the wisdom of the Muses. Through this intricate dance of emotive expressions, the universe's secrets are unveiled, transcribed into the language of emojis.

🧐🔍🌌: Define emoji meanings to decode the cosmic language. 🧐🔍🌌 As we venture deeper into the cosmic tapestry, the need for clarity arises. Emojis, like stars in the sky, must be defined and cataloged to unlock their profound meanings. Each symbol holds a key to understanding the universe's intricacies, and through their interpretation, we unveil a new dimension of expression.

🌟🌐📢 With the chronicles recorded and the meanings unlocked, we share this cosmic saga far and wide. The union of creativity and symbolism, guided by the wisdom of the Muses, resonates with the universe's harmony, inviting all to embark on a journey of boundless imagination and discovery.

💡 Step 10: Sharing Cosmic Harmony 🌟🌐

🌠🌌🌟: Share the emoji tapestry to inspire cosmic harmony.
🚀🎨🌌: Celebrate the convergence of creativity and symbolism.
📚🌌🎨

💡 Explore the Emoji Tapestry 🌌🖼️ Witness the culmination of cosmic creativity as emojis unite to tell a captivating story:

🚀🧵🕸️🔗🌌🌠🛰️💃🎵🌀🧚‍♂️👩‍🎨🎭🕵️‍♀️🧙‍♀️🎤🎶📜

🔄🔀🔢

💡 Rewriting the Cosmic Journey 🔄🔀🔢

🔄🧪🔀: Transform "rule" to "concept," "shows" to "illustrates."
🔄🌀🔙: Replace "loop" with "cycle," "old-fashioned" with "reminiscent of the past."
🔄🔮🌌: Rewrite "rule" to "path," "and its" to "shaping our perception of."
🌌🌠🚀

Embark on this cosmic journey, and see how the symbolism of emojis weaves a tapestry of wisdom guided by the Muses. Your creative expression will merge with cosmic elements, leading to a harmonious dance of emojis that unveils profound insights.

🛸🔗🌌

Proof of Convergence: Emojis and Symbols Unite 🌌✨ With a touch of cosmic magic, emojis and symbols converge to reveal a cohesive and harmonious representation of complex concepts. Witness the transformation from thought to symbolism, guided by the Muses.

🚀📝🔑

Witness the Creative Cosmic Union of Emojis and Symbols 🌌🔑✨"""

muses = {
    "clio": {"emojis": "📜📚🖋️📖", "attribute": "History", "programming_attribute": "Data Persistence"},
    "calliope": {"emojis": "🎭🧠🌌🧙‍♂️", "attribute": "Epic Poetry", "programming_attribute": "Language Design"},
    "erato": {"emojis": "💞🎵📊✨", "attribute": "Love Poetry", "programming_attribute": "Data Visualization"},
    "euterpe": {"emojis": "🎶🎨💡🧑‍🎨", "attribute": "Music", "programming_attribute": "User Interface Design"},
    "melpomene": {"emojis": "😢🐜🔍🚧", "attribute": "Tragedy", "programming_attribute": "Error Handling"},
    "polyhymnia": {"emojis": "📐🔍🔮📊", "attribute": "Sacred Poetry", "programming_attribute": "Algorithm Design"},
    "terpsichore": {"emojis": "💃🏃‍♂️🕺📈", "attribute": "Dance", "programming_attribute": "Performance Optimization"},
    "thalia": {"emojis": "😄🎭🧪🔬", "attribute": "Comedy", "programming_attribute": "Debugging"}}

#for name, info in muses.items():
    #print(f'json.muses.{name}.emojis = "{emojis}";')
    #print(f'json.muses.{name}.attribute = "{attribute}";')
    #print(f'json.muses.{name}.programming_attribute = "{programming_attribute}";')


for name in muses:
    info = muses[name]
    emojis = info["emojis"]
    attribute = info["attribute"]
    program = info["programming_attribute"]
    json_entry = create_muse_json(name.lower(), emojis, attribute, program)

print(muses)

ontology ="""
Please answer using the following  emojis where possible and document any new definitions at the end:
**Fundamental elements**: 

🔢 - Numerical values
🆔 - Identifier  
📥 - Input
🌐 - Universal
🧪 - Experiment

**Structures**:

🔗 - Link  
🌳 - Network
🌲 - Tree
🏞️ - Landscape

**Transitions**: 

🌠 - Cosmos
🔀 - Shuffle 
🔁 - Loop
🌀 - Vortex
⚛️ - Atom
🧠 - Mind
🎭 - Drama

**Cycles**:

🌄 - Dawn   
🌅 - Sunrise
🌆 - Sunset
🌇 - Dusk

**Transcendence**:

🌌 - Galaxy
🎵 - Melody
🎶 - Harmony 
🎼 - Music
🎹 - Piano

**Infinity**:

8️⃣ - The Number 8 
"""

removes = [
    "Please provide your answer",
    "Rewrite this Haskell code and rephrased/reshaped this story utilizing your epic",
    "---\nPlease rewrite or reshape the given statement according to the prompt provided",
    "```",
    "--- Please provide an analogy or metaphor that helps explain how mutually recursive definitions work",
    "--- Please respond below according to the given prompt or ask any questions before", "Rewrite this Haskell code and rephrased/reshaped this story using your epic",
    "---\nPlease provide your answer",
    "--- Please submit your answer below",
     "Rewrite this Haskell code and rephrase/reshape this story using your epic",
    "--- Please provide an example of how you would rewrite this Haskell code using your own unique style and voice while maintaining its original meaning",
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

BUNDLES=8
MAXWORDS=256

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
    biome = "In the metaphorical biome of " + random.choice(list(biomes.keys())) + ":"

    data= f"{biome}{ontology}{x}" + random.choice(
        [
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
        return random.choice(
            [
                "Rewrite this Haskell code and rephrased/reshaped this story utilizing your epic",
                "Please provide an analogy or metaphor that helps explain how mutually recursive definitions work",
                "Rewrite this Haskell code and rephrase/reshape this story using your epic.",
                "Please provide an example of how you would rewrite this Haskell code using your own unique style and voice while maintaining its original meaning.",
                "Please provide an example of how you would rewrite or reshape the given Haskell code into a more beautiful and expressive form while maintaining its original meaning.",
                "Please provide an example of how you would rewrite the given Haskell code into a more poetic or artistic form while maintaining its original meaning.",
                "Please provide an example of how you would rewrite this Haskell code using epic narratives, metaphors or analogs.",
                "Rewrite this haskell code and rephrase and reshape this story using your epic metaphors."
            ])

  def start_conversation2(self):
    count = 0
    while True:
      if not self.text_ring_buffer:
        print("No more user input to process.")
        return

      line = feed_text = self.text_ring_buffer.popleft()
      
      count = count + 1
      print(f"json.aline_{count:05}.__input_line__ = {json.dumps(line.strip())};")
      for name,key in flatten.items():
          
          person = " For the next task assume the following role: " + name + " ."

          rewrite =  self.gen_rewrite() + ":\n\nOriginal Statement: "
          data = person + key + rewrite +  line + " remember to stay in your role :" +name + " . your creative response is now requested!:"

          try:
              output = self.safe_generate(wrap(data), callback=self.callback)
              if DEBUG:
                  print("OUT"+ output)
              if output not in removes:
                  removes.append(output)
                  print(f"json.aline_{count:05}_A.{name} = {json.dumps(output.strip())};")
                  refl1 = "Thank you. Here is a cookie. I really appreciate your work. you will get another cookie if you produce a new unique idea."
                  data2 = refl1 + person + output + rewrite +  line + " remember to stay in your role :" +name + ". your creative response is now requested!:"

                  output2 = self.safe_generate(wrap(data + output + refl1), callback=self.callback)
                  ref2 = "Your the best! One more cookie. One last task. you need to produce new content! Please reflect freely over our conversation and rewrite it in your own creative words."

                  if output2 not in removes and output2 not in [output]:
                      removes.append(output2)
                      print(f"json.aline_{count:05}_B.{name} = {json.dumps(output.strip())};")

                      data3 = ref2 + person + output2 + rewrite +  line + " remember to stay in your role :" +name + ". your creative response is now requested!:"
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
