import os
import subprocess
import time
from datetime import datetime
import webbrowser
def calcular_porcentagem(valor, total):
    return (valor / total) * 100 if total > 0 else 0
def criar_log(pasta, total_arquivos, executados_com_sucesso, bloqueados, eficiencia_bloqueio, detalhes_executaveis):
    data_hora_atual = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    nome_arquivo_log = f"log_{data_hora_atual}.txt"
    caminho_completo = os.path.join(os.path.dirname(os.path.realpath(__file__)), nome_arquivo_log)
    
    with open(caminho_completo, 'w', encoding='utf-8') as arquivo_log:
        arquivo_log.write(f"Data e Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        arquivo_log.write(f"Número de objetos na pasta: {total_arquivos}\n")
        arquivo_log.write(f"Número de objetos executados: {executados_com_sucesso}\n")
        arquivo_log.write(f"Número de objetos bloqueados: {bloqueados}\n")
        arquivo_log.write(f"Percentual de eficiência do bloqueio: {eficiencia_bloqueio:.2f}%\n")
        arquivo_log.write("Detalhes dos executáveis:\n")
        for detalhe in detalhes_executaveis:
            arquivo_log.write(f"{detalhe}\n")
    
    return caminho_completo
def executar_executaveis(pasta):
    arquivos = os.listdir(pasta)
    total_arquivos = len(arquivos)
    executaveis = [arquivo for arquivo in arquivos if arquivo.endswith(('.exe', '.msi', '.jar', '.java', '.pdf'))]
    detalhes_executaveis = []
    executados_com_sucesso = bloqueados = 0 
    
    for indice, executavel in enumerate(executaveis, start=1):
        caminho_executavel = os.path.join(pasta, executavel)
        status = "Executado"
        try:
            processo = subprocess.Popen(caminho_executavel)
            time.sleep(5)
            if processo.poll() is not None:
                status = "Bloqueado"
        except Exception as e:
            status = "Bloqueado"
        print(f'Arquivo [{indice} de {len(executaveis)}] - {executavel} - Progresso: {int((indice / len(executaveis)) * 100)}%')
        
        try:
            processo = subprocess.Popen(caminho_executavel)
            time.sleep(5)
            if processo.poll() is not None:
                bloqueados += 1
                detalhes_executaveis.append(f"{executavel} (Bloqueado)")
                print("Status: Bloqueado")
            else:
                executados_com_sucesso += 1
                detalhes_executaveis.append(f"{executavel} (Executando)")
                print("Status: Executando")
                processo.terminate()  # Opcional, dependendo do seu caso de uso
        except Exception as e:
            erro = str(e)
            if "access denied" in erro.lower() or "WinError 5" in erro or "WinError 193" in erro or "WinError 129" in erro or "WinError 216" in erro or "WinError 2" in erro:
                bloqueados += 1
                detalhes_executaveis.append(f"{executavel} (Bloqueado - Acesso negado)")
                print("Status: Bloqueado - Acesso negado")
            else:
                bloqueados += 1
                detalhes_executaveis.append(f"{executavel} (Bloqueado - {erro})")
                print(f"Erro ao executar {executavel}: {erro}")
    
    eficiencia_bloqueio = calcular_porcentagem(bloqueados, len(executaveis))
    caminho_log = criar_log(pasta, total_arquivos, executados_com_sucesso, bloqueados, eficiencia_bloqueio, detalhes_executaveis)
    
    if caminho_log:
        webbrowser.open(caminho_log)
    else:
        print("Não foi possível criar o arquivo de log.")
pasta_executaveis = input('Digite o caminho da pasta onde estão os executáveis: ')
protecao_ativada = input('A proteção em tempo real está ativada? (Y/N): ').strip().upper()
if protecao_ativada == 'Y':
    executar_executaveis(pasta_executaveis)
else:
    print('Proteção em tempo real desativada. Os executáveis não serão executados.')
