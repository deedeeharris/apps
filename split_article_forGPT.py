# Split article text for ChatGPT in order to get a summary
# Yedidya Harris, Jan-2023

import streamlit as st
#import pyperclip


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
    st.title("Article Text Splitter App, for ChatGPT, by Yedidya Harris")
    st.write("This app splits text into chunks of 2000 words or less, in order to send the parts to ChatGPT to get an entire summary.")

    text_input = st.text_area("Paste long text here:")
    if st.button("Split"):
        result = split_text(text_input)
        with open("all_parts.txt", "w") as f:
            for i, text_part in enumerate(result):
                f.write(f"\nPart{i+1}, WAIT!: {text_part} WAIT!\n")
            f.write(f"Now start summarizing. Go!")

        st.success("Text has been splitted!")
        
        st.markdown("1. Send ChatGPT the following prompt:")
        st.markdown(""""Your name is "Student". Every time you answer me, write "Student: answer". I want you to act as a PhD student and provide summaries of scientific articles that I will provide the full text of. The summaries should be concise and suitable for presentation in a classroom setting as a PowerPoint. The summary should cover the main findings and conclusions of the article, and should be written in proper academic language. You may include specific citations from my article or references in your summaries from my article. Your summary should be free of any personal opinions or bias. My first article will be attached in the following messages. Start summarizing only after you've received the entire article, and that will be when i say "GO". If you start summarizing by accident, without the entire article, I'll say "WAIT". Everytime i send you a message, reply with "You've just sent [x] number of words, send the rest!". x in the brackets, should be the number of words i just sent. "
                    """)
        st.markdown("2. Send each part of the article, in one message.")

        
        with open("all_parts.txt", "r") as f:
            file_text = f.read()
            st.text(file_text)
        
        st.text('When you finish sending all the parts, just write GPT to "GO".')


if __name__ == '__main__':
    main()
