import json
import re

caminho_entrada = r"C:\Users\mayse\OneDrive\Documentos\rii2\corpus.json"

with open(caminho_entrada, 'r', encoding='utf-8') as arquivo_json:
    dados_json = json.load(arquivo_json)


def extrair_fabricante_e_modelo(texto, fabricantes_presentes):
    fabricante_encontrado = None
    modelo_encontrado = None

    for fabricante in fabricantes_presentes:
        #regex para encontrar o fabricante no texto
        match = re.search(fabricante, texto, flags=re.IGNORECASE)
        if match:
            fabricante_encontrado = match.group(0)
            break  #parar aqui quando o fabricante for encontrado

    if fabricante_encontrado:
        fabricante_escapado = re.escape(fabricante_encontrado)

        # busca o nome do modelo após o nome do fabricante no texto
        nome_modelo_match = re.search(rf'{fabricante_escapado}\s*([^0-9]+)', texto, flags=re.IGNORECASE)
        nome_modelo = nome_modelo_match.group(1).strip() if nome_modelo_match else "N/A"

        print((f"nome_modelo2: {nome_modelo}"))

        #busca o numero do modelo após o nome do modelo
        numeral_modelo_match = re.search(rf'{re.escape(nome_modelo)}\s*([\d]+)', texto, flags=re.IGNORECASE)
        numeral_modelo = numeral_modelo_match.group(1).strip() if numeral_modelo_match else "N/A"

        print((f"numeral_modelo: {numeral_modelo}"))

        # condição para definir modelo como None se fabricante for None
        if numeral_modelo != "N/A":
            #verificar se a palavra imediatamente anterior a numeral_modelo é "android" (ignorando o caso)
            anterior_android_match = re.search(rf'\bAndroid\b', texto, flags=re.IGNORECASE)
            if anterior_android_match:
                # caso seja, definir nome_modelo como a primeira e segunda palavra após o nome do fabricante
                palavras_apos_fabricante_match = re.search(rf'{re.escape(fabricante_escapado)}\s+(\w+)\s+(\w+)', texto, flags=re.IGNORECASE)
                nome_modelo = f"{palavras_apos_fabricante_match.group(1).strip()} {palavras_apos_fabricante_match.group(2).strip()}" if palavras_apos_fabricante_match else "N/A"

                #combinar o nome e o numeral do modelo
                modelo_encontrado = f"{nome_modelo}"
            else:
                
                modelo_encontrado = f"{nome_modelo} {numeral_modelo}"
        else:
            modelo_encontrado = f"{nome_modelo} {numeral_modelo}"

    return fabricante_encontrado, modelo_encontrado

#fabricantes
fabricantes_presentes = {"Motorola", "Cubot", "Alcatel", "Xiaomi", "Samsung", "Ulefone", "Jinga", "Redmi", "Vivo"}

#extrair fabricante, modelo e versão
for i, documento in enumerate(dados_json, 1):

    fabricante, modelo = extrair_fabricante_e_modelo(f"{documento.get('title', '')} {documento.get('summary', '')}", fabricantes_presentes)

    documento['Fabricante'] = fabricante
    documento['Modelo'] = modelo

    # mudar urls
    if 'http://' in documento.get('summary', ''):
        documento['summary'] = documento['summary'].replace('http://', 'https://')
    elif 'https://' in documento.get('summary', ''):
        documento['summary'] = documento['summary'].replace('https://', 'http://')
    elif 'www.' in documento.get('summary', ''):
        documento['summary'] = documento['summary'].replace('www.', 'www_')

    # inverter a data no formato DD/MM/AAAA 
    ano, mes, dia = documento.get('publication_date', '')[:10].split('-')
    data_invertida = f"{dia}-{mes}-{ano}"
    documento['publication_date'] = data_invertida

    # extrair url e email
    url_match = re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
                          documento.get('summary', ''))
    documento['URL'] = url_match.group(0) if url_match else 'N/I'

    email_match = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', documento.get('summary', ''))
    documento['E-mail'] = email_match.group(0) if email_match else 'N/I'

    # extrair a versão do android do título
    versao_android_titulo = re.search(r'Android\s*([\d.,]+)', documento.get('title', ''), flags=re.IGNORECASE)

    # extrair a versão do android do sumário
    versao_android_sumario = re.search(r'Android\s*([\d.,]+)', documento.get('summary', ''), flags=re.IGNORECASE)

    #escolher a versão do android encontrada (pode ser do título ou do sumário)
    versao_android = versao_android_titulo.group(1).strip() if versao_android_titulo else 'N/I'
    if not versao_android or versao_android == 'N/I':
        versao_android = versao_android_sumario.group(1).strip() if versao_android_sumario else 'N/I'

    documento['Versão do Android'] = versao_android

    print(f"\nOUTPUT (template):")
    print(f"1. Título: {documento.get('title', '')}")
    print(f"2. Data invertida: {documento.get('publication_date', '')}")
    print(f"3. Fabricante: {documento.get('Fabricante', '')}")
    print(f"4. Modelo: {documento.get('Modelo', '')}")
    print(f"5. Versão do Android: {documento.get('Versão do Android', '')}")
    print(f"6. URL: {documento.get('URL', '')}")
    print(f"7. E-mail: {documento.get('E-mail', '')}")
    print(f"8. Resumo = {documento.get('summary', '')}")


caminho_saida = r"C:\Users\mayse\OneDrive\Documentos\rii2\saida_corpus.json"
with open(caminho_saida, 'w', encoding='utf-8') as arquivo_saida:
    json.dump(dados_json, arquivo_saida, indent=2, ensure_ascii=False)

print(f"\nSaída final salva no arquivo '{caminho_saida}'.")
