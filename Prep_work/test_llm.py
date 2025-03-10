import os
from openai import AzureOpenAI
from langchain.chains import SimpleChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from langchain.retrievers import VectorStoreRetriever
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

client = AzureOpenAI(
  azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT"), 
  api_key=os.getenv("AZURE_OPENAI_API_KEY"),  
  api_version="2024-02-01"
)

log_file_path = "C:/Users/kr4193/Desktop/Log_error_reporter/Prep_work/clean_Geiger_for_LLMs.log"
pytest_path = "C:/Users/kr4193/Downloads/evtstuff/atf/tests/print/clean_cutter.py"

# Read the log content from the file
file = open(pytest_path, "r")
content = file.read()

def read_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

log_content = read_log_file(log_file_path)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
    You are a helpful assistant. Use the following context to answer the question.
    Context: {context}
    Question: {question}
    """
)

# Define the LLM
llm = OpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-02-01"
)

# Define the retriever
def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_db = FAISS.load_local("sample_db", embeddings, allow_dangerous_deserialization=True)
    retriever = VectorStoreRetriever(vector_db)
    return retriever

# Define the chain
def qa_chain():
    retriever = get_retriever()
    chain = SimpleChain(
        retriever=retriever,
        llm=llm,
        prompt_template=prompt_template
    )
    return chain

# Main function
if __name__ == '__main__':
    # Create vector data base
    local_vectordb = create_vectordb(log_file_path, "sample_db")

    # Load existing database using db name
    vector_db = load_vector_db("all-MiniLM-L6-v2", "sample_db")

    # Initialize the retriever with retrieval method
    retriever = vector_db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.1})

    # Define the chain
    chain = qa_chain()

    # Query the database to get semantic search output
    query = "What is the error in the log file?"
    while query != "quit":
        query = input("Enter your query: ")
        output = chain.invoke({"context": retriever, "question": query})
        print(output)
    print(f"vectordb ready")