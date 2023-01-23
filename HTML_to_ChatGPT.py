# Split HTML source code ChatGPT
# Yedidya Harris, Jan-2023

import streamlit as st

def main():
    st.title("HTML Source Code Splitter App, for ChatGPT, by Yedidya Harris")
    st.write("This app splits HTML CODE into chunks of 10,000 chars or less, in order to send the parts to ChatGPT.")
    chunk_size = 10000
    
    html_code = st.text_area("Enter the HTML code:")
    if st.button("Split"):
        chunks = [html_code[i:i+chunk_size] for i in range(0, len(html_code), chunk_size)]
        with open("all_parts.txt", "w") as f:
            for i, chunk in enumerate(chunks):
                f.write(f"\n\nChunk {i+1}: {chunk}  !!Wait for next chunk.!!\מ")
            #f.write(f"Go!")

        st.success("HTML code has been splitted!")
        
        st.markdown("1. Send ChatGPT the following prompt:")
        st.markdown("""" "I want you to act as a senior software developer. I will provide you with the source code of a HTML page. Your task is to answer my questions  regarding the code, or fill out requests. I will send the source code of the HTML page in chunks, and once you have received a chunk, please respond with "send the rest". Do not begin programming until I give the command "Go". Your focus should be on providing the python code for my requests, and not on providing any other explanations or additional information."
                    """)
        st.markdown("2. Send each chuck as one message.")

        
        with open("all_parts.txt", "r") as f:
            file_text = f.read()
            st.text(file_text)
        
        st.text('When you finish sending all the chunks, just write GPT to "GO".')


if __name__ == '__main__':
    main()
