#!/bin/bash

echo "🚀 Configurando ambiente Lead Scoring Analysis..."

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install --upgrade pip
pip install -r requirements.txt

# Copiar dados (ajuste o caminho conforme necessário)
echo "📁 Copie seus arquivos de dados para a pasta data/:"
echo "  • Lead_Scoring.csv -> data/"
echo "  • Leads Data Dictionary.xlsx -> data/"

echo "✅ Setup concluído!"
echo "Para ativar o ambiente: source venv/bin/activate"
echo "Para executar análise: python src/lead_scoring_analysis.py"
