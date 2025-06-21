# 🎯 Lead Scoring Analysis

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Complete-success.svg)]()

## 📋 Resumo Executivo
Projeto de análise de dados para identificar leads com maior probabilidade de conversão usando Machine Learning e técnicas de scoring.

### 🎯 Principais Resultados
- **Taxa de conversão**: 38.5%
- **Melhor fonte**: Referências (91.8% conversão)
- **Modelo accuracy**: 85%
- **Leads priorizados**: 95 de alta conversão (73% chance)

## 🔍 Metodologia

### 1. Análise Exploratória
- Análise de 9.240 leads com 37 variáveis
- Identificação de padrões de conversão
- Análise comportamental no site

### 2. Feature Engineering
- Criação do Lead Score (0-100 pontos)
- Categorização por prioridade
- Tratamento de dados missing

### 3. Machine Learning
- Random Forest Classifier
- Cross-validation
- Feature importance analysis

## 📊 Principais Insights

| Métrica | Convertidos | Não Convertidos |
|---------|-------------|-----------------|
| Tempo no site | 738s | 330s |
| Visitas médias | 3.6 | 3.3 |
| Taxa conversão telefone | 73% | - |

### 🎯 Segmentação de Leads
- **Alta prioridade** (70-100): 1.0% - Contato imediato
- **Média prioridade** (50-69): 30.2% - Nutrição ativa  
- **Baixa prioridade** (30-49): 39.5% - Email marketing
- **Muito baixa** (0-29): 29.3% - Requalificar

## 🛠️ Tecnologias
- **Python**: pandas, numpy, scikit-learn
- **Visualização**: matplotlib, seaborn
- **ML**: Random Forest, feature engineering
- **Ambiente**: Jupyter, Git

## 🚀 Como Usar

### Instalação
```bash
git clone https://github.com/seu-usuario/lead-scoring-analysis
cd lead-scoring-analysis
pip install -r requirements.txt
```

### Execução
```bash
# Análise completa
python src/lead_scoring_analysis.py

# Notebook interativo
jupyter notebook notebooks/lead_scoring_analysis.ipynb

# Apenas scoring
python src/scoring_model.py
```

## 📈 Resultados do Modelo
- **Accuracy**: 85%
- **Precision**: 82%
- **Recall**: 88%
- **F1-Score**: 85%

## 💡 Recomendações
1. **Focar em referências** - ROI 91.8%
2. **Implementar scoring automático**
3. **Priorizar contato telefônico** para score 70+
4. **Segmentar campanhas** por prioridade

## 📁 Estrutura do Projeto
```
lead-scoring-analysis/
├── data/
│   ├── Lead_Scoring.csv
│   └── processed/
├── notebooks/
│   └── lead_scoring_analysis.ipynb
├── src/
│   ├── lead_scoring_analysis.py
│   ├── scoring_model.py
│   └── utils.py
├── images/visualizations/
├── docs/relatorio_detalhado.md
├── requirements.txt
└── README.md
```

## 👨‍💻 Autor
**Arthur Ramos Dos Santos** 
 🔗 [LinkedIn](https://www.linkedin.com/in/arthur-ramos-dos-santos-689a30230/)) | 🐙 [GitHub](https://github.com/arthur)

## 📄 Licença
Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---
⭐ Se este projeto foi útil, considere dar uma estrela!
