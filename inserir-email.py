import os
import random
import json


emails = ["usuario1@example.com", "teste123@gmail.com", "contato_xyz@yahoo.com", "suporte_abc@samsung.com", "info_mn@motorola.com", "pessoa_789@tools.com", "email_teste_1@example.com", "usuario_2@gmail.com", "contato_456@yahoo.com", "suporte_123@samsung.com", "info_abc@motorola.com", "pessoa_xyz@tools.com", "email_789@example.com", "teste_3@gmail.com", "contato_abc@yahoo.com"]
urls = ["http://www.exemplo_1.com", "https://empresa_teste.com.br", "www.exemplo_2.net", "http://www.site_abc.com", "https://companhia_xyz.org", "www.teste_123.net", "http://www.nova_empresa.com", "https://site_teste_1.com.br", "www.url_exemplo.net", "http://www.teste_abc.com", "https://novo_site.org.br", "www.url_teste.net", "http://www.outra_empresa.com", "https://site_xyz.com.br", "www.url_123.net"]

caminho_input = r"your_path"


with open(caminho_input, 'r', encoding='utf-8') as file:
    artigos = json.load(file)

random.shuffle(emails)

for i, artigo in enumerate(artigos):
    artigo["summary"] = artigo["summary"].replace("[factory reset]", f"[factory reset]({emails[i % len(emails)]})")


caminho_output = r"your_path"


with open(caminho_output, 'w') as file:
    json.dump(artigos, file, indent=4)


for i, artigo in enumerate(artigos):
    print(f"Artigo {i+1}:\n{json.dumps(artigo, indent=4)}\n")
