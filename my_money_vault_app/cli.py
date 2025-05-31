def first_letter_upper(input_name):
    return input_name[0].upper() + input_name[1:]

def create_model_file(entity_name):
    entity_name_model_file = f"src/Models/{first_letter_upper(entity_name)}.py"
    with open(entity_name_model_file, "w") as file:
        file_content = f"class {first_letter_upper(entity_name)}:"
        file.write(file_content)
    print(f"Model file {entity_name_model_file} created successfully!")

def create_repository_file(entity_name):
    entity_name_repository_file = f"src/Repositories/{first_letter_upper(entity_name)}Repository.py"
    with open(entity_name_repository_file, "w") as file:
        file_content = f"class {first_letter_upper(entity_name)}Repository:"
        file.write(file_content)
    print(f"Repository file {entity_name_repository_file} created successfully!")

entity_name = input("Give the entity name: ")

create_model_file(entity_name)
create_repository_file(entity_name)
