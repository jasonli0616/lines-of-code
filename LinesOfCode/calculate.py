import os


def get_directory_name(directory) -> str:
    """
    Returns the directory name (without path).

    Parameters:
        directory
            - the directory to check
    
    Returns:
        str
            - the directory name
    """

    return os.path.basename(directory)


def get_lines_of_code(directory, whitelist: bool, file_extensions: list):
    lines_of_code = 0
    blanklines_of_code = 0
    characters_of_code = 0

    listdir = os.listdir(directory)

    for item in listdir:

        if item == ".git":
            continue

        full_path = os.path.join(directory, item)

        # Check if the user entered file extensions to filter
        if file_extensions:

            if whitelist:
                # If the file's extension is not in the filter list, skip iteration
                if os.path.isfile(full_path) and not (os.path.splitext(item)[1] in file_extensions) and not (item in file_extensions):
                    continue
            
            else:
                # If the file's extension is in the filter list, skip iteration
                if (os.path.splitext(item)[1] in file_extensions) or (item in file_extensions):
                    continue

        # If the path is a file
        if os.path.isfile(full_path):

            try:
                with open(full_path, "r") as f:

                    for line in f:

                        # Increment lines of code
                        lines_of_code += 1

                        # Increment lines of blank code, if line is blank
                        if line.strip() == "": blanklines_of_code += 1

                        for character in line:
                            # Increment characters of code, if there is a character
                            if character.strip() != "": characters_of_code += 1
                    
                    f.close()
            except:
                # Ignore files that cannot be opened
                pass

        # If the path is a directory
        elif os.path.isdir(full_path):

            # Recursively get data
            subdirectory = get_lines_of_code(full_path, whitelist, file_extensions)

            # Increment accordingly
            lines_of_code += subdirectory[0]
            blanklines_of_code += subdirectory[1]
            characters_of_code += subdirectory[2]


    return lines_of_code, blanklines_of_code, characters_of_code