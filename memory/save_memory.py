def save_to_memory(content):

    with open(
        "memory/documents.txt",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(str(content) + "\n")

    print("Memory saved successfully.")