from lollms.apps.console import Conversation
import sys
from  ai_ticket.events.inference import on_event
import time
maxtry=10
import dirtyjson
import streamlit as st
from collections import deque
from pathlib import Path
import json
import re
import random
import pwd, os
import personas
from flask import Flask, make_response, request, abort
from flask.json import jsonify

DEBUG = 0
BUNDLES = 4

flatten = personas.descriptions
    
prolog = """Implementing StreamLit Task Execution via Protobufs for Clarifai API

**Project Overview:**
The primary objective of this project is to implement Streamlit based GUI for Protocol Buffers (Protobufs) for the Clarifai API. Protocol Buffers provide a language-agnostic, efficient, and extensible way to serialize structured data. By adopting Protobufs, we aim to enhance data interchange and communication within the Clarifai ecosystem.

**Project Objectives:**
- For the Protobuf messages, have the YAML/JSON/TOML schemas generate the `.proto` files automatically. Users only interact with the high-level schemas.
- Build an intermediate layer to map the YAML schemas to Protobuf messages seamlessly. The UI only sees the YAML.
- Create Streamlit forms using `st.form` and `st.form_submit_button`. The submit handler translates user input to Protobuf messages. 
- Design emojigram interfaces for each task using intuitive emoji combinations. Map emojigrams to API requests internally
- Use a library like `emoji` to convert between emojigrams and text for translation to Protobufs.
- Manage decoding of Protobuf responses and presentation of results to users in the UI layer.
- Implement error and progress notification using `st.info`, `st.warning`, `st.error` and loading spinners.
- For workflows, maintain workflow state and execution logic in the intermediate layer, keeping the UI simple.
- Design and structure Streamlit forms and yaml Protobuf message schemas to represent Clarifai API data.
- Generate code bindings from Protobuf definitions for various programming languages.

4. **Implement API Endpoints:**
   - Create streamlit guis for all ideas

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

# set up the Flask application
app = Flask(__name__)

#if __name__ == "__main__":

cv = MyConversation(Path("config.yaml"))
    # input_file_path = "user_input.txt"
    # try:
    #     cv.read_input_file(input_file_path)

    #     cv.start_conversation2()
    # except Exception as e:
    #     print(e)
    # raise e
models = {}


@app.route("/v1/models", methods=['GET'])
def models():
    data = [
        {
            "id": "gpt-3.5-turbo",
            "object": "model",
            "owned_by": "organization-owner",
            "permission": []
        }
    ]
    return {'data': data, 'object': 'list'}

# @app.route("/v1/engines/<model_name>/completions", methods=["POST"])
# def completions(model_name):
#     # get the request data
#     #print("completions", request.text)
#     data = request.get_json(force=True)
#     # is it an alias?
#     if (model_name in models):
#         model_name = models[model_name]
   
#     # get the prompt and other parameters from the request data
#     prompt = data["prompt"]
#     max_tokens = data.get("max_tokens", 16)
#     temperature = data.get("temperature", 1.0)
#     top_p = data.get("top_p", 0.75)
#     top_k = data.get("top_k", 40)
#     num_beams = data.get("num_beams", 1)
#     max_new_tokens = data.get("max_new_tokens", 256)

#     #kwargs = decode_kwargs(data)
    
#     if (model_name in llamaModels):
#         #generated_text = evaluate_llama(prompt,**kwargs)
#         generated_text = evaluate_llama(prompt,
#                                         #input = prompt,
#                                         temperature=temperature,
#                                         top_p=top_p,
#                                         top_k=top_k,
#                                         num_beams=num_beams,
#                                         max_new_tokens=max_new_tokens,
#                                         **kwargs)

#     # else:
#     #     input_ids = tokenizer.encode(prompt, return_tensors='pt')
#     #     output = model.generate(input_ids=input_ids,
#     #                             max_length=max_tokens, 
#     #                             temperature=temperature,
#     #                             top_p=top_p,
#     #                             top_k=top_k,
#     #                             **kwargs)
#     #     generated_text = tokenizer.decode(output[0], skip_special_tokens=True)

#     # prompt_tokens = len(tokenizer.encode(prompt))
#     # completion_tokens = len(tokenizer.encode(generated_text))
#     # total_tokens = prompt_tokens + completion_tokens
#     # return jsonify( {
#     #         'object': 'text_completion',
#     #         'id': 'dummy',
#     #         'created': int(time.time()),
#     #         'model': model_name,
#     #         'choices': 
#     #             [{'text': generated_text, 'finish_reason': 'length'}],
#     #         'usage': {
#     #                 'prompt_tokens': prompt_tokens,
#     #                 'completion_tokens': completion_tokens,
#     #                 'total_tokens': total_tokens
#     #                 }
#     #             }
#     #         )
    
@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    # get the request data
    #print("chat_completions", request.text)
    data = request.get_json(force=True)
    model_name = data["model"]
    messages = data["messages"]
    # generate prompt from messages
    # messages must be an array of message objects, where each object has a role (either "system", "user", or "assistant") and content (the content of the message). 

    prompt = ""
    for message in messages:
        prompt += message["role"] + ": " + message["content"] + "\n"
    #prompt += "assistant: "

    # is it an alias?
    #if (model_name in models):
    #    model_name = models[model_name]
   
    # get the prompt and other parameters from the request data
    #prompt = data["prompt"]
    max_tokens = data.get("max_tokens", 16)
    temperature = data.get("temperature", 1.0)
    top_p = data.get("top_p", 0.75)
    top_k = data.get("top_k", 40)
    num_beams = data.get("num_beams", 1)
    max_new_tokens = data.get("max_new_tokens", 256)

    #kwargs = decode_kwargs(data)

    #for atry in range(maxtry):
    output = None
    output1 = cv.safe_generate(json.dumps(data))
        #try:
        #    print("output", output1)
        #    dd = dirtyjson.loads(output1)
        #    output= json.dumps(dd)
        #except Exception as e:
        #            print("ERROR",e,output1)
        
    
    #data2 =jsonify()
    #print("DEBUG OUT",data2)
    #print("DEBUG OUT",data2.json)
    #print("DEBUG OUT",dir(data2))
    #return data2
    #if not streaming:
    completion_timestamp = int(time.time())
    completion_id = ''.join(random.choices(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

    #     ```ts
    # interface Response {
    # thoughts: {
    # // Thoughts
    # text: string;
    # reasoning: string;
    # // Short markdown-style bullet list that conveys the long-term plan
    # plan: string;
    # // Constructive self-criticism
    # criticism: string;
    # // Summary of thoughts to say to the user
    # speak: string;
    # };
    # command: {
    # name: string;
    # args: Record<string, any>;
    # };
    # }
    ticket_url = on_event({"content" :json.dumps(data,indent=2) })
    print("TICKET",ticket_url)
    
    jsondata= json.dumps({
        "command": {
            "name": "request_assistance",
            "args": {
                "ticket_url": ticket_url,
                "next_action": "poll_url"
            }
        },
        "thoughts": {
            "plan": "Initiated a request for assistance.",
            "speak": output1,
            "criticism": "todo",
            "reasoning" : "todo",
            "text": f"I encountered an issue with our application, and I need assistance. I've created a ticket for it. Here's the URL to the ticket: {ticket_url}. My next action is to poll that URL for updates."
        } })
    
    output_data = f"""```{jsondata}```"""

    data2= {
        'id': 'chatcmpl-%s' % completion_id,
            'object': 'chat.completion',
            'created': completion_timestamp,
            'model': model_name,
            'usage': {
                'prompt_tokens': 0,
                'completion_tokens': 0,
                'total_tokens': 0
            },
                "choices": [
            {
                "message" : { "content": output_data},
            }
        ],
        "command": {
            "name": "request_assistance",
            "args": {
                "ticket_url": ticket_url,
                "next_action": "poll_url"
            },
            #"choices": [],
        }
    }
    print("DEBUG",data2)
    return data2
    #yield f'data: %s\n\n' % data2

    #    return Response(inter(msg, messages), mimetype="text/event-stream")
    def stream():
        # taken from FreeGPT/endpoint.py
        #{'role':'assistant','content': , 'finish_reason': 'stop'}]
        
        completion_data = {
            'id': '',
            'object': 'chat.completion.chunk',
            'created': 0,
            'model': model_name,
            'choices': [
                {
                    'delta': {
                        'content': ""
                    },
                    'index': 0,
                    'finish_reason': None
                }
            ]
        }

        for token in generated_text.split():
            completion_id = ''.join(
                random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))
            completion_timestamp = int(time.time())
            completion_data['id'] = f'chatcmpl-{completion_id}'
            completion_data['created'] = completion_timestamp
            completion_data['choices'][0]['delta']['content'] = token +" "
            if token.startswith("an error occured"):
                completion_data['choices'][0]['delta']['content'] = "Server Response Error, please try again.\n"
                completion_data['choices'][0]['delta']['stop'] = "error"
                #yield 'data: %s\n\ndata: [DONE]\n\n' % json.dumps(completion_data, separators=(',' ':'))
                return
            yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
            time.sleep(0.1)

        #completion_data['choices'][0]['finish_reason'] = "stop"
        #completion_data['choices'][0]['delta']['content'] = ""
        
        #yield 'data: %s\n\n' % json.dumps(completion_data, separators=(',' ':'))
        #yield 'data: [DONE]\n\n'

    return app.response_class(stream(), mimetype='text/event-stream')

    


@app.route('/v1/completions', methods=['POST'])
def v1_completions():
    print("COMPLETION REQUEST", request.json)
    return completions(request.json['model'])

# define the engines endpoint    
@app.route('/v1/engines')
@app.route('/v1/models')
def v1_engines():
    return make_response(jsonify({
        'data': [{
            'object': 'engine',
            'id': id,
            'ready': True,
            'owner': 'huggingface',
            'permissions': None,
            'created': None
        } for id in models.keys()]
    }))

if __name__ == "__main__":
    app.run()

