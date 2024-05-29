# Prompt-to-Website-Generator
 The Prompt to Website Generator simplifies custom website creation. Built with Streamlit, this user-friendly tool lets users specify website type and content to generate HTML, CSS, and JavaScript code using OpenAI's language model. The result is a modern, responsive, and visually appealing website.
## Requirements
- Python 3.10 (64-bit)
- Streamlit
- Langchain
-Installation

## Install the required Python packages:
```bash
pip install streamlit
pip install langchain
```
Set up your OpenAI API key and Unsplash API key:
Create a file named secret.py in the project directory.
Add your OpenAI API key and Unsplash API key to secret.py:
```python

OPENAIKEY = 'your_openai_api_key'
unsplash_api_key = 'your_unsplash_api_key'
```
### How to Run
Navigate to the project directory.
Run the Streamlit application:
```bash
streamlit run prompt2webpage.py
```
- Open the provided local URL (usually http://localhost:8501) in your web browser to access the application.
- Enter the type of website you want to create (e.g., portfolio, blog, e-commerce).
- Enter the content you want on your website.
- Select an image from the provided choices to use as the website background.
- Click "Generate Website" to generate the HTML, CSS, and JavaScript code.
- Preview the generated code within the application.
- Download the generated website files as a ZIP file.

