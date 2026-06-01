import csv
import re
from datetime import datetime

'''
Função para importar dados de um arquivo CSV e retornar uma lista de dicionários. Cada dicionário representa uma linha do arquivo, 
com as chaves correspondendo aos nomes das colunas.
'''
def importador_csv(nome_arquivo):
    with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
        leitor = csv.DictReader(arquivo)
        dados = list(leitor)
    return dados

'''
Função para gerar um relatório informando a quantidade de nulos e vazios, a quantidade de registros com caracteres especiais e 
a quantidade de registros com letras maiúsculas na coluna product_category_name.
'''
def relatorio_produto_categoria_sem_tratamento(lista_produtos):
    contador_vazios_nulos = 0
    contador_caracteres_especiais = 0
    contador_maiusculas = 0

    # Verificador de quantidade de registros com diferentes tipos de valores na coluna 'product_category_name'
    for linha in lista_produtos:
        if linha['product_category_name'] == '' or linha['product_category_name'] == None:
            contador_vazios_nulos += 1
        if re.search(r'[^a-zA-Z0-9]', linha['product_category_name']) and linha['product_category_name'] != 'sem categoria':
            contador_caracteres_especiais += 1
        if re.search(r'[A-Z]', linha['product_category_name']):
            contador_maiusculas += 1

    print(f'Quantidade de registros vazios na coluna Categoria de produto: {contador_vazios_nulos}')
    print(f'Quantidade de registros com caracteres especiais na coluna Categoria de produto: {contador_caracteres_especiais}')
    print(f'Quantidade de registros com letras maiúsculas na coluna Categoria de produto: {contador_maiusculas}')

'''
Função para tratar a categoria do produto, preenchendo os valores vazios ou nulos com "sem categoria", convertendo para minúsculas 
e tirando os espaços em branco(no começo e fim) e removendo os caracteres especiais.
'''
def tratamento_categoria_produto(lista_produtos):
    contador_categorias_vazias_tratadas = 0
    contador_produtos_processados = 0

    for linha in lista_produtos:
    
        # Preenche os valores vazios ou nulos da categoria do produto com "sem categoria"
        if linha['product_category_name'] == '' or linha['product_category_name'] == None:
           linha['product_category_name'] = 'sem categoria'
           contador_categorias_vazias_tratadas += 1

        # Converte a categoria do produto para minúsculas e remove espaços em branco no início e no final
        linha['product_category_name'] = linha['product_category_name'].strip().lower()
        contador_produtos_processados += 1

        # Remove caracteres especiais da categoria do produto
        linha['product_category_name'] = re.sub(r'[^a-zA-Z0-9\s]', '', linha['product_category_name'])
        contador_produtos_processados += 1

    return contador_categorias_vazias_tratadas, contador_produtos_processados, lista_produtos

'''
Função para verificar a relação entre a data de entrega e os cancelamentos, contando a quantidade de registros com data 
de entrega vazia, a quantidade de registros com data de entrega vazia e cancelamentos, a quantidade total de cancelamentos
e o percentual de registros com data de entrega vazia que não são cancelamentos.
'''
def verifica_relacao_data_entrega_e_cancelamentos(lista_ordens):
    contador_data_entrega_vazia = 0
    contador_data_entrega_vazia_com_cancelamentos = 0
    contador_cancelamentos = 0
    contador_ordens_processadas = 0

    for linha in lista_ordens:
        contador_ordens_processadas += 1
        if linha['order_delivered_customer_date'] == '' or linha['order_delivered_customer_date'] == None:
            contador_data_entrega_vazia += 1
            if linha['order_status'] == 'canceled':
                contador_data_entrega_vazia_com_cancelamentos += 1
        if linha['order_status'] == 'canceled':
            contador_cancelamentos += 1

    print(f'Quantidade de registros com data de entrega vazia: {contador_data_entrega_vazia}')
    print(f'Quantidade de registros com data de entrega vazia e cancelamentos: {contador_data_entrega_vazia_com_cancelamentos}')
    print(f'Quantidade total de cancelamentos: {contador_cancelamentos}')

    # Verifica qual o percentual de registros com data de entrega vazia que não são cancelamentos.
    if contador_data_entrega_vazia > 0:
        percentual = (contador_data_entrega_vazia - contador_data_entrega_vazia_com_cancelamentos) / contador_data_entrega_vazia * 100
        print(f'Percentual de registros com data de entrega vazia que não são cancelamentos: {percentual:.2f}%')
    
    return contador_ordens_processadas, contador_cancelamentos

'''
Função para tratar a data de aprovação do pedido, convertendo para o formato pt-BR (dd/mm/aaaa).
'''
def tratativa_data_para_ptbr(lista_ordens):
    for linha in lista_ordens:
        contador_ordens_processadas = 0
        if linha['order_approved_at'] != '' and linha['order_approved_at'] != None:
            contador_ordens_processadas += 1    
            ## Converte a data para o formato pt-BR com função datetime do módulo datetime brasileiro (ex: "dd/mm/aaaa")
            data = datetime.strptime(linha['order_approved_at'], '%Y-%m-%d %H:%M:%S')
            linha['order_approved_at'] = data.strftime('%d/%m/%Y')

    print(f'Quantidade de ordens processadas: {contador_ordens_processadas}')   

    for linha in lista_ordens:
        if linha['order_approved_at'] != '' and linha['order_approved_at'] != None:
            print(f'Exemplo de data convertida para o formato pt-BR: {linha["order_approved_at"]}')
            break     

    return contador_ordens_processadas, lista_ordens

'''
Função para tratar as dimensões do produto, preenchendo os valores vazios ou nulos com a média das 
dimensões de outros produtos da mesma categoria. Se não houver registros para essa categoria, 
o produto é excluído do dataset. Para um tratamento mais acertivo, a função trata cada dimensão 
(length, height, width e weight) separadamente, verificando a média apenas dos os produtos 
com a mesma categoria.
'''
def tratativa_dimensoes_produto(lista_produtos):
    produtos_remover = []
    
    for linha in lista_produtos:
        categoria = linha['product_category_name']
        
        # Trata a coluna product_length_cm
        if linha['product_length_cm'] == '' or linha['product_length_cm'] is None:
            produtos_com_length = []
            for produto in lista_produtos:
                if produto['product_category_name'] == categoria and produto['product_length_cm'] != '' and produto['product_length_cm'] is not None:
                    produtos_com_length.append(produto)
            
            if len(produtos_com_length) > 0:
                soma = 0.0
                for produto in produtos_com_length:
                    soma += float(produto['product_length_cm'])
                media = int(soma / len(produtos_com_length))
                linha['product_length_cm'] = str(media)
            else:
                if linha not in produtos_remover:
                    produtos_remover.append(linha)
        
        # Trata a coluna product_height_cm
        if linha['product_height_cm'] == '' or linha['product_height_cm'] is None:
            produtos_com_height = []
            for produto in lista_produtos:
                if produto['product_category_name'] == categoria and produto['product_height_cm'] != '' and produto['product_height_cm'] is not None:
                    produtos_com_height.append(produto)
            
            if len(produtos_com_height) > 0:
                soma = 0.0
                for produto in produtos_com_height:
                    soma += float(produto['product_height_cm'])
                media = int(soma / len(produtos_com_height))
                linha['product_height_cm'] = str(media)
            else:
                if linha not in produtos_remover:
                    produtos_remover.append(linha)
        
        # Trata a coluna product_width_cm
        if linha['product_width_cm'] == '' or linha['product_width_cm'] is None:
            produtos_com_width = []
            for produto in lista_produtos:
                if produto['product_category_name'] == categoria and produto['product_width_cm'] != '' and produto['product_width_cm'] is not None:
                    produtos_com_width.append(produto)
            
            if len(produtos_com_width) > 0:
                soma = 0.0
                for produto in produtos_com_width:
                    soma += float(produto['product_width_cm'])
                media = int(soma / len(produtos_com_width))
                linha['product_width_cm'] = str(media)
            else:
                if linha not in produtos_remover:
                    produtos_remover.append(linha)
        
        # Trata a coluna product_weight_g
        if linha['product_weight_g'] == '' or linha['product_weight_g'] is None:
            categoria = linha['product_category_name']
            produtos_categoria = []

            for produto in lista_produtos:
                if produto['product_category_name'] == categoria and produto['product_weight_g'] != '' and produto['product_weight_g'] is not None:
                    produtos_categoria.append(produto)

            if len(produtos_categoria) > 0:
                soma = 0.0

                for produto in produtos_categoria:
                    soma += float(produto['product_weight_g'])
                media_weight = int(soma / len(produtos_categoria))
                linha['product_weight_g'] = str(media_weight)
            else:
                if linha not in produtos_remover:
                    produtos_remover.append(linha)
    
    # Remove produtos que não puderam ser tratados
    for produto in produtos_remover:
        lista_produtos.remove(produto)
        
    return lista_produtos
