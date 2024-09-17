# Install necessary libraries 
# !pip install fastapi uvicorn transformers torch sentence-transformers faiss-cpu numpy
'''
The code imports necessary libraries such as FastAPI, transformers, FAISS, and sentence transformers to build 
an API that handles updating and querying posts. A FastAPI instance is initialized, loading the BART model for 
text generation and a sentence transformer for embeddings, along with a FAISS index for similarity search using 
a 384-dimensional space. Post data is stored in an in-memory list, with Pydantic models defining the structure 
for posts and chat messages. The /update_post endpoint updates or adds post content and its embedding to the 
FAISS index, while the /chat endpoint generates responses by encoding a chat query, retrieving relevant posts 
from the FAISS index, and using the BART model to generate a response based on the query and retrieved context. 
The app is run locally on port 8000 using uvicorn.run.
'''

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import uvicorn
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

app = FastAPI()

# Load models and initialize components
tokenizer = AutoTokenizer.from_pretrained("facebook/bart-large")
model = AutoModelForSeq2SeqLM.from_pretrained("facebook/bart-large")
embedding_model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Initialize FAISS index
dimension = 384  # Dimension of the paraphrase-MiniLM-L6-v2 model
index = faiss.IndexFlatL2(dimension)

# In-memory storage for post content (replace with database in production)
posts = []

class PostContent(BaseModel):
    id: int
    content: str

class ChatMessage(BaseModel):
    message: str

@app.post("/update_post")
async def update_post(post: PostContent):
    # Update post content and embedding
    embedding = embedding_model.encode([post.content])[0]
    if post.id < len(posts):
        posts[post.id] = post.content
        index.remove_ids(np.array([post.id]))
    else:
        posts.append(post.content)
    index.add(np.array([embedding]).astype('float32'))
    return {"status": "success"}

@app.post("/chat")
async def chat(message: ChatMessage):
    # Generate embedding for the query
    query_embedding = embedding_model.encode([message.message])[0]
    
    # Search for relevant posts
    k = 3  # Number of relevant posts to retrieve
    D, I = index.search(np.array([query_embedding]).astype('float32'), k)
    relevant_posts = [posts[i] for i in I[0] if i < len(posts)]
    
    # Prepare context
    context = "\n".join(relevant_posts)
    
    # Generate response
    input_text = f"Query: {message.message}\n\nContext: {context}"
    inputs = tokenizer(input_text, return_tensors="pt", max_length=1024, truncation=True)
    outputs = model.generate(**inputs, max_length=150, num_return_sequences=1, num_beams=4)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    
    return {"response": response}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
