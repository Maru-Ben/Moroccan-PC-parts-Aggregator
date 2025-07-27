import re

def preprocess(title):
    # Lowercase
    title = title.lower()
    
    # Remove content inside parentheses
    title = re.sub(r'\([^)]*\)', '', title)
    
    # Remove special characters except hyphens and spaces
    title = re.sub(r'[^\w\s-]', ' ', title)
    
    # Normalize whitespace
    title = re.sub(r'\s+', ' ', title).strip()
    
    # Noise and color terms
    noise = ['casablanca','maroc','tray','socket','cartes','prix',
             'box','exclusivite','web','special','edition','mémoire','vive']
    
    colors = ['noir','black','white','blanc','rouge','red', 'yellow', 'green'
              'rose','pink','bleu', 'blue','violet','beige','vert','turquoise',
              'gris','gray','rgb', 'argb']
    
    # Remove noise terms using word boundaries
    for term in noise + colors:
        title = re.sub(rf'\b{re.escape(term)}\b', '', title)
    
    # Final cleanup
    title = re.sub(r'\s+', ' ', title).strip()
    
    return title