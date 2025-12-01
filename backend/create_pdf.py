from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

contenu = """
Titre : Guide d’utilisation de AskMyDoc

Objectifs principaux :
1. Démontrer l’intégration de LangChain avec Flask.
2. Créer un pipeline RAG pour des documents PDF.
3. Permettre à l’utilisateur de poser des questions et d’obtenir des réponses précises.

Introduction :
AskMyDoc est une application RAG qui utilise LangChain pour transformer n’importe quel document PDF en base de connaissances consultable. 
Le système utilise des embeddings vectoriels pour retrouver les informations pertinentes et un LLM pour générer des réponses.

Fonctionnalités :
- Upload de PDF
- Découpage en chunks
- Création d’embeddings
- Recherche contextuelle
- Réponse générée par un LLM
"""

# Remplacer les caractères spéciaux ou utiliser fpdf2 UTF-8
contenu = contenu.replace("’", "'").replace("à", "a").replace("é", "e")

pdf.multi_cell(0, 10, txt=contenu)
pdf.output("document_exemple.pdf")
print("PDF créé : document_exemple.pdf")
