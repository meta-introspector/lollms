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
BUNDLES = 3

flatten = personas.descriptions
    
prolog = """"🚀 Join our interdisciplinary project to revolutionize AI workflows, fusing math, art, and AI 🎨🤖. From project start to AI review, we boost collaboration with personas and emojis. Embrace CEVaDi: Collect, Evaluate, Validate, Document Information. Enhance decision-making and data integrity. #Innovation #AI #ProjectManagement"""


MAXWORDS = len(prolog) + (256*3)

ontology = ""

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
        topic = "Detailed plan"
        target= "Detailed Workflow"
        return random.choice(
            [
                f"Rewrite this {topic} as a {target} implementation.",
                f"Please provide an example of how you would implement a {target} for this {topic} using Python.",
                f"Reshape the given {topic} into a {target} code snippet in Python.",
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
                    + ". Please definine in your own words:"
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
                            refl1 = "Thank you. Here is a cookie. I really appreciate your work. you will get another cookie if you produce a new unique idea."

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

                            ref2 = "Your the best! One more cookie. Now reflect over our conversation"
                            data3 = output + output2 + ". Now rewrite with unit tests."
                            output3 = self.safe_generate(
                                wrap(data3), callback=self.callback
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
