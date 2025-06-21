"""
Modelo de Lead Scoring
Script para aplicar scoring em novos leads
"""

import pandas as pd
import joblib

class LeadScorer:
    def __init__(self):
        self.model = None
        
    def calculate_business_score(self, lead):
        """Calcula score baseado em regras de negócio"""
        score = 0
        
        # Fonte (peso alto)
        source_scores = {
            'Welingak Website': 40, 'Reference': 35, 'Google': 20,
            'Organic Search': 15, 'Direct Traffic': 10, 'Olark Chat': 5
        }
        score += source_scores.get(lead.get('Lead Source', ''), 0)
        
        # Tempo no site
        time_spent = lead.get('Total Time Spent on Website', 0) or 0
        if time_spent > 1000: score += 20
        elif time_spent > 500: score += 15
        elif time_spent > 200: score += 10
        elif time_spent > 0: score += 5
        
        # Última atividade
        activity_scores = {
            'Had a Phone Conversation': 25, 'SMS Sent': 20,
            'Email Opened': 10, 'Email Link Clicked': 5
        }
        score += activity_scores.get(lead.get('Last Activity', ''), 0)
        
        # Visitas
        visits = lead.get('TotalVisits', 0) or 0
        if visits > 5: score += 10
        elif visits > 2: score += 5
        
        # Qualidade
        quality_scores = {'High': 15, 'Medium': 10, 'Low': 5}
        score += quality_scores.get(lead.get('Lead Quality', ''), 0)
        
        return min(score, 100)
    
    def get_priority(self, score):
        """Define prioridade baseada no score"""
        if score >= 70: return 'ALTA'
        elif score >= 50: return 'MÉDIA'
        elif score >= 30: return 'BAIXA'
        else: return 'MUITO BAIXA'
    
    def score_leads(self, leads_df):
        """Aplica scoring em um DataFrame de leads"""
        leads_df['Lead_Score'] = leads_df.apply(self.calculate_business_score, axis=1)
        leads_df['Prioridade'] = leads_df['Lead_Score'].apply(self.get_priority)
        return leads_df

# Exemplo de uso
if __name__ == "__main__":
    scorer = LeadScorer()
    
    # Exemplo de lead
    new_lead = {
        'Lead Source': 'Google',
        'Total Time Spent on Website': 600,
        'Last Activity': 'Email Opened',
        'TotalVisits': 3,
        'Lead Quality': 'Medium'
    }
    
    score = scorer.calculate_business_score(new_lead)
    priority = scorer.get_priority(score)
    
    print(f"Lead Score: {score}/100")
    print(f"Prioridade: {priority}")
