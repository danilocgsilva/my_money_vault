entity_name = input("Give the entity name: ")

entity_name_model_file = f"src/Models/{entity_name}.py"

with open(entity_name_model_file, "a") as file:
    file_content = "class State:"
    file.write(file_content)
