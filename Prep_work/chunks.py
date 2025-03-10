def generate_chunks(filename):
    data = []
    final_chunk = []

    loader = TextLoader(filename, encoding="utf-8")
    rawdata = loader.load()
    if rawdata:
        text_splitter = CharacterTextSplitter(chunk_size=5000, chunk_overlap=100)
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