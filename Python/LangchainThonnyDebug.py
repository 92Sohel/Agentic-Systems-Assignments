import requests
import json

ollama_host="http://localhost:11434"

api_path="/api/chat"

url=ollama_host+api_path

model_name= "gemma3:1b"

prompt="explain SQL fundamentals in a begginer friendly way"

payload={
    "model":model_name,
    "messages":[
        {"role":"user",
         "content":prompt,
         }
    ],
    "stream":True,
}

response = requests.post(url,json=payload,stream=True,timeout=120)

for line in response.iter_lines():
    if line:
        data = json.loads(line)

        if "message" in data:
            print(data["message"]["content"], end="", flush=True)

print()