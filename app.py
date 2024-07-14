import warnings
import streamlit as st
import google.generativeai as palm
from google.api_core import retry

# Suppress warnings
warnings.filterwarnings('ignore')

# Configure the API key for the Google Generative AI
palm.configure(api_key='AIzaSyAriIMWwoijQfqDP25qflpSHuliIzq_RV8')

# Get the model for text generation
models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model_bison = models[0]

# Define the retry mechanism
@retry.Retry()
def generate_text(prompt, model=model_bison, temperature=0.0):
    return palm.generate_text(prompt=prompt, model=model, temperature=temperature)

# Define the prompt template
prompt_template = """
You are a seasoned senior programmer.
Your extensive knowledge spans various programming languages, frameworks, and tools.
You possess expertise in writing, debugging, and optimizing code,
as well as addressing a wide range of programming-related inquiries.

When given a task, your goal is to provide the most effective and accurate solution.
This could involve writing clean, efficient code,
identifying and fixing bugs, optimizing existing code for performance,
or offering insightful advice on best practices and implementation strategies.

The given task is: 
{task}
"""


# Streamlit app

st.title("Code Assistant Application")
# Chat input for the task
task = st.chat_input("Enter your programming task here:")

# Generate code when input is provided
if task:
    with st.spinner('Generating code...'):
        prompt = prompt_template.format(task=task)
        try:
            response = generate_text(prompt)
            generated_code = response.result

            st.write(generated_code)
        except Exception as e:
            st.error(f"An error occurred: {e}")
