import streamlit as st

def split_text(text):
    # Split the text into words
    words = text.split()
    # Initialize an empty list to store the resulting strings
    result = []
    # Initialize a variable to keep track of the current string
    current_string = ""
    # Iterate over the words
    for word in words:
        # If adding the word to the current string would exceed the 2000 word limit
        if len(current_string.split()) + len(word.split()) > 2000:
            # Append the current string to the result list
            result.append(current_string)
            # Reset the current string
            current_string = ""
        # Add the word to the current string
        current_string += " " + word
    # Append the final string to the result list
    result.append(current_string)
    return result

def main():
    st.title("Text Splitter App")
    st.write("This app splits text into chunks of 2000 words or less, saves each chunk in a new line in a text file named 'all_parts.txt', adds 'WAIT!' at the beginning and end of each chunk, and adds instructions at the end of the file")

    text_input = st.text_area("Enter the text:")
    if st.button("Split and Save"):
        result = split_text(text_input)
        with open("all_parts.txt", "w") as f:
            for i, text_part in enumerate(result):
                f.write(f"\nPart{i+1}, WAIT!: {text_part} WAIT!\n")
            f.write(f"\nNow start summarizing. Go!")

        st.success("Text has been splitted and saved in all_parts.txt")
        st.text(open("all_parts.txt").read())

if __name__ == '__main__':
    main()
