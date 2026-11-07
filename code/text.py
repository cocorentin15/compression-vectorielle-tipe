import pyperclip


def insert_character():
    text = input("Enter the text: ")
    char_to_detect = ")"
    char_to_insert = " \n \n "
    result = ""

    for char in text:
        result += char
        if char == char_to_detect:
            result += char_to_insert

    pyperclip.copy(result)
    return result

# Call the function
for i in range(999):
    print(insert_character())