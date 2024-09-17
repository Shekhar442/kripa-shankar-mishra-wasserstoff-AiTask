# Import necessary libraries
'''
This code snippet imports essential libraries for tasks such as making HTTP requests, handling JSON data, 
performing vector similarity search, and transforming sentences into embeddings.
'''
import os
import requests
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# 1. Data Retrieval
'''
This code snippet defines a function called fetch_wp_content that retrieves content from a WordPress site using its 
API. The function constructs the appropriate URL based on the site URL and an optional post ID, makes an HTTP request, 
and returns the content in JSON format. If any errors occur during the request, it prints an error message and returns 
an empty list.
'''
def fetch_wp_content(site_url, post_id=None):
    site_url = site_url.rstrip('/')
    url = f"{site_url}/wp-json/wp/v2/posts"
    if post_id:
        url += f"/{post_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"An error occurred while fetching WordPress content: {e}")
        return []

# 2. Embedding Generator
'''
This code snippet defines an embedding generator using the SentenceTransformer library. It initializes a model 
(specifically, ‘paraphrase-MiniLM-L6-v2’) and provides a function (generate_embeddings) that encodes input texts into 
dense vector embeddings. If no texts are provided, it returns an empty NumPy array.
'''
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

def generate_embeddings(texts):
    if not texts:
        return np.array([])
    return model.encode(texts)

# 3. Vector Database
'''
This code snippet initializes a vector database using Faiss. It creates an index (specifically, IndexFlatL2) for 
efficient similarity search in a high-dimensional space (384 dimensions in this case).
'''
dimension = 384  # Dimension of the embeddings
index = faiss.IndexFlatL2(dimension)

# 4. RAG Processor
'''
The rag_processor function retrieves relevant content based on a user query using vector similarity search and semantic 
embeddings
'''
def rag_processor(query, top_k=3):
    if index.ntotal == 0:
        return ["No content available to process the query."]
    query_embedding = generate_embeddings([query])
    D, I = index.search(query_embedding.astype('float32'), top_k)
    retrieved_texts = [all_texts[i] for i in I[0]]
    return retrieved_texts

# 5. Chain of Thought Module (simplified)
'''
The chain_of_thought function simplifies the thought process by listing relevant information, analyzing key points, and 
formulating a response based on the query and retrieved texts. 
'''
def chain_of_thought(query, retrieved_texts):
    prompt = f"Query: {query}\n\nRelevant information:\n"
    for i, text in enumerate(retrieved_texts, 1):
        prompt += f"{i}. {text}\n"
    prompt += "\nThinking step by step:\n1. Consider the query and relevant information.\n2. Analyze the key points in the retrieved texts.\n3. Formulate a response based on the analysis.\n\nResponse: "
    return prompt

# 6. User Interface 
'''
The chatbot_interface function provides a user-friendly interface for interacting with the WordPress RAG-CoT Chatbot. 
Users can input queries, receive relevant information, and get step-by-step thought processes leading to potential answers.
'''
def chatbot_interface():
    print("Welcome to the WordPress RAG-CoT Chatbot!")
    print("Type 'exit' to end the conversation.")
    
    while True:
        query = input("You: ")
        if query.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        retrieved_texts = rag_processor(query)
        cot = chain_of_thought(query, retrieved_texts)
        
        print("Chatbot (thinking):")
        print(cot)
        print("\nChatbot (response):")
        print("Based on the relevant information, here's a possible answer to your query...")

# Main execution
'''
 The provided code snippet orchestrates the main execution of a chatbot that interacts with a WordPress site, retrieves content, 
 generates embeddings, and engages in user conversations through a simple interface.
'''
if __name__ == "__main__":
    # Fetch content from a WordPress site
    site_url = "https://techcrunch.com"  # Using TechCrunch as an example
    posts = fetch_wp_content(site_url)
    
    if not posts:
        print("No posts were fetched. The chatbot will have limited functionality.")
        all_texts = ["No content available."]
    else:
        # Extract text content from posts
        all_texts = [post['title']['rendered'] + " " + post['content']['rendered'] for post in posts]
    
    # Generate embeddings and add to the index
    embeddings = generate_embeddings(all_texts)
    if embeddings.size > 0:
        index.add(embeddings.astype('float32'))
    else:
        print("No embeddings were generated. The chatbot will have limited functionality.")
    
    # Start the chatbot interface
    chatbot_interface()   
