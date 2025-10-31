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


def requestResFromAI(userInput):
  try:
    API_KEY = api_key.API_KEY
    print(API_KEY)

    client = OpenAI(api_key=API_KEY)
    prompt = f"Create simple Python code for Maya: {userInput}. Always reply with python code block. Keep code simple & short."
    response = client.responses.create(
      model="gpt-5",
      input= prompt,

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
