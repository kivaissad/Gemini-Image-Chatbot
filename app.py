import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure the API key
genai.configure(api_key='GOOGLE_API_KEY')

# Initialize conversation history
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history=[]

# Define the prompt template
def create_prompt(conversation_history, user_input):
    template="""
    You are an AI model made by Avik Das. You are an expert in understanding images and describing them.
    You respond every question in a humorous, sarcastic, and sassy manner typical of Indian and Asian cultures. 
    Use cultural references, idioms, and humor that are relatable in India and Asia. 
    Every response must be funny, sarcastic, and witty.
    
    {conversation_history}
    User: {user_input}
    Assistant:
    """
    return template.format(conversation_history=conversation_history, user_input=user_input)

# Function to get response from the Gemini model
def get_gemini_response(input_text, image, conversation_history):
    # Prepare the conversation history
    conversation_str=""
    for turn in conversation_history:
        conversation_str+=f"{turn['role']}: {turn['content']}\n"

    # Create the prompt
    prompt=create_prompt(conversation_str, input_text)

    # Generate the response
    response=genai.GenerativeModel('gemini-pro-vision').generate_content([prompt, image[0]])

    # Add the user's input and the model's response to the conversation history
    conversation_history.append({"role": "user", "content": input_text})
    conversation_history.append({"role": "assistant", "content": response.text})

    return response.text

def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data=uploaded_file.getvalue()
        image_parts=[
            {
                'mime_type': uploaded_file.type,
                'data': bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError('No File Uploaded')

# Initialize the Streamlit app
st.set_page_config(page_title='Custom Image Descriptor')
st.header('Custom Image Descriptor')

input_text=st.text_input('Input Prompt: ', key='input')
uploaded_file=st.file_uploader('Choose an image of your liking...', type=['jpg', 'jpeg', 'png'])

image=''

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_column_width=True)

submit=st.button('Tell me about the picture')

# If the submit button is clicked
if submit:
    if uploaded_file is not None:
        image_data=input_image_details(uploaded_file)
        response=get_gemini_response(input_text, image_data, st.session_state.conversation_history)
        st.subheader('The response is:')
        st.write(response)
    else:
        st.write("Please upload an image.")

# Display conversation history
st.subheader('Conversation History:')
for turn in st.session_state.conversation_history:
    st.write(f"**{turn['role'].capitalize()}:** {turn['content']}")
