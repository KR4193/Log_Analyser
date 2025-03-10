import csv
import os
import io
import shutil
import zipfile

import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import CharacterTextSplitter

embedding_model = "all-MiniLM-L6-v2"
database_name = "sample_db"
input_filename = "budget.txt"
def generate_chunks(filename):
    data = []
    final_chunk = []

    loader = TextLoader(filename, encoding="utf-8")
    rawdata = loader.load()
    if rawdata:
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        data = text_splitter.split_documents(rawdata)
        if data:
            print(f"generate_chunks - {filename}")
            final_chunk += data
        else:
            print(f"generate_chunks - data is None")
    else:
        print(f"generate_chunks - rawdata is None")

    print(f"{filename} data chunks ready for embedding")

        # Add more conditions for other file types if needed
    print("prepare_data_chunks: finished")
    return final_chunk


def create_vectordb(filepath, databasename):
    data = generate_chunks(filepath)
    if data:
        print(f"Starting to create {filepath} ...")
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        print(f"embedding : {embeddings}")
        if embeddings:
            vdatabase = FAISS.from_documents(data, embeddings)
            vdatabase.save_local(databasename)
            print(f" vectordatabase {databasename} ready...")
        else:
            print(f"Empty Embeddings")
        return vdatabase
    else:
        print("chunk data received is null, exiting database creation")
        return None


def load_vector_db(embedding_model_name, vector_db_name):
    print(f" Loading {vector_db_name} ...")
    if os.path.exists(vector_db_name):
        print(f" database {vector_db_name} present!!")
        embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name)
        if embeddings:
            vector_db = FAISS.load_local(vector_db_name, embeddings, allow_dangerous_deserialization=True)
            print(f" Loading {vector_db_name} Done!!")
        else:
            print(f"Empty Embeddings")
    else:
        print(f" No file path found for {vector_db_name}..")
    return vector_db

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # Create vector data base
    local_vectordb = create_vectordb(input_filename, database_name)

    # Load existing database using db name
    vector_db = load_vector_db(embedding_model, database_name)

    # Initialze the retriver with retrieval method
    #retriever = jira_vector_db.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.1})
    retriever = vector_db.as_retriever(search_type="mmr", search_kwargs={"k":20})

    # Query the database to get symantical search output
    retrieved_output = retriever.invoke("What is this document about?")
    print(f"vectordb ready")
