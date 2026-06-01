import funcoes

lista_produtos = funcoes.importador_csv('./data/olist_products_dataset.csv')
lista_ordens = funcoes.importador_csv('./data/olist_orders_dataset.csv')

print('\n ------Relatório de produtos por Categoria de produto sem tratamento:------ \n')
funcoes.relatorio_produto_categoria_sem_tratamento(lista_produtos)

contador_categorias_vazias_tratadas, contador_produtos_processados, lista_produtos_tratada = funcoes.tratamento_categoria_produto(lista_produtos)

print('\n ------Relatório de produtos por Categoria de produto com tratamento:------ \n')
print(f'Quantidade de categorias tratadas: {contador_categorias_vazias_tratadas}')
print(f'Quantidade de produtos processados: {contador_produtos_processados}')

print('\n ------Relatório de relação entre data de entrega e cancelamentos:------ \n')
contador_ordens_processadas, contador_cancelamentos = funcoes.verifica_relacao_data_entrega_e_cancelamentos(lista_ordens)

print('\n ------Relatório de tratamento de datas para o formato pt-br:------ \n')
funcoes.tratativa_data_para_ptbr(lista_ordens)

resultado_dimensoes_tratadas = funcoes.tratativa_dimensoes_produto(lista_produtos_tratada)

print('\n ------Relatório final de processamento dos dados:------ \n')
print(f'Quantidade de produtos processados: {contador_produtos_processados}')
print(f'Quantidade de ordens processadas: {contador_ordens_processadas}')
print(f'Quantidade total de registros processados: {contador_produtos_processados + contador_ordens_processadas}')
print(f'Quantidade de nulos tratados: {contador_categorias_vazias_tratadas}')
print(f'Quantidade de cancelamentos: {contador_cancelamentos}')
