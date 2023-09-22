from lollms.apps.console import Conversation
import sys
from collections import deque
from pathlib import Path
import json
import re
import random
import pwd, os
import personas

DEBUG = 0
BUNDLES = 4

flatten = personas.descriptions
    
prolog = """Implementing Protobufs for Clarifai API

**Project Overview:**
The primary objective of this project is to implement Protocol Buffers (Protobufs) for the Clarifai API. Protocol Buffers provide a language-agnostic, efficient, and extensible way to serialize structured data. By adopting Protobufs, we aim to enhance data interchange and communication within the Clarifai ecosystem.

**Project Objectives:**
- Define clear requirements for implementing Protobufs.
- Design and structure Protobuf message schemas to represent Clarifai API data.
- Generate code bindings from Protobuf definitions for various programming languages.
- Implement Clarifai API endpoints using Protobufs.
- Perform comprehensive testing and validation of the Protobuf implementation.
- Create documentation to guide developers on utilizing Protobufs and the Clarifai API effectively.
   
4. **Implement API Endpoints:**
   - Incorporate Protobufs into the existing Clarifai API endpoints, ensuring smooth data serialization and deserialization.

"""


MAXWORDS = len(prolog) + (256*3)

ontology = """
**Background Ontology for Clarifai API Protobufs**

**Data Types:**

1. **String (`str`):** A sequence of characters.
   
2. **Boolean (`bool`):** Represents a binary value, typically `True` or `False`.

3. **Integer (`int`):** A whole number without a fractional part.

4. **NoneType (`NoneType`):** Represents the absence of a value.

5. **Descriptor (`google._upb._message.Descriptor`):** A descriptor for a Protocol Buffers message type.

6. **ByNameMap (`google._upb._message._ByNameMap`):** A mapping structure for Protocol Buffers message types.

7. **GenericSequence (`google._upb._message._GenericSequence`):** A generic sequence data structure.

8. **FileDescriptor (`google._upb._message.FileDescriptor`):** Descriptor for a Protocol Buffers file.

9. **Built-in Function or Method (`builtin_function_or_method`):** Predefined functions or methods in Python.

10. **List (`list`):** An ordered collection of elements.

11. **Dictionary (`dict`):** A collection of key-value pairs.

**Ontological Relationships:**

- **String, Boolean, Integer, NoneType:** These fundamental data types form the basis of data representation in various contexts.

- **Descriptor, ByNameMap, GenericSequence, FileDescriptor:** These are specialized data types related to Protocol Buffers for defining and working with structured data.

- **Built-in Function or Method:** Represents predefined functionalities available in the Python language.

- **List, Dictionary:** These data structures provide a means of organizing and storing data efficiently.

**Semantic Associations:**

- Protocol Buffers (`Descriptor`, `ByNameMap`, `FileDescriptor`) are used to define structured data formats and facilitate efficient data interchange.

- Lists (`list`) and Dictionaries (`dict`) are commonly used for organizing and manipulating data collections.

- Built-in Functions and Methods provide core functionalities for various operations.
"""

seen = {}
for x in  [
    "```",
    "--- Please provide your answer below",
    "--- Please answer",
    ")))))\n\n---",
    "</instruction>)",
    "</instruction>",
    "---",
    "",
]:
    seen[x]=1


# print pwd.getpwuid(os.getuid()).pw_gecos
username = pwd.getpwuid(os.getuid()).pw_name

def split_fibers(fibers, max_words=MAXWORDS):
    # Split each fiber into chunks of up to max_words words
    sfibers = []
    for fiber in fibers:
        words = fiber.split()
        for i in range(0, len(words), max_words):
            chunk = " ".join(words[i : i + max_words])
            sfibers.append(chunk)
    return sfibers

def refactor_into_fiber_bundles(lines, bundle_size):
    bundles = []
    temp = []
    for line in lines:
        # Split the line into fibers
        # fibers = line.split('.')
        fibers = re.split(r"[\.\n]", line)

        # Filter out empty lines or lines with only whitespace
        fibers = [fiber.strip() for fiber in fibers if re.search(r"\S", fiber)]

        # Add filtered fibers to the current bundle
        temp.extend(split_fibers(fibers))
    # now lete
    current_bundle = []
    # print(temp)
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

    biome = f""
    data = f"{biome}{ontology}{x}" + random.choice(
        [
            "",
        ]
    )
    if DEBUG:
        print(data)
    return data


class MyConversation(Conversation):
    def __init__(self, cfg=None):
        super().__init__(cfg, show_welcome_message=False)
        self.text_ring_buffer = deque()  # Ring buffer to hold user responses

    def read_input_file(self, file_path):
        with open(file_path, "r") as file:
            lines = file.readlines()

            lines = refactor_into_fiber_bundles(lines, BUNDLES)

            with open("debug.txt", "w") as fo:
                for line in lines:
                    fo.write("|\n".join(line))
        for line in lines:
            self.text_ring_buffer.append(
                self.personality.user_message_prefix + "\n".join(line)
            )
        print("start COUNT",len(self.text_ring_buffer))

    def gen_rewrite(self):
        topic = "Snippet"
        target= "Protobuf Server"
        return random.choice(
            [
                f"Transform this {topic} into a Python code representation of a {target}.",
                f"Generate a Python code snippet for a {target} that implements this {topic}.",
                f"Craft a Python implementation of a {target} that embodies the essence of this {topic}.",
            ]
        )

    def start_conversation2(self):
        count = 0
        print("COUNT",len(self.text_ring_buffer))

        while True:
            if len(self.text_ring_buffer) <= 0:
                print("No more user input to process.")
                return

            line = feed_text = self.text_ring_buffer.popleft()

            count = count + 1
            print(f"json.aline_{count:05}.__input_line__ = {json.dumps(line.strip())};")
            for name, key in flatten.items():

                person = prolog 

                rewrite = self.gen_rewrite() + ":\n\nOriginal Term/Statement: "
                data = (
                    person
                    + key
                    + rewrite
                    + line
                    + ". Please in your own words:"
                )

                try:
                    newt = []

                    maxtry=6
                    for atry in range(maxtry):
                        output = self.safe_generate(wrap(data + f"try {atry}/{maxtry}"), callback=self.callback)
                        if DEBUG:
                            print("OUT" + output)
                        if output not in seen:
                            seen[output]=1
                            print(
                                f"json.aline_{count:05}_A.{name} = {json.dumps(output.strip())};"
                            )
                            newt.append(output)

                        newt2 = []
                        for atry in newt:
                            refl1 = "Thank you. Here is a cookie. "

                            output2 = self.safe_generate(
                                wrap(data + atry + refl1), callback=self.callback
                            )
                            if output2 not in seen and output2 not in [output]:
                                seen[output2]=1
                                print(
                                    f"json.aline_{count:05}_B.{name} = {json.dumps(output.strip())};"

                                )
                                newt2.append(output2)
                                                    
                        for output2 in newt2:
                            data3 = output2

                            for prompt in (
                                    "Please rewrite as an instruction template",
                                    "Please rewrite creativly",
                                    "Listt the 96 concepts found in the following",
                            ):
                                output3 = self.safe_generate(
                                    prompt + " " + wrap(data3), callback=self.callback
                                )
                                if output3 not in seen and output3 not in [
                                        output,
                                        output2,
                                ]:
                                    seen[output3]=1
                                    print(
                                        f"json.aline_{count:05}_C.{name} = {json.dumps(output.strip())};"
                                    )
                        else:
                            if DEBUG:
                                print("-", output2)
                    else:
                        if DEBUG:
                            print("-", output)

                except Exception as e:
                    stre = json.dumps(str(e)).replace(username,"USER")
                    print(f"json.aline_{count:05}_ERRROR.{name} = {stre}")
                    raise e

    def callback(self, text, type=None, metadata: dict = {}):
        if DEBUG:
            print("DBG:" + text, end="")
            sys.stdout.flush()
        return True


if __name__ == "__main__":
    cv = MyConversation(Path("config.yaml"))
    input_file_path = "user_input.txt"
    try:
        cv.read_input_file(input_file_path)

        cv.start_conversation2()
    except Exception as e:
        print(e)
        raise e
