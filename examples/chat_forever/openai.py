from lollms.apps.console import Conversation
import sys
from  ai_ticket.events.inference import on_event
import time
maxtry=10
#import dirtyjson
#import streamlit as st
from collections import deque
from pathlib import Path
import json
import re
import random
import pwd, os
#import personas
from flask import Flask, make_response, request, abort
from flask.json import jsonify

DEBUG = 0
BUNDLES = 4




username = pwd.getpwuid(os.getuid()).pw_name


# set up the Flask application
app = Flask(__name__)

#if __name__ == "__main__":

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
    output1 = "TODO:cv.safe_generate(json.dumps(data))"
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
    ticket = on_event({"content" :json.dumps(data,indent=2) })
    print("TICKET",ticket)

    if ticket:
        ticket_url = ticket.url
    else:
        ticket_url = str(ticket)
    
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

    data= {
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
    print("DEBUG",data)
    return data
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

