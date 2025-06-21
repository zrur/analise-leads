import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

print('📊 Gerando visualizações...')

# Carregar dados
df = pd.read_csv('data/Lead_Scoring.csv')

# Configurar estilo
plt.style.use('default')
sns.set_palette('husl')

# 1. GRÁFICO: Conversão por Fonte
plt.figure(figsize=(12, 6))
source_conv = df.groupby('Lead Source')['Converted'].agg(['count', 'mean']).reset_index()
source_conv = source_conv[source_conv['count'] >= 50].sort_values('mean', ascending=False)

bars = plt.bar(range(len(source_conv)), source_conv['mean'], color='skyblue', edgecolor='navy', alpha=0.7)
plt.title('📈 Taxa de Conversão por Fonte de Lead', fontsize=16, fontweight='bold', pad=20)
plt.xticks(range(len(source_conv)), source_conv['Lead Source'], rotation=45, ha='right')
plt.ylabel('Taxa de Conversão', fontsize=12)
plt.ylim(0, 1)

# Adicionar valores nas barras
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 0.01, 
             f'{height:.1%}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('images/visualizations/conversao_por_fonte.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Gráfico 1 salvo: conversao_por_fonte.png')

# 2. GRÁFICO: Distribuição de Tempo no Site
plt.figure(figsize=(12, 6))
converted = df[df['Converted']==1]['Total Time Spent on Website'].dropna()
not_converted = df[df['Converted']==0]['Total Time Spent on Website'].dropna()

plt.hist(not_converted, bins=50, alpha=0.7, label='Não Convertidos', color='lightcoral', density=True)
plt.hist(converted, bins=50, alpha=0.7, label='Convertidos', color='lightgreen', density=True)

plt.title('⏱️ Distribuição: Tempo Gasto no Site', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Tempo no Site (segundos)', fontsize=12)
plt.ylabel('Densidade', fontsize=12)
plt.legend(fontsize=12)
plt.grid(True, alpha=0.3)

# Adicionar médias
conv_mean = converted.mean()
not_conv_mean = not_converted.mean()
plt.axvline(conv_mean, color='green', linestyle='--', alpha=0.8, label=f'Média Convertidos: {conv_mean:.0f}s')
plt.axvline(not_conv_mean, color='red', linestyle='--', alpha=0.8, label=f'Média Não Convertidos: {not_conv_mean:.0f}s')
plt.legend()

plt.tight_layout()
plt.savefig('images/visualizations/tempo_no_site.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Gráfico 2 salvo: tempo_no_site.png')

# 3. GRÁFICO: Lead Score Distribution
# Aplicar scoring primeiro
def calculate_lead_score(row):
    score = 0
    source_scores = {'Welingak Website': 40, 'Reference': 35, 'Google': 20, 'Organic Search': 15, 'Direct Traffic': 10, 'Olark Chat': 5}
    score += source_scores.get(row.get('Lead Source', ''), 0)
    
    time_spent = row.get('Total Time Spent on Website', 0) or 0
    if time_spent > 1000: score += 20
    elif time_spent > 500: score += 15
    elif time_spent > 200: score += 10
    elif time_spent > 0: score += 5
    
    return min(score, 100)

df['Lead_Score'] = df.apply(calculate_lead_score, axis=1)

plt.figure(figsize=(12, 6))
plt.hist(df['Lead_Score'], bins=20, edgecolor='black', alpha=0.7, color='lightblue')
plt.title('🎯 Distribuição dos Lead Scores', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Lead Score (0-100)', fontsize=12)
plt.ylabel('Número de Leads', fontsize=12)
plt.grid(True, alpha=0.3)

# Adicionar linhas de corte
plt.axvline(70, color='red', linestyle='--', alpha=0.8, label='Alta Prioridade (70+)')
plt.axvline(50, color='orange', linestyle='--', alpha=0.8, label='Média Prioridade (50+)')
plt.axvline(30, color='yellow', linestyle='--', alpha=0.8, label='Baixa Prioridade (30+)')
plt.legend()

# Estatísticas
mean_score = df['Lead_Score'].mean()
plt.text(0.7, 0.8, f'Score Médio: {mean_score:.1f}', transform=plt.gca().transAxes, 
         bbox=dict(boxstyle='round', facecolor='white', alpha=0.8), fontsize=12)

plt.tight_layout()
plt.savefig('images/visualizations/lead_score_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Gráfico 3 salvo: lead_score_distribution.png')

# 4. GRÁFICO: Matriz de Correlação (variáveis numéricas)
plt.figure(figsize=(10, 8))
numeric_cols = ['TotalVisits', 'Total Time Spent on Website', 'Page Views Per Visit', 'Converted', 'Lead_Score']
correlation_matrix = df[numeric_cols].corr()

sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, 
            square=True, cbar_kws={'shrink': 0.8})
plt.title('🔥 Matriz de Correlação - Variáveis Numéricas', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('images/visualizations/matriz_correlacao.png', dpi=300, bbox_inches='tight')
plt.close()
print('✅ Gráfico 4 salvo: matriz_correlacao.png')

print('\\n🎉 TODAS AS VISUALIZAÇÕES FORAM CRIADAS!')
print('📁 Localização: images/visualizations/')
print('🔄 Pronto para o próximo passo!')
