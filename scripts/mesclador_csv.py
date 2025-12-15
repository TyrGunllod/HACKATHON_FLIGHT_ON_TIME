import os
import pandas as pd # Importa a biblioteca Pandas

# --- Configurações Iniciais ---

# 1. Dicionário para forçar o tipo de dado da coluna 'CANCELLED' para float.
# Isso resolve o DtypeWarning, pois o float aceita valores numéricos e nulos (NaN).
tipos_para_forcar = {
    'CANCELLED': float  
}

# 2. Defina o caminho para a pasta que contém os arquivos CSV
pasta_de_entrada = 'T_ONTIME_REPORTING' 

# 3. Defina o nome do arquivo final CSV
nome_arquivo_saida = 'T_ONTIME_REPORTING_2021_2025.csv'

# 4. Lista para armazenar todos os DataFrames (tabelas) lidos
lista_dataframes = []

# --- Função Principal de Mesclagem de CSV ---

def mesclar_csv(caminho_pasta, arquivo_saida):
    """
    Lê todos os arquivos CSV em uma pasta, mescla-os em um único DataFrame e salva o resultado.
    """
    
    print(f"Buscando arquivos CSV na pasta: {caminho_pasta}")

    # Iterar sobre todos os arquivos na pasta
    for nome_arquivo in os.listdir(caminho_pasta):
        
        if nome_arquivo.endswith('.csv'):
            caminho_completo_arquivo = os.path.join(caminho_pasta, nome_arquivo)
            
            try:
                # 5. Ler o arquivo CSV usando a função read_csv do Pandas
                # Aplicando o 'dtype' para a coluna 'CANCELLED' e 'low_memory=False'
                df_temp = pd.read_csv(
                    caminho_completo_arquivo,
                    dtype=tipos_para_forcar,
                    low_memory=False
                )
                
                # Adicionar o DataFrame lido à nossa lista
                lista_dataframes.append(df_temp)
                
                print(f"  [SUCESSO] Arquivo '{nome_arquivo}' lido e adicionado.")
                
            except Exception as e:
                # Tratar erros de leitura
                print(f"  [ERRO] Não foi possível ler o arquivo CSV '{nome_arquivo}'. Erro: {e}")
    
    
    # Verificar se algum DataFrame foi lido
    if not lista_dataframes:
        print("\n--- RESUMO ---")
        print("Nenhum arquivo CSV foi encontrado ou lido com sucesso na pasta.")
        return 


    # 6. Mesclar todos os DataFrames da lista em um único DataFrame
    try:
        df_final = pd.concat(lista_dataframes, ignore_index=True)
        
        # 7. Salvar o DataFrame final em um novo arquivo CSV
        df_final.to_csv(arquivo_saida, index=False, encoding='utf-8')
        
        # 8. Exibir resumo final
        print("\n--- RESUMO DA MESCLAGEM ---")
        print("Mesclagem concluída com sucesso!")
        print(f"Total de linhas (registros) no arquivo final: {len(df_final)}")
        print(f"Resultado salvo em: {os.path.abspath(arquivo_saida)}")
        
    except Exception as e:
        # 9. Tratar erros durante a concatenação ou escrita
        print(f"\n[ERRO CRÍTICO] Falha ao concatenar ou escrever o arquivo de saída. Erro: {e}")


# --- Execução do Script ---
if __name__ == '__main__':
    mesclar_csv(pasta_de_entrada, nome_arquivo_saida)
