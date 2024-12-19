import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Função de otimização: Alocar as mercadorias no caminhão
def alocar_carga(capacidade_peso, capacidade_volume, itens):
    carga_atual = []
    peso_atual = 0
    volume_atual = 0
    for item in itens:
        if peso_atual + item["peso"] <= capacidade_peso and volume_atual + item["volume"] <= capacidade_volume:
            carga_atual.append(item)
            peso_atual += item["peso"]
            volume_atual += item["volume"]
    return carga_atual, peso_atual, volume_atual

# Interface do Streamlit
st.title("Otimização de Carregamento de Caminhão")

# Entradas do usuário para a capacidade do caminhão
capacidade_peso = st.slider("Capacidade de Peso do Caminhão (kg)", 100, 500, 300)
capacidade_volume = st.slider("Capacidade de Volume do Caminhão (m³)", 10, 50, 30)

# Entradas dinâmicas para mercadorias
st.subheader("Adicione Mercadorias")
itens = []

# Definindo o número de mercadorias que o usuário quer adicionar
num_itens = st.number_input("Quantas mercadorias você deseja adicionar?", min_value=1, max_value=20, value=5)

# Campos de entrada para cada mercadoria
for i in range(num_itens):
    nome = st.text_input(f"Nome da Mercadoria {i+1}")
    peso = st.number_input(f"Peso da Mercadoria {i+1} (kg)", min_value=1, value=10)
    volume = st.number_input(f"Volume da Mercadoria {i+1} (m³)", min_value=1, value=1)

    # Adiciona o item à lista
    if nome:
        itens.append({"nome": nome, "peso": peso, "volume": volume})

# Botão para executar a otimização
if st.button("Alocar Carga"):
    if len(itens) == 0:
        st.warning("Adicione pelo menos uma mercadoria para otimizar o carregamento.")
    else:
        # Chamada à função de otimização
        carga, peso_usado, volume_usado = alocar_carga(capacidade_peso, capacidade_volume, itens)
        
        # Exibir o resultado
        st.write(f"Total de peso alocado: {peso_usado} kg")
        st.write(f"Total de volume alocado: {volume_usado} m³")
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
        
        # Gráfico de volume
        ax[1].bar(mercadorias, volumes, color='green')
        ax[1].set_title('Distribuição de Volume das Mercadorias')
        ax[1].set_xlabel('Mercadorias')
        ax[1].set_ylabel('Volume (m³)')

        st.pyplot(fig)
