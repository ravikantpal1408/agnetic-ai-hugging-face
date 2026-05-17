from llama_index.core import SimpleDirectoryReader

reader = SimpleDirectoryReader(input_dir="path/to/your/folder")

doc = reader.load_data()
