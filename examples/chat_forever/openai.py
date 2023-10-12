from lollms.apps.console import Conversation
import sys
from  ai_ticket.events.inference import on_event
from examples.chat_forever import docker_controller
import time
maxtry=10
from collections import deque
from pathlib import Path
import json
import re
import random
import pwd, os
from flask import Flask, make_response, request, abort
from flask.json import jsonify
DEBUG = 0
BUNDLES = 4
username = "username"
app = Flask(__name__)
models = {}

from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
llm = OpenAI()
template = """Question: {question}

Answer: Let's think step by step."""

prompt = PromptTemplate(template=template, input_variables=["question"])
llm_chain = LLMChain(prompt=prompt, llm=llm)


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

    question = prompt
    
    output1 = llm_chain.run(question)
    completion_timestamp = int(time.time())
    completion_id = ''.join(random.choices(
        'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789', k=28))

    # create a ticket for the request
    ticket = on_event({"content" :json.dumps(data,indent=2) })
    print("TICKET",ticket)

    ticket_url = ticket

    jsondata= json.dumps({
        "command": {
            "name": "request_assistance",
            "args": {        "ticket_url": ticket_url,     "next_action": "poll_url"            }        },
        "thoughts": {
            "plan": "Initiated a request for assistance.",
            "speak": output1,
            "criticism": "todo",
            "reasoning" : "todo",
            "text": f"I encountered an issue with our application, and I need assistance. I've created a ticket for it. Here's the URL to the ticket: {ticket_url}. My next action is to poll that URL for updates."
        } })

    #this  is the mock json data from the llm itself
    output_data = jsondata#f"""```{jsondata}```"""

    ##### this is the new ticket for the user to replace
    data2 =   {
            "command": {
                "name": "execute_python_code",
                "args" : { "code": "print(42)" },
            },
            "thoughts": {
                "plan": output1,
                "speak": "This is where you speak to the requesting user. Replace the command above and this text with your results",
                "criticism": "todo",
                "reasoning" : json.dumps(docker_controller.inspect()),
                "text": f"This template will be executed."
            }}
    # create a second ticket to handle the agent
    ticket2 = on_event({"content" : json.dumps(data2) })
    ticket_url = ticket2

    return {
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
                "message" : { "content": json.dumps({
        "command": {
            "name": "request_assistance",
            "args": {        "ticket_url": ticket_url,     "next_action": "poll_url"            }        },
        "thoughts": {
            "plan": "Initiated a request for assistance.",
            "speak": output1,
            "criticism": "todo",
            "reasoning" : "todo",
            "text": f"I encountered an issue with our application, and I need assistance. I've created a ticket for it. Here's the URL to the ticket: {ticket_url}. My next action is to poll that URL for updates."
        } })},
            }
        ],
        "thoughts": {
            "plan": "Initiated a request for assistance.",
            "speak": "asking for help",
            "criticism": "todo",
            "reasoning" : "todo",
            "text": f"testing."
        },
        "command": {
            "name": "request_assistance",
            "args": {
                "ticket_url": ticket_url,
                "next_action": "poll_url"
            }
        }
    }


    


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
    app.run(host="0.0.0.0")

