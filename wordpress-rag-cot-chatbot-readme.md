# WordPress RAG-CoT Chatbot

This project implements a chatbot that uses Retrieval-Augmented Generation (RAG) and Chain of Thought (CoT) reasoning to answer queries based on content from a WordPress site. The chatbot fetches content, generates embeddings, performs similarity searches, and provides step-by-step reasoning for its responses.

## Features

- Fetch content from WordPress sites
- Generate embeddings for text content
- Perform vector similarity search
- Implement RAG (Retrieval-Augmented Generation) for relevant information retrieval
- Utilize Chain of Thought reasoning for step-by-step analysis
- Provide a simple command-line interface for user interaction

## Requirements

- Python 3.6+
- Libraries: requests, json, faiss, numpy, sentence_transformers

## Installation

1. Clone this repository:
   

2. Install the required libraries:
   

## Usage

1. Run the main script:
   

2. The chatbot will fetch content from the specified WordPress site (default is TechCrunch).

3. Once loaded, you can start interacting with the chatbot by typing your queries.

4. Type 'exit' to end the conversation.

## Code Structure

1. **Data Retrieval**: The `fetch_wp_content` function retrieves content from a WordPress site using its API.

2. **Embedding Generator**: Utilizes the SentenceTransformer library to generate embeddings for text content.

3. **Vector Database**: Initializes a Faiss index for efficient similarity search.

4. **RAG Processor**: The `rag_processor` function retrieves relevant content based on a user query using vector similarity search.

5. **Chain of Thought Module**: The `chain_of_thought` function implements a simplified thought process for analyzing and responding to queries.

6. **User Interface**: The `chatbot_interface` function provides a command-line interface for interacting with the chatbot.

## Customization

- To use a different WordPress site, modify the `site_url` variable in the main execution block.
- Adjust the `top_k` parameter in the `rag_processor` function to retrieve more or fewer relevant texts.
- Modify the `chain_of_thought` function to implement more sophisticated reasoning processes.

## Limitations

- The chatbot's knowledge is limited to the content fetched from the specified WordPress site.
- The current implementation uses a simplified Chain of Thought process and does not include a language model for generating responses.

## Contributing

Contributions to improve the chatbot's functionality or efficiency are welcome. Please submit a pull request or open an issue to discuss proposed changes.


