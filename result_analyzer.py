import pandas as pd

# Funció per analitzar els resultats de la campanya
def analyze_results(results):
    # Convertir els resultats a DataFrame per facilitar l'anàlisi
    df = pd.DataFrame(results)
    # Anàlisi bàsica: comptar els clics i submissions
    clicks = df[df['clicked'] == True].shape[0]
    submissions = df[df['submitted'] == True].shape[0]
    print(f'Número de clics: {clicks}')
    print(f'Número de submissions: {submissions}')

# Exemple de resultats de campanya
results = [
    {'email': 'juan.perez@example.com', 'clicked': True, 'submitted': False},
    {'email': 'maria.garcia@example.com', 'clicked': False, 'submitted': False},
    {'email': 'luis.martinez@example.com', 'clicked': True, 'submitted': True},
]

analyze_results(results)
