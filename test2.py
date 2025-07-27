import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import DBSCAN
import difflib
from collections import defaultdict
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

class ProductClusterer:
    """
    A robust solution for clustering product entries that represent the same item
    despite text variations, across different sources and formats.
    """
    
    def __init__(self, eps=0.1, min_samples=1, n_gram_range=(2, 5)):
        """
        Initialize the product clusterer with more sensitive default parameters.
        
        Args:
            eps: DBSCAN epsilon parameter (similarity threshold)
            min_samples: DBSCAN min_samples parameter
            n_gram_range: Range of n-grams to use for TF-IDF
        """
        self.eps = eps
        self.min_samples = min_samples
        self.n_gram_range = n_gram_range
        self.vectorizer = None
        
    def preprocess(self, products):
        """
        Perform minimal preprocessing on product names.
        
        Args:
            products: List of product names
            
        Returns:
            List of preprocessed product names
        """
        processed = []
        for product in products:
            # Convert to lowercase for case-insensitive comparison
            text = product.lower()
            
            # Standardize whitespace
            text = re.sub(r'\s+', ' ', text)
            text = text.strip()
            
            # Standardize parentheses
            text = re.sub(r'\(([^)]*)\)', r' \1 ', text)
            
            # Remove specific unwanted terms
            unwanted_terms = ['casablanca', 'maroc', 'tray', 'socket', 'cartes', 'prix', 'box', 'mémoire', 'vive', 'exclusivite', 'web', 'special', 'edition']
            for term in unwanted_terms:
                text = text.replace(term, '')
                
            # Remove specific unwanted terms
            colors = ['noir', 'black', 'white', 'blanc', 'argent', 'rouge', 'red', 'rose', 'pink', 'bleu', 'violet', 'beige','vert', 'turquoise', 'gris', 'gray', 'rgb']
            for term in colors:
                text = text.replace(term, '')
                
            # Remove special characters and normalize spaces
            text = re.sub(r'[^\w\s-]', ' ', text)
            text = re.sub(r'\s+', ' ', text)
            
            processed.append(text)
        
        return processed
    
    def create_features(self, products):
        """
        Create TF-IDF features from product names.
        
        Args:
            products: List of preprocessed product names
            
        Returns:
            TF-IDF feature matrix
        """
        # Use character n-grams which are more robust to spelling variations
        self.vectorizer = TfidfVectorizer(
            analyzer='char_wb',  # Character n-grams including word boundaries
            ngram_range=self.n_gram_range,
            min_df=1,  # Allow n-grams that appear in only one document
            sublinear_tf=True,  # Apply sublinear tf scaling (1 + log(tf))
        )
        
        return self.vectorizer.fit_transform(products)
    
    def visualize_similarity_matrix(self, products, filename='similarity_matrix.png'):
        """
        Visualize the similarity matrix as a heatmap.
        
        Args:
            products: List of product names
            filename: Output file name
        """
        preprocessed = self.preprocess(products)
        features = self.create_features(preprocessed)
        
        # Calculate cosine similarity matrix
        similarity_matrix = cosine_similarity(features)
        
        # Plot the similarity matrix
        plt.figure(figsize=(12, 10))
        plt.imshow(similarity_matrix, cmap='viridis')
        plt.colorbar(label='Cosine Similarity')
        plt.title('Product Similarity Matrix')
        plt.savefig(filename)
        plt.close()
        
        return similarity_matrix
    
    def cluster_products(self, products):
        """
        Cluster product names using DBSCAN.
        
        Args:
            products: List of product names
            
        Returns:
            Dictionary mapping cluster IDs to lists of product names
        """
        preprocessed = self.preprocess(products)
        features = self.create_features(preprocessed)
        
        # Use DBSCAN for clustering
        dbscan = DBSCAN(
            eps=self.eps,
            min_samples=self.min_samples,
            metric='cosine',
            n_jobs=-1
        )
        
        labels = dbscan.fit_predict(features)
        
        # Create clustering result
        clusters = defaultdict(list)
        for i, label in enumerate(labels):
            if label != -1:  # Ignore noise points
                clusters[label].append(products[i])
            else:
                # Put each noise point in its own singleton cluster
                singleton_label = f"singleton_{i}"
                clusters[singleton_label] = [products[i]]
        
        return clusters
    
    def identify_product_groups(self, products):
        """
        Complete pipeline to identify groups of identical products with refinement.
        
        Args:
            products: List of product names
            
        Returns:
            List of product groups
        """
        # Initial clustering
        clusters = self.cluster_products(products)
        # Convert to list of lists and filter out singletons
        return [cluster for cluster_id, cluster in clusters.items() 
                if not isinstance(cluster_id, str) or not cluster_id.startswith('singleton')]

    def find_optimal_epsilon(self, products, eps_range=(0.05, 0.25), num_steps=20):
        """
        Find the optimal epsilon value by testing a range of values.
        
        Args:
            products: List of product names
            eps_range: Range of epsilon values to test
            num_steps: Number of steps within the range
            
        Returns:
            Dictionary of results with epsilon values as keys and number of clusters as values
        """
        results = {}
        
        # Generate epsilon values
        eps_values = np.linspace(eps_range[0], eps_range[1], num_steps)
        
        preprocessed = self.preprocess(products)
        features = self.create_features(preprocessed)
        
        for eps in eps_values:
            # Use DBSCAN for clustering
            dbscan = DBSCAN(
                eps=eps,
                min_samples=self.min_samples,
                metric='cosine',
                n_jobs=-1
            )
            
            labels = dbscan.fit_predict(features)
            
            # Count number of unique non-noise clusters
            unique_clusters = len(set([label for label in labels if label != -1]))
            
            results[eps] = unique_clusters
        
        return results


# Sample data from provided examples
product_names = [
    # Group 0: Corsair Nautilus 240
    "corsair nautilus 240 rs argb (noir)",
    "corsair nautilus 240 rs argb blanc",
    "corsair nautilus 240 rs argb noir",

    # Group 1: Corsair Nautilus 360
    "corsair nautilus 360 rs argb (noir)",
    "corsair nautilus 360 rs argb (noir)",
    "corsair nautilus 360 rs argb blanc",
    "corsair nautilus 360 rs argb noir",

    # Group 2: Corsair Vengeance 16GB (1x16)
    "corsair vengeance lpx series low profile 16go (1x 16go) ddr4 3200 mhz cl16",
    "corsair vengeance lpx series low profile 16go (1x 16go) ddr4 3200 mhz cl16 bulk mémoire vive",
    "corsair vengeance lpx series low profile 16go (1x 16go) ddr4 3200 mhz cl16 mémoire vive",

    # Group 3: Corsair Vengeance 16GB (2x8)
    "corsair vengeance lpx series low profile 16go (2x 8go) ddr4 3200 mhz cl16",

    # Group 4: Corsair Vengeance 8GB
    "corsair vengeance lpx series low profile 8go (1x 8go) ddr4 3200 mhz cl16",
    "corsair vengeance lpx series low profile 8go (1x 8go) ddr4 3200 mhz cl16 bulk mémoire vive",

    # Group 5: Crucial P3 4TB
    "crucial p3 4 to (sans emballage)",
    "crucial p3 4 to (sans emballage)",

    # Group 6: Crucial P3 1TB
    "crucial p3 m.2 pcie nvme 1tb",

    # Group 7: RTX 5070 Eagle
    "gigabyte geforce rtx 5070 eagle oc ice sff 12g cartes",

    # Group 8: RTX 5070 Gaming OC
    "gigabyte geforce rtx 5070 gaming oc 12g",
    "gigabyte geforce rtx 5070 gaming oc 12g",

    # Group 9: RTX 5070 Ti Windforce
    "gigabyte geforce rtx 5070 ti windforce oc sff 16g",
    "gigabyte geforce rtx 5070 ti windforce oc sff 16g",
    "gigabyte geforce rtx 5070 ti windforce oc sff 16g cartes",

    # Group 10: RTX 5070 Windforce
    "gigabyte geforce rtx 5070 windforce oc sff 12g",
    "gigabyte geforce rtx 5070 windforce oc sff 12g (exclusivite web)",
    "gigabyte geforce rtx 5070 windforce oc sff 12g cartes",
    "gigabyte geforce rtx 5070 windforce sff 12g",

    # Group 11: RTX 5080 Aero
    "gigabyte geforce rtx 5080 aero oc sff 16g",
    "gigabyte geforce rtx 5080 aero oc sff 16g",
    "gigabyte geforce rtx 5080 aero oc sff 16g",

    # Group 12: RTX 5080 Gaming
    "gigabyte geforce rtx 5080 gaming oc 16g",
    "gigabyte geforce rtx 5080 gaming oc 16g",
    "gigabyte geforce rtx 5080 gaming oc 16g",

    # Group 13: RTX 5080 Windforce
    "gigabyte geforce rtx 5080 windforce oc sff 16g",
    "gigabyte geforce rtx 5080 windforce oc sff 16g",

    # Group 14: P550SS
    "gigabyte p550ss 550w silver",
    "gigabyte p550ss 550w silver",
    "gigabyte p550ss 550w silver",

    # Group 15: P550SS ICE
    "gigabyte p550ss ice 550w silver",
    "gigabyte p550ss ice 550w silver",
    "gigabyte p550ss ice 550w silver",

    # Group 16: P650SS
    "gigabyte p650ss 650w silver",
    "gigabyte p650ss 650w silver",
    "gigabyte p650ss 650w silver",

    # Group 17: Hybrok HG27
    'hybrok hg27xis 27"" ips 240hz 1ms"',

    # Group 18: Hybrok HL240B
    "hybrok hl240b rgb black",
    "hybrok hl240b rgb black maroc prix",

    # Group 19: Hybrok HL240W
    "hybrok hl240w blanc",
    "hybrok hl240w rgb white maroc prix",

    # Group 20: Hybrok HL360B
    "hybrok hl360b noir",

    # Group 21: Intel i9 11900KF
    "intel core i9 11900kf (3.5 ghz / 5.3 ghz) tray",

    # Group 22: Intel i9 14900K
    "intel core i9 14900k (3.2 ghz / 5.8 ghz)",
    "intel core i9 14900k (3.2 ghz / 5.8 ghz)",
    "intel core i9 14900k (3.2 ghz / 5.8 ghz) tray",
    "intel core i9 14900k (3.2 ghz / 5.8 ghz) tray",

    # Group 23: Intel Ultra 5 225F
    "intel core ultra 5 225f (3.3 ghz / 4.9 ghz)",
    "intel core ultra 5 225f (3.3 ghz / 4.9 ghz) box socket",

    # Group 24: Intel Ultra 5 245KF
    "intel core ultra 5 245kf (4.2 ghz / 5.2 ghz) tray",
    "intel core ultra 5 245kf (4.2 ghz / 5.2 ghz) tray socket",

    # Group 25: Intel Ultra 7 265K
    "intel core ultra 7 265k (3.9 ghz / 5.5 ghz)",
    "intel core ultra 7 265k (3.9 ghz / 5.5 ghz) maroc",
    "intel core ultra 7 265k (3.9 ghz / 5.5 ghz) tray",
    
    # Group 26 xtrmlab xp-550b 80+ bronze 550w
    'xtrmlab xp-550b 80+ bronze 550w',
    'xtrmlab xp-550b 80+ bronze 550w ( 2 ans garantie ) entre 500 w et 599',
    
    # Group 27 patriot viper venom 32gb 
    'patriot viper venom 32gb (2x16gb) ddr5 7400mhz',
    'patriot viper venom 32gb (2x16gb) ddr5 7400mhz cl36 - pvv532g740c36k',
    
    # Group 28 rapoo ensemble filaire souris + clavier
    'rapoo ensemble filaire souris + clavier rapoo x130pro',
    'rapoo ensemble filaire souris + clavier rapoo x130pro (azerty français) kits',
]

# Preprocessing placeholder
def preprocess(products):
    processed = []
    for name in products:
        name = name.lower().strip()
        
        # Remove specific unwanted terms
        unwanted_terms = ['casablanca', 'maroc', 'tray', 'socket', 'cartes', 'prix', 'box', 'mémoire', 'vive', 'exclusivite', 'web', 'special', 'edition']
        for term in unwanted_terms:
            name = name.replace(term, '')
            
        # Remove specific unwanted terms
        colors = ['noir', 'black', 'white', 'blanc', 'argent', 'rouge', 'red', 'rose', 'pink', 'bleu', 'violet', 'beige','vert', 'turquoise', 'gris', 'gray', 'rgb']
        for term in colors:
            name = name.replace(term, '')
            
        # Remove special characters and normalize spaces
        name = re.sub(r'[^\w\s-]', ' ', name)
        name = re.sub(r'\s+', ' ', name)
        
        processed.append(name.strip())
    
    return processed


def run_analysis():
    # First, let's find the optimal epsilon value
    clusterer = ProductClusterer(min_samples=1, n_gram_range=(2, 5))
    eps_results = clusterer.find_optimal_epsilon(product_names, eps_range=(0.03, 0.1), num_steps=20)
    
    # Print epsilon analysis
    print("Epsilon analysis:")
    for eps, num_clusters in sorted(eps_results.items()):
        print(f"eps={eps:.3f}: {num_clusters} clusters")
    
    # Create clusterer with suggested parameters
    chosen_eps = 0.06  # <<--- TRY A SMALLER EPS VALUE HERE (e.g., 0.06, 0.07, 0.08)
    suggested_parameters = [
        (chosen_eps, 1, (2, 5)), 
    ]
    
    for eps, min_samples, n_gram_range in suggested_parameters:
        print(f"\n\n{'='*80}")
        print(f"PARAMETERS: eps={eps}, min_samples={min_samples}, n_gram_range={n_gram_range}")
        print(f"{'='*80}")
        
        clusterer = ProductClusterer(eps=eps, min_samples=min_samples, n_gram_range=n_gram_range)
        clusters = clusterer.identify_product_groups(product_names)
        
        # Print results
        print(f"\nFound {len(clusters)} clusters with parameters:")
        print(f"  - eps={eps}")
        print(f"  - min_samples={min_samples}")
        print(f"  - n_gram_range={n_gram_range}")
        
        # Print example clusters
        print("\nExample clusters:")
        for i, cluster in enumerate(sorted(clusters, key=len, reverse=True)):
            print(f"\nCluster {i + 1} (size: {len(cluster)}):")
            for product in cluster:
                print(f"  - {product}")
        

if __name__ == "__main__":
    run_analysis()