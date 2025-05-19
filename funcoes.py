import yfinance as y
import pandas as pd
import datetime
import numpy as np
import matplotlib.pyplot as plt
from fpdf import FPDF

def data_inicio(a, m, d):
    return datetime.datetime(a, m, d).date()

def data_fim(a, m, d):
    return datetime.datetime(a, m, d).date()

def historico_ativo(ativos_sigla, data_inicio, data_fim):
    historico = pd.DataFrame()
    for ativo_sigla in ativos_sigla:
        ativo = y.download(ativo_sigla, data_inicio, data_fim, auto_adjust=False)['Adj Close']
        historico[ativo_sigla.upper()] = ativo
    return historico

def risco_anual(dataframe, pesos):
    retorno_diario = dataframe.pct_change(fill_method=None).dropna() * 100
    pesos_array = np.array(pesos)
    risco = (np.dot(pesos_array.T, np.dot(retorno_diario.cov() * 250, pesos))) ** 0.5
    return round(risco, 2)

def risco_individual(df):
    retorno_diario = df.pct_change(fill_method=None).dropna()
    risco_por_ativo = retorno_diario.std() * np.sqrt(250) * 100  # desvio padrão anualizado (%)
    return risco_por_ativo

def correlacao(dataframe):
    return dataframe.corr().round(2)

def graf_evolucao_relativa(dataframe, largura, altura, caminho_imagem="grafico_evolucao.png"):
    plt.figure(figsize=(largura, altura))
    for coluna in dataframe.columns:
        preco_inicial = dataframe[coluna].iloc[0]
        evolucao = (dataframe[coluna] / preco_inicial - 1) * 100
        cor = 'black' if coluna.upper() == '^BVSP' else None
        plt.plot(dataframe.index, evolucao, label=coluna, color=cor)

    plt.title("Evolução do Preço por Ação")
    plt.xlabel("Data")
    plt.ylabel("Variação (%)")
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(caminho_imagem)
    plt.close()
    return caminho_imagem

def gerar_relatorio_pdf(df, df_e_ibov, pesos, capital, data_inicio, data_fim, nome_arquivo="relatorio_carteira.pdf"):
    retorno_simples = df.pct_change(fill_method=None).dropna() * 250 * 100
    medias_individuais = retorno_simples.mean()
    media_geral = medias_individuais.mean()
    risco = risco_anual(df, pesos)
    risco_indiv = risco_individual(df)
    matriz_corr = correlacao(df)
    caminho_imagem = graf_evolucao_relativa(df_e_ibov, 12, 6)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Relatório de Desempenho de Ativos", ln=True)

    pdf.ln(3)

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 7, "Ativos utilizados:", ln=True)
    pdf.set_font("Arial", "", 7)
    pdf.multi_cell(0, 7, ", ".join(df.columns))

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 7, "Pesos utilizados:", ln=True)
    pdf.set_font("Arial", "", 7)
    pdf.multi_cell(0, 7, ", ".join([f"{peso:.2f}" for peso in pesos]))

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 7, "Período analisado:", ln=True)
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 7, f"Início: {data_inicio}  |  Fim: {data_fim}", ln=True)

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 7, "Capital investido:", ln=True)
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 7, f"R$ {capital:,.2f}", ln=True)

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 7, f"Risco anual da carteira:", ln=True)
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 7, f"{risco} %", ln=True)

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 7, f"Média geral dos retornos anualizados:", ln=True)
    pdf.set_font("Arial", "", 7)
    pdf.cell(0, 7, f"{media_geral:.2f} %", ln=True)

    pdf.ln(3)

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 7, "Resumo da Alocação, Retorno e Risco por Ativo:", ln=True)
    pdf.ln(1)

    pdf.set_fill_color(220, 220, 220)
    pdf.cell(30, 6, "Ativo", 1, fill=True)
    pdf.cell(30, 6, "Alocação (%)", 1, fill=True)
    pdf.cell(45, 6, "Valor Inicial -> Final", 1, fill=True)
    pdf.cell(30, 6, "Retorno Anual (%)", 1, fill=True)
    pdf.cell(25, 6, "Risco (%)", 1, fill=True)
    pdf.ln()

    pdf.set_font("Arial", "", 7)

    total_aloc_inicial = 0
    total_aloc_final = 0
    total_valor_pos_inicial = 0
    total_valor_pos_final = 0

    for i, ativo in enumerate(df.columns):
        preco_inicio = df[ativo].iloc[0]
        preco_fim = df[ativo].iloc[-1]
        aloc_inicial = pesos[i]
        aloc_final = (preco_fim / preco_inicio) * pesos[i]
        valor_pos_inicial = capital * aloc_inicial
        valor_pos_final = capital * aloc_final
        retorno_ativo = medias_individuais[ativo]
        risco_ativo = risco_indiv[ativo]

        total_aloc_inicial += aloc_inicial
        total_aloc_final += aloc_final
        total_valor_pos_inicial += valor_pos_inicial
        total_valor_pos_final += valor_pos_final

        pdf.cell(30, 6, ativo, 1)
        pdf.cell(30, 6, f"{aloc_inicial:.2%} -> {aloc_final:.2%}", 1)
        pdf.cell(45, 6, f"R$ {valor_pos_inicial:,.2f} -> R$ {valor_pos_final:,.2f}", 1)
        pdf.cell(30, 6, f"{retorno_ativo:.2f}%", 1)
        pdf.cell(25, 6, f"{risco_ativo:.2f}%", 1)
        pdf.ln()

    # Totais e médias
    media_retorno = np.average(medias_individuais, weights=pesos)
    media_risco = np.average(risco_indiv, weights=pesos)

    pdf.set_font("Arial", "B", 7)
    pdf.cell(30, 6, "TOTAL / MÉDIA", 1)
    pdf.cell(30, 6, f"{total_aloc_inicial:.2%} -> {total_aloc_final:.2%}", 1)
    pdf.cell(45, 6, f"R$ {total_valor_pos_inicial:,.2f} -> R$ {total_valor_pos_final:,.2f}", 1)
    pdf.cell(30, 6, f"{media_retorno:.2f}%", 1)
    pdf.cell(25, 6, f"{media_risco:.2f}%", 1)
    pdf.ln()

    pdf.ln(3)

    pdf.set_font("Arial", "B", 7)
    pdf.cell(0, 5, "Matriz de Correlação:", ln=True)
    pdf.set_font("Arial", "", 6)

    ativos = matriz_corr.columns.tolist()
    cell_w = 15
    cell_h = 6

    pdf.set_fill_color(220, 220, 220)
    pdf.cell(cell_w, cell_h, "", border=1, fill=True)
    for ativo in ativos:
        pdf.cell(cell_w, cell_h, ativo, border=1, fill=True)
    pdf.ln()

    for ativo_linha in ativos:
        pdf.set_fill_color(220, 220, 220)
        pdf.cell(cell_w, cell_h, ativo_linha, border=1, fill=True)
        pdf.set_fill_color(255, 255, 255)
        for ativo_coluna in ativos:
            valor = str(matriz_corr.loc[ativo_linha, ativo_coluna])
            pdf.cell(cell_w, cell_h, valor, border=1)
        pdf.ln()

    pdf.ln(5)
    pdf.image(caminho_imagem, w=180)

    pdf.output(nome_arquivo)
    print(f"Relatório PDF gerado com sucesso: {nome_arquivo}")