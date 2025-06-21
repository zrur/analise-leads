"""
Funções utilitárias para análise de leads
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_conversion_charts(df):
    """Cria gráficos de conversão"""
    plt.style.use('seaborn-v0_8')
    fig, axes = plt.subplots(2, 2, figsize=(15, 12))
    
    # 1. Conversão por fonte
    source_conv = df.groupby('Lead Source')['Converted'].agg(['count', 'mean']).reset_index()
    source_conv = source_conv[source_conv['count'] >= 50].sort_values('mean', ascending=False)
    
    axes[0,0].bar(range(len(source_conv)), source_conv['mean'])
    axes[0,0].set_title('Taxa de Conversão por Fonte')
    axes[0,0].set_xticks(range(len(source_conv)))
    axes[0,0].set_xticklabels(source_conv['Lead Source'], rotation=45)
    axes[0,0].set_ylabel('Taxa de Conversão')
    
    # 2. Distribuição de tempo no site
    axes[0,1].hist(df[df['Converted']==1]['Total Time Spent on Website'], 
                   alpha=0.7, label='Convertidos', bins=30)
    axes[0,1].hist(df[df['Converted']==0]['Total Time Spent on Website'], 
                   alpha=0.7, label='Não Convertidos', bins=30)
    axes[0,1].set_title('Distribuição: Tempo no Site')
    axes[0,1].set_xlabel('Tempo (segundos)')
    axes[0,1].legend()
    
    # 3. Score distribution
    axes[1,0].hist(df['Lead_Score'], bins=20, edgecolor='black')
    axes[1,0].set_title('Distribuição dos Lead Scores')
    axes[1,0].set_xlabel('Lead Score')
    axes[1,0].set_ylabel('Frequência')
    
    # 4. Conversão por prioridade
    priority_conv = df.groupby('Prioridade')['Converted'].mean().sort_values(ascending=False)
    axes[1,1].bar(priority_conv.index, priority_conv.values)
    axes[1,1].set_title('Taxa de Conversão por Prioridade')
    axes[1,1].set_ylabel('Taxa de Conversão')
    
    plt.tight_layout()
    plt.savefig('images/visualizations/conversion_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def generate_lead_report(df, lead_id):
    """Gera relatório detalhado de um lead específico"""
    lead = df[df['Lead Number'] == lead_id].iloc[0]
    
    report = f"""
    📋 RELATÓRIO DO LEAD #{lead_id}
    {'='*40}
    
    🎯 Score: {lead['Lead_Score']}/100
    📊 Prioridade: {lead['Prioridade']}
    
    📍 Informações Básicas:
    • Fonte: {lead['Lead Source']}
    • Origem: {lead.get('Lead Origin', 'N/A')}
    • País: {lead.get('Country', 'N/A')}
    
    🖱️ Comportamento no Site:
    • Tempo total: {lead.get('Total Time Spent on Website', 0)}s
    • Visitas: {lead.get('TotalVisits', 0)}
    • Páginas por visita: {lead.get('Page Views Per Visit', 0)}
    
    📧 Última Atividade: {lead.get('Last Activity', 'N/A')}
    
    💼 Perfil:
    • Ocupação: {lead.get('What is your current occupation', 'N/A')}
    • Especialização: {lead.get('Specialization', 'N/A')}
    
    📞 Contato:
    • Email permitido: {lead.get('Do Not Email', 'N/A')}
    • Ligação permitida: {lead.get('Do Not Call', 'N/A')}
    
    🎯 RECOMENDAÇÃO DE AÇÃO:
    """
    
    if lead['Lead_Score'] >= 70:
        report += "🔥 CONTATO IMEDIATO - Ligar hoje!"
    elif lead['Lead_Score'] >= 50:
        report += "📧 Enviar conteúdo relevante e agendar follow-up"
    elif lead['Lead_Score'] >= 30:
        report += "📬 Incluir em campanha de email marketing"
    else:
        report += "🔄 Requalificar ou mover para nurturing"
    
    return report
