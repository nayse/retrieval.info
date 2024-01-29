import json
import os

caminho_saida = r"your_path"

# verificar se o arquivo existe e não está vazio
if os.path.exists(caminho_saida) and os.path.getsize(caminho_saida) > 0:
    with open(caminho_saida, 'r', encoding='utf-8') as arquivo_json:
        dados_json = json.load(arquivo_json)

    campos_esperados = ['title', 'publication_date', 'summary', 'Fabricante', 'Modelo', 'URL', 'E-mail', 'Versão do Android']


    total_campos_corretos = 0
    total_campos_incorretos = 0
    total_campos_esperados = len(campos_esperados)


    for i, documento in enumerate(dados_json, 1):
        print(f"\nDocumento {i}:")

        campos_corretos = 0
        campos_incorretos = 0

        # verifica se cada campo está preenchido corretamente
        for campo in campos_esperados:
            valor_campo = documento.get(campo, 'Não encontrado')

            preenchido_corretamente = (
                campo in documento and
                valor_campo not in ('', 'N/I', 'Null', 'null', 'N/A')
            )


            if preenchido_corretamente:
                campos_corretos += 1
            else:
                campos_incorretos += 1
  

        # acurácia para este documento
        acuracia_documento = campos_corretos / total_campos_esperados
        print(f'Acurácia do Documento: {acuracia_documento:.2%}')

        total_campos_corretos += campos_corretos
        total_campos_incorretos += campos_incorretos

    #calcular a taxa média de preenchimento correto e a taxa média de preenchimento incorreto por documento
    taxa_media_preenchimento_correto = total_campos_corretos / (len(dados_json) * total_campos_esperados)
    taxa_media_preenchimento_incorreto = total_campos_incorretos / (len(dados_json) * total_campos_esperados)

    print("-------")

    print("Campos Totais", 58*8)
    print("Total de campos sem Valores Nulos", total_campos_corretos)
    print("Total de campos com Valores Nulos", total_campos_incorretos)
    print("Total de campos por Doc", total_campos_esperados)
    print(f'\nTaxa Média de Campos Preenchidos de todos os Documento: {taxa_media_preenchimento_correto:.2%}')
    print(f'Taxa Média de Campos não preenchidos de todos os Documento (Campos Não existem em tittle, summary) : {taxa_media_preenchimento_incorreto:.2%}')
else:
    print("O arquivo não existe ou está vazio.")

####################

with open(caminho_saida, 'r', encoding='utf-8') as arquivo_json:
    dados_json = json.load(arquivo_json)

campos_esperados = ['title', 'publication_date', 'summary', 'Fabricante', 'Modelo', 'URL', 'E-mail', 'Versão do Android']

documentos_com_campos_corretos = 0
documentos_sem_campos_corretos = 0

for i, documento in enumerate(dados_json, 1):
    todos_campos_corretos = all(documento.get(campo, '') not in ('', 'N/I', 'Null', 'null', 'N/A') for campo in campos_esperados)

    if todos_campos_corretos:
        documentos_com_campos_corretos += 1
    else:
        documentos_sem_campos_corretos += 1

print(f"\nNúmero total de documentos com todos os campos preenchidos com todas as informações: {documentos_com_campos_corretos}")
print(f"Número total de documentos com campos preenchidos corretamente porém com valores 'N/I', 'Null', 'null', 'N/A' etc: {documentos_sem_campos_corretos}")
