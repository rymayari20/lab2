import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import matplotlib.pyplot as plt

def main():
    url = "https://news.ycombinator.com/item?id=42919502"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Trouver les commentaires de niveau 0
    elements = soup.find_all(class_="ind", indent=0)
    comments = [e.find_next(class_="comment") for e in elements if e.find_next(class_="comment")]
    
    # Dictionnaire des technologies avec compteur
    keywords = {
        "python": 0, "javascript": 0, "typescript": 0, 
        "go": 0, "golang": 0, "c#": 0, "java": 0, 
        "rust": 0, "react": 0, "aws": 0, "docker": 0,
        "kubernetes": 0, "node": 0, "postgres": 0,
        "mongodb": 0, "sql": 0, "flask": 0, "django": 0
    }

    # Caractères spéciaux à supprimer
    chars_to_strip = ".,/:;!@()[]{}<>\"'\\|-_+=*&^%$#`~"
    
    # Dictionnaire pour les mots uniques trouvés
    unique_words = defaultdict(int)
    
    for comment in comments:
        comment_text = comment.get_text().lower()
        # Utilisation d'un set pour les mots uniques
        words = {w.strip(chars_to_strip) for w in comment_text.split()}
        
        # Mise à jour des mots uniques
        for word in words:
            unique_words[word] += 1
        
        # Version optimisée du comptage des technologies
        for tech in keywords:
            if tech in words:
                keywords[tech] += 1

    # Affichage brut du dictionnaire keywords
    print("\nDictionnaire complet des technologies:")
    print(keywords)

    # Affichage formaté des résultats
    print("\nTechnologies recherchées dans les offres :")
    print("-" * 50)
    for tech, count in sorted(keywords.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"{tech.upper():<15}: {count} occurrences")
    
    # Optionnel : afficher les mots uniques intéressants
    print("\nMots clés uniques trouvés :")
    print("-" * 50)
    for word, count in sorted(unique_words.items(), key=lambda x: x[1], reverse=True)[:20]:
        if len(word) > 3 and count > 1:
            print(f"{word:<20}: {count} posts")

    # Création du graphique
    plt.figure(figsize=(12, 6))
    
    # Filtrer les technologies avec au moins une occurrence
    filtered_data = {k: v for k, v in keywords.items() if v > 0}
    
    # Trier par nombre d'occurrences (décroissant)
    sorted_tech = sorted(filtered_data.items(), key=lambda x: x[1], reverse=True)
    tech_names = [x[0].upper() for x in sorted_tech]
    tech_counts = [x[1] for x in sorted_tech]
    
    # Création du bar plot
    bars = plt.bar(tech_names, tech_counts, color='skyblue')
    
    # Ajout des valeurs sur chaque barre
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(height)}',
                ha='center', va='bottom')
    
    # Personnalisation du graphique
    plt.xlabel("Technologies", fontsize=12)
    plt.ylabel("Nombre de mentions", fontsize=12)
    plt.title("Technologies les plus demandées sur Hacker News", fontsize=14)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Affichage du graphique
    plt.show()

if __name__ == "__main__":
    main()