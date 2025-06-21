# 📖 Como Usar o Projeto Lead Scoring

## 🚀 Início Rápido

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/lead-scoring-analysis
cd lead-scoring-analysis
```

### 2. Configure o ambiente
```bash
bash setup.sh
source venv/bin/activate
```

### 3. Adicione seus dados
Copie o arquivo `Lead_Scoring.csv` para a pasta `data/`

### 4. Execute a análise
```bash
python src/lead_scoring_analysis.py
```

## 📊 Outputs Esperados

### Console
- Análise exploratória completa
- Estatísticas de conversão
- Top leads para focar
- Recomendações estratégicas

### Arquivos Gerados
- `data/processed/leads_with_scores.csv` - Dataset com scores
- `data/processed/promising_leads.csv` - Top leads priorizados
- `images/visualizations/` - Gráficos gerados

## 🎯 Como Interpretar os Resultados

### Lead Score (0-100)
- **70-100**: Alta prioridade - Contato imediato
- **50-69**: Média prioridade - Nutrição ativa
- **30-49**: Baixa prioridade - Email marketing
- **0-29**: Muito baixa - Requalificar

### Próximos Passos
1. Review dos leads de alta prioridade
2. Implementação das recomendações
3. Monitoramento dos resultados
4. Ajustes mensais no modelo
