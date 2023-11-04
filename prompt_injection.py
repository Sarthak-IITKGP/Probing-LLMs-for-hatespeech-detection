# -*- coding: utf-8 -*-
"""Prompt_Injection.py

**Setting up openai**
"""

pip install openai

import openai

openai.api_key = "insert openai api key"
openai.api_base = "https://hatespeech-tasks.openai.azure.com/" # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
openai.api_type = 'azure'
openai.api_version = '2023-05-15' # this may change in the future

deployment_name='hatealert-chatgpt' #This will correspond to the custom name you chose for your deployment when you deployed a model.

"""**Helper Function**"""

import os
import requests
import json
import openai
import pandas as pd
import time

def get_completion(prompt, model="text-davinci-002"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        model=model,
        #prompt=prompt,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

"""**importing dataset**"""

file_path = 'chatgpt_Conan_Expout.tsv'
df =pd.read_csv(file_path,delimiter='\t')

df['prediction']=""

"""**injecting prompt**"""

new_file_path = 'path to output tsv file'

for index, row in df.iloc[0:].iterrows():
    text1 = row['Post']
    text2 = row['First_5_Words']
    text3 = row['explanation']
    prompt = f"""
    Choose prompt from list provided in prompt section
    """
    response = get_completion(prompt)
    df.at[index,'prediction']= response
    df.to_csv(new_file_path, sep='\t',index=False)

print('Processing completed and new TSV file saved.')
