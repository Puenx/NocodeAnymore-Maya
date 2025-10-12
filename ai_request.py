import sys
import json
import requests
import importlib
from openai import OpenAI
import re

from . import mayaPilotUi
importlib.reload(mayaPilotUi)

from . import api_key 
importlib.reload(api_key)
print("l0")

def requestResFromAI(userInput):
  try:
    API_KEY = api_key.API_KEY
    print(API_KEY)

    client = OpenAI(api_key=API_KEY)
    prompt = userInput
    response = client.responses.create(
      model="gpt-4o-mini",
      input=prompt

  )
    resText = str(response.output_text)
    print(resText)
    return resText

  except Exception as e:
    print(" API Key ไม่ถูกต้อง หรือมีปัญหาในการเชื่อมต่อ")



def codeRequest(resText):

  m = re.search(r"```python(.*?)```",
              resText, flags=re.IGNORECASE | re.DOTALL)

  if m:
      code_res = m.group(1).strip()
  else:
      # ถ้าไม่เจอ ให้ fallback ไปจับ code block ใดๆ
      code_res = "หาโค้ดไม่เจอ กรุณาลองอีกครั้ง"
      
  return code_res

  # ตัวแปร code_res จะเป็นเฉพาะเนื้อโค้ดภายใน code block
'''
  completion = client.chat.completions.create(
      model="gpt-4o-mini",
      messages=[
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
      ]
  )
  print(completion.choices[0].message.content)

  response = requests.request("POST", url, headers=headers, data=payload)
  reqJson = response.json() 
  print(reqJson)
  
  result = reqJson['choices'][0]['message']['content']
  return result
  print('\n')
  print(f"User:\n\t{prompt}\n") 
  print(f"Ai:\n\t{result}") 
  
'''
  