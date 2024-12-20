import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Dados predefinidos para as 10 mercadorias
itens_predefinidos = [
    {"nome": "Mercadoria 1", "peso": 50, "volume": 3},
    {"nome": "Mercadoria 2", "peso": 30, "volume": 2},
    {"nome": "Mercadoria 3", "peso": 80, "volume": 5},
    {"nome": "Mercadoria 4", "peso": 60, "volume": 4},
    {"nome": "Mercadoria 5", "peso": 40, "volume": 3},
    {"nome": "Mercadoria 6", "peso": 70, "volume": 5},
    {"nome": "Mercadoria 7", "peso": 25, "volume": 2},
    {"nome": "Mercadoria 8", "peso": 90, "volume": 6},
    {"nome": "Mercadoria 9", "peso": 55, "volume": 4},
    {"nome": "Mercadoria 10", "peso": 45, "volume": 3},
]

# Função de otimização multi-objetivo usando Programação Dinâmica
def knapsack_multiobjetivo(capacidade_peso, capacidade_volume, itens, peso_peso=1, peso_volume=1):
    n = len(itens)
    
    # Inicializando a matriz de programação dinâmica para peso e volume
    dp = np.zeros((n + 1, capacidade_peso + 1, capacidade_volume + 1))
    
    for i in range(1, n + 1):
        for w in range(capacidade_peso + 1):
            for v in range(capacidade_volume + 1):
                peso_item = itens[i - 1]['peso']
                volume_item = itens[i - 1]['volume']
                
                # Combinando peso e volume com pesos
                if peso_item <= w and volume_item <= v:
                    utilidade = peso_peso * peso_item + peso_volume * volume_item
                    dp[i][w][v] = max(dp[i - 1][w][v], 
                                       dp[i - 1][w - peso_item][v - volume_item] + utilidade)
    
    # Recuperando os itens selecionados
    w, v = capacidade_peso, capacidade_volume
    itens_selecionados = []
    for i in range(n, 0, -1):
        if dp[i][w][v] != dp[i - 1][w][v]:
            itens_selecionados.append(itens[i - 1])
            w -= itens[i - 1]['peso']
            v -= itens[i - 1]['volume']
    
    return itens_selecionados, dp[n][capacidade_peso][capacidade_volume]

# Interface do Streamlit
st.title("Otimização de Carregamento de Caminhão - Problema da Mochila 0-1")

# Entradas do usuário para a capacidade do caminhão
capacidade_peso = st.slider("Capacidade de Peso do Caminhão (kg)", 100, 500, 300)
capacidade_volume = st.slider("Capacidade de Volume do Caminhão (m³)", 10, 50, 30)

# Exibindo as 10 mercadorias predefinidas
st.subheader("Mercadorias Predefinidas")
df_predefinidos = pd.DataFrame(itens_predefinidos)
st.dataframe(df_predefinidos)

# Entradas dinâmicas para mercadorias adicionais
st.subheader("Adicione Mercadorias")
itens_adicionais = []

# Definindo o número de mercadorias adicionais que o usuário quer adicionar
num_itens_adicionais = st.number_input("Quantas mercadorias adicionais você deseja adicionar?", min_value=1, max_value=20, value=5)

# Campos de entrada para cada mercadoria adicional
for i in range(num_itens_adicionais):
    nome = st.text_input(f"Nome da Mercadoria Adicional {i+1}")
    peso = st.number_input(f"Peso da Mercadoria Adicional {i+1} (kg)", min_value=1, value=10)
    volume = st.number_input(f"Volume da Mercadoria Adicional {i+1} (m³)", min_value=1, value=1)

    # Adiciona o item à lista
    if nome:
        itens_adicionais.append({"nome": nome, "peso": peso, "volume": volume})

# Exibindo as mercadorias adicionais como tabela
if len(itens_adicionais) > 0:
    df_adicionais = pd.DataFrame(itens_adicionais)
    st.subheader("Mercadorias Adicionais")
    st.dataframe(df_adicionais)

# Exibindo a tabela final com todas as mercadorias (predefinidas + adicionais)
if len(itens_adicionais) > 0 or len(itens_predefinidos) > 0:
    st.subheader("Tabela Final de Mercadorias")
    itens_totais = itens_predefinidos + itens_adicionais
    df_final = pd.DataFrame(itens_totais)
    st.dataframe(df_final)

# Botão para executar a otimização
if st.button("Alocar Carga"):
    if len(itens_adicionais) == 0 and len(itens_predefinidos) == 0:
        st.warning("Adicione pelo menos uma mercadoria para otimizar o carregamento.")
    else:
        # Concatenando as mercadorias predefinidas e as adicionais
        itens_totais = itens_predefinidos + itens_adicionais

        # Chamada à função de otimização multi-objetivo (knapsack com peso e volume)
        carga, utilidade_total = knapsack_multiobjetivo(capacidade_peso, capacidade_volume, itens_totais)
        
        # Exibir o resultado
        st.write(f"Utilidade total (peso + volume): {utilidade_total}")
        st.write(f"Mercadorias carregadas no caminhão:")
        for item in carga:
            st.write(f"- {item['nome']} (Peso: {item['peso']} kg, Volume: {item['volume']} m³)")
        
        # Gráfico da alocação de carga
        mercadorias = [item["nome"] for item in carga]
        pesos = [item["peso"] for item in carga]
        volumes = [item["volume"] for item in carga]

        fig, ax = plt.subplots(1, 2, figsize=(12, 6))
        
        # Gráfico de peso
        ax[0].bar(mercadorias, pesos, color='blue')
        ax[0].set_title('Distribuição de Peso das Mercadorias')
        ax[0].set_xlabel('Mercadorias')
        ax[0].set_ylabel('Peso (kg)')
        ax[0].tick_params(axis='x', rotation=45)  # Rotacionar os rótulos para evitar sobreposição

        # Gráfico de volume
        ax[1].bar(mercadorias, volumes, color='green')
        ax[1].set_title('Distribuição de Volume das Mercadorias')
        ax[1].set_xlabel('Mercadorias')
        ax[1].set_ylabel('Volume (m³)')
        ax[1].tick_params(axis='x', rotation=45)  # Rotacionar os rótulos para evitar sobreposição

        st.pyplot(fig)

        # Explicação sobre a técnica de otimização
        st.subheader("Explicação sobre a Técnica de Otimização - Problema da Mochila 0-1")
        st.write("""
            O **Problema da Mochila 0-1** otimizado foi abordado usando a Programação Dinâmica, onde consideramos tanto o peso quanto o volume das mercadorias. O objetivo é maximizar a **utilização das capacidades de peso e volume do caminhão** ao mesmo tempo.
            
            **Como Analisar os Resultados:**
            - O modelo seleciona a combinação de mercadorias que mais utiliza o espaço disponível, tanto em termos de peso quanto de volume, sem exceder a capacidade máxima do caminhão.
            - A tabela de resultados mostra as mercadorias selecionadas, o peso e o volume de cada uma, além da utilidade total (combinando peso e volume).

            **Por que o Resultado Ficou Assim:**
            - O algoritmo seleciona a combinação de mercadorias que maximiza a utilidade ponderada entre peso e volume, levando em consideração as restrições de capacidade.
            - A visualização gráfica ajuda a compreender como o espaço e o peso são distribuídos entre as mercadorias selecionadas, permitindo verificar a eficiência do carregamento.
        """)
