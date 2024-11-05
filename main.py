import wikipediaapi
import importlib

# Dynamically import classes from llama_index
llama_index = importlib.import_module("llama_index")

# Function to initialize Wikipedia API
def initialize_wiki():
    return wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent="Gowtham RAG Learning Assistant (gowthammourya9@gmail.com)"
    )

# Function to collect documents from Wikipedia
def collect_documents(wiki, topics):
    documents = []
    for topic in topics:
        try:
            page = wiki.page(topic)
            if page.exists():
                documents.append({"text": page.text, "title": topic})
        except Exception as e:
            print(f"Error fetching page for {topic}: {e}")
    return documents

# Function to setup the document index using llama_index
def setup_pipeline(documents):
    if not documents:
        print("No documents found for the topics provided.")
        return None

    try:
        # Convert documents to Llama Index Document format
        llama_docs = [llama_index.Document(text=doc['text'], metadata={"title": doc['title']}) for doc in documents]
        
        # Create a SimpleDocumentIndex or equivalent
        index = llama_index.SimpleDocumentIndex(llama_docs)  # Change if needed based on actual class
        return index
    except AttributeError as e:
        print(f"Error while setting up the index: {e}")
        return None

# Function to ask a question using llama_index
def ask_question(index, query):
    try:
        # Using the index to get the response for the query
        response = index.query(query)
        return response
    except Exception as e:
        print(f"Error in asking question: {e}")
        return "An error occurred while processing the question."

# Function to save output to a file
def save_output_to_file(filename, response, documents):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("AI-Powered Assistant Response:\n")
        file.write(response + "\n\n")
        file.write("Collected Documents:\n")
        for doc in documents:
            file.write(f"Document Title: {doc['title']}\n")
            file.write(f"Content: {doc['text']}\n")  # Write full content without truncation
            file.write("\n")

# Main function
def main():
    wiki = initialize_wiki()
    topics = ["Natural language processing", "Machine learning", "Artificial intelligence"]
    documents = collect_documents(wiki, topics)

    index = setup_pipeline(documents)
    if index:
        query = "What is natural language processing?"
        response = ask_question(index, query)
        
        # Save the output to a file
        output_filename = "output.txt"
        save_output_to_file(output_filename, response, documents)
        print(f"Output saved to {output_filename}")

    # Optional: Print collected documents for debugging
    print("\nCollected Documents:")
    for doc in documents:
        print(f"Document Title: {doc['title']}")
        print(f"Content: {doc['text']}")  # Print full content without truncation

if __name__ == "__main__":
    main()
