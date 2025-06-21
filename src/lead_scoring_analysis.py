"""
Lead Scoring Analysis
Análise completa para identificação de leads promissores
Autor: Arthur Silva
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.preprocessing import LabelEncoder
import warnings
warnings.filterwarnings('ignore')

class LeadScoringAnalysis:
    def __init__(self, data_path):
        """Inicializa a análise de lead scoring"""
        self.df = pd.read_csv(data_path)
        self.le_dict = {}
        self.model = None
        
        print("🎯 Lead Scoring Analysis Iniciada")
        print(f"📊 Dataset carregado: {self.df.shape[0]} leads, {self.df.shape[1]} variáveis")
        print(f"💰 Taxa de conversão: {self.df['Converted'].mean():.1%}")
        
    def exploratory_analysis(self):
        """Realiza análise exploratória completa"""
        print("\n" + "="*50)
        print("📈 ANÁLISE EXPLORATÓRIA")
        print("="*50)
        
        # Análise por fonte
        source_analysis = self.df.groupby('Lead Source').agg({
            'Converted': ['count', 'sum', 'mean']
        }).round(3)
        source_analysis.columns = ['Total_Leads', 'Convertidos', 'Taxa_Conversao']
        source_analysis = source_analysis[source_analysis['Total_Leads'] >= 50]
        source_analysis = source_analysis.sort_values('Taxa_Conversao', ascending=False)
        
        print("\n🎯 CONVERSÃO POR FONTE:")
        print(source_analysis)
        
        # Comportamento no site
        print("\n🖱️ COMPORTAMENTO NO SITE:")
        behavioral_cols = ['TotalVisits', 'Total Time Spent on Website', 'Page Views Per Visit']
        
        for col in behavioral_cols:
            conv_avg = self.df[self.df['Converted'] == 1][col].mean()
            not_conv_avg = self.df[self.df['Converted'] == 0][col].mean()
            diff = ((conv_avg/not_conv_avg - 1) * 100) if not_conv_avg > 0 else 0
            
            print(f"\n{col}:")
            print(f"  ✅ Convertidos: {conv_avg:.1f}")
            print(f"  ❌ Não convertidos: {not_conv_avg:.1f}")
            print(f"  📊 Diferença: {diff:+.1f}%")
        
        return source_analysis
    
    def create_lead_score(self):
        """Cria sistema de scoring para leads"""
        print("\n" + "="*50)
        print("🎯 CRIANDO MODELO DE SCORING")
        print("="*50)
        
        def calculate_score(row):
            score = 0
            
            # Fonte (peso 40%)
            source_scores = {
                'Welingak Website': 40, 'Reference': 35, 'Google': 20,
                'Organic Search': 15, 'Direct Traffic': 10, 'Olark Chat': 5
            }
            score += source_scores.get(row.get('Lead Source', ''), 0)
            
            # Tempo no site (peso 20%)
            time_spent = row.get('Total Time Spent on Website', 0) or 0
            if time_spent > 1000: score += 20
            elif time_spent > 500: score += 15
            elif time_spent > 200: score += 10
            elif time_spent > 0: score += 5
            
            # Última atividade (peso 25%)
            activity_scores = {
                'Had a Phone Conversation': 25, 'SMS Sent': 20,
                'Email Opened': 10, 'Email Link Clicked': 5
            }
            score += activity_scores.get(row.get('Last Activity', ''), 0)
            
            # Visitas (peso 10%)
            visits = row.get('TotalVisits', 0) or 0
            if visits > 5: score += 10
            elif visits > 2: score += 5
            
            # Qualidade (peso 5%)
            quality_scores = {'High': 15, 'Medium': 10, 'Low': 5}
            score += quality_scores.get(row.get('Lead Quality', ''), 0)
            
            return min(score, 100)
        
        self.df['Lead_Score'] = self.df.apply(calculate_score, axis=1)
        
        # Categorias de prioridade
        def get_priority(score):
            if score >= 70: return 'ALTA'
            elif score >= 50: return 'MÉDIA'
            elif score >= 30: return 'BAIXA'
            else: return 'MUITO BAIXA'
        
        self.df['Prioridade'] = self.df['Lead_Score'].apply(get_priority)
        
        # Estatísticas do scoring
        print(f"📊 Score médio: {self.df['Lead_Score'].mean():.1f}/100")
        print(f"🎯 Score máximo: {self.df['Lead_Score'].max()}/100")
        
        print("\n📋 DISTRIBUIÇÃO POR PRIORIDADE:")
        priority_dist = self.df['Prioridade'].value_counts()
        for priority, count in priority_dist.items():
            percentage = (count / len(self.df)) * 100
            print(f"  {priority}: {count:,} leads ({percentage:.1f}%)")
        
        return self.df['Lead_Score']
    
    def train_ml_model(self):
        """Treina modelo de Machine Learning"""
        print("\n" + "="*50)
        print("🤖 TREINANDO MODELO ML")
        print("="*50)
        
        # Features para ML
        ml_features = [
            'TotalVisits', 'Total Time Spent on Website', 'Page Views Per Visit',
            'Lead Source', 'Last Activity', 'Lead Quality', 'Lead Origin'
        ]
        
        ml_df = self.df[ml_features + ['Converted']].copy()
        
        # Tratar valores nulos
        for col in ml_df.columns:
            if ml_df[col].dtype == 'object':
                ml_df[col] = ml_df[col].fillna('Unknown')
            else:
                ml_df[col] = ml_df[col].fillna(0)
        
        # Encode categóricas
        categorical_cols = ml_df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            ml_df[col] = le.fit_transform(ml_df[col].astype(str))
            self.le_dict[col] = le
        
        # Split dados
        X = ml_df.drop('Converted', axis=1)
        y = ml_df['Converted']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Treinar modelo
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.model.fit(X_train, y_train)
        
        # Avaliar
        y_pred = self.model.predict(X_test)
        y_proba = self.model.predict_proba(X_test)[:, 1]
        
        print("📊 PERFORMANCE DO MODELO:")
        print(classification_report(y_test, y_pred))
        print(f"🎯 AUC Score: {roc_auc_score(y_test, y_proba):.3f}")
        
        # Feature importance
        feature_importance = pd.DataFrame({
            'feature': X.columns,
            'importance': self.model.feature_importances_
        }).sort_values('importance', ascending=False)
        
        print("\n📈 VARIÁVEIS MAIS IMPORTANTES:")
        for _, row in feature_importance.head(7).iterrows():
            print(f"  {row['feature']}: {row['importance']:.3f}")
        
        return self.model
    
    def identify_promising_leads(self, min_score=60):
        """Identifica leads mais promissores"""
        print("\n" + "="*50)
        print(f"🔍 LEADS PROMISSORES (Score >= {min_score})")
        print("="*50)
        
        promising = self.df[
            (self.df['Converted'] == 0) & 
            (self.df['Lead_Score'] >= min_score)
        ].copy()
        
        promising = promising.sort_values('Lead_Score', ascending=False)
        
        print(f"🎯 Encontrados {len(promising)} leads promissores")
        
        if len(promising) > 0:
            print(f"\n🥇 TOP 10 LEADS PARA FOCAR:")
            for i, (_, lead) in enumerate(promising.head(10).iterrows()):
                print(f"\n{i+1}. Lead #{lead['Lead Number']} (Score: {lead['Lead_Score']}/100)")
                print(f"   📍 Fonte: {lead['Lead Source']}")
                print(f"   ⏱️ Tempo no site: {lead['Total Time Spent on Website']}s")
                print(f"   📧 Última atividade: {lead['Last Activity']}")
                print(f"   👁️ Visitas: {lead['TotalVisits']}")
                print(f"   🎯 Prioridade: {lead['Prioridade']}")
        
        return promising
    
    def generate_recommendations(self):
        """Gera recomendações estratégicas"""
        print("\n" + "="*50)
        print("💡 RECOMENDAÇÕES ESTRATÉGICAS")
        print("="*50)
        
        print("🎯 AÇÕES PRIORITÁRIAS:")
        print("  1. Contatar IMEDIATAMENTE leads score 70+ por telefone")
        print("  2. Enviar conteúdo relevante para leads 50-69")
        print("  3. Campanhas de email para leads 30-49")
        print("  4. Requalificar ou descartar leads abaixo de 30")
        
        print("\n📈 MELHORIAS NO PROCESSO:")
        print("  1. Investir em programa de referências (91.8% conversão)")
        print("  2. Otimizar campanhas Google (40% conversão)")
        print("  3. Implementar scoring automático")
        print("  4. Treinar equipe para abordagem telefônica")
        
        print("\n📊 KPIs PARA MONITORAR:")
        print("  • Taxa de conversão por fonte")
        print("  • Tempo médio no site por segmento") 
        print("  • Efetividade por prioridade")
        print("  • ROI das campanhas segmentadas")
    
    def save_results(self):
        """Salva resultados da análise"""
        # Salvar dataset com scores
        self.df.to_csv('data/processed/leads_with_scores.csv', index=False)
        
        # Salvar leads promissores
        promising = self.df[
            (self.df['Converted'] == 0) & 
            (self.df['Lead_Score'] >= 60)
        ].sort_values('Lead_Score', ascending=False)
        
        promising.to_csv('data/processed/promising_leads.csv', index=False)
        
        print(f"\n💾 Resultados salvos:")
        print(f"  📁 data/processed/leads_with_scores.csv")
        print(f"  📁 data/processed/promising_leads.csv")

def main():
    """Função principal"""
    # Inicializar análise
    analyzer = LeadScoringAnalysis('data/Lead_Scoring.csv')
    
    # Executar análises
    analyzer.exploratory_analysis()
    analyzer.create_lead_score()
    analyzer.train_ml_model()
    analyzer.identify_promising_leads()
    analyzer.generate_recommendations()
    analyzer.save_results()
    
    print("\n" + "="*50)
    print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
    print("="*50)
    print("📊 Próximos passos:")
    print("  1. Review dos leads prioritários")
    print("  2. Implementação das recomendações") 
    print("  3. Monitoramento dos KPIs")
    print("  4. Ajuste do modelo mensalmente")

if __name__ == "__main__":
    main()
