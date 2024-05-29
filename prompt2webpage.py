import streamlit as st
import requests
import json
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
from secret import OPENAIKEY , unsplash_api_key
import os
import base64
import zipfile
import io

os.environ['OPENAI_API_KEY'] = OPENAIKEY

llm=OpenAI(temperature=0.9, max_tokens=3800)

def generate_website_components(website_type, website_content, img_path=None):
    chains = {
        'html': {
            'prompt': f"""Generate a single HTML code for a modern, ready-to-deploy {website_type} type website with the following user-provided content: {website_content}. The website should have a responsive layout with a header, main content area, and a footer. The header should include a navigation bar with dropdown menus. The main content area should be divided into sections as per the requirements of a {website_type} website, including interactive elements like image sliders, forms, and modals. The website should have a modern and visually appealing look. Ensure the website is responsive and looks good on all device sizes.The html code should contain links to "style.css" for css styling and "script.js" for javascript script.""",
            'output_key': 'html_code'
        },
        'css': {
            'prompt': f"""Generate a single CSS code for a modern, ready-to-deploy {website_type} type website with the following user-provided content: {website_content}. The website should have a responsive layout with a header, main content area, and a footer. The header should include a navigation bar with dropdown menus. The main content area should be divided into sections as per the requirements of a {website_type} website, including interactive elements like image sliders, forms, and modals. The website should have a modern and visually appealing look. Ensure the website is responsive and looks good on all device sizes.Do not include a background color inside the body section.Make sure to only generate the raw code and not include any other text apart from the code.""",
            'output_key': 'css_code'
        },
        'js': {
            'prompt': f"""Generate the JavaScript code for the HTML structure provided in the first prompt. Implement necessary interactive features such as form validation, responsive navigation menu, modals, image sliders, or any other feature relevant to a {website_content} website. Use modern JavaScript features and ensure the code is efficient and error-free.""",
            'output_key': 'js_code'
        }
    }

    response = {}
    for code_type, chain_info in chains.items():
        prompt_template = PromptTemplate(
            input_variables=['website_type', 'website_content'],
            template=chain_info['prompt']
        )
        chain = LLMChain(llm=llm, prompt=prompt_template, output_key=chain_info['output_key'])
        chain_response = chain({'website_type': website_type, 'website_content': website_content})
        response[chain_info['output_key']] = chain_response[chain_info['output_key']]

    return response

def add_background_image_to_css(css_code, img_url):
    css_code = css_code.replace("CSS Code:", "").strip()
    body_index = css_code.find('body {')
    if body_index != -1:
        css_code = css_code[:body_index+6] + f"\n\tbackground-image: url('{img_url}');\n\tbackground-repeat: no-repeat;\n\tbackground-size: cover;" + css_code[body_index+6:]
    else:
        css_code += f"\nbody {{\n\tbackground-image: url('{img_url}');\n\tbackground-repeat: no-repeat;\n\tbackground-size: cover;\n}}"

    return css_code

def main():
    st.title("Web-Designer")
    website_type = st.text_input("Enter the type of website you want to create:")
    website_content = st.text_area("Enter the content you want on your website:")
    api_key = unsplash_api_key
    response = requests.get(f"https://api.unsplash.com/search/photos?query={website_type}&per_page=5&client_id={api_key}")
    images = json.loads(response.text)["results"]

    if "img_url" not in st.session_state:
        st.session_state.img_url = None

    for i, img in enumerate(images):
        st.image(img["urls"]["small"], width=200)
        if st.button(f"Select Image {i+1}"):
            st.session_state.img_url = img["urls"]["small"]
            st.write(f"You have selected this Image-{st.session_state.img_url}")

    if website_type and website_content and st.button("Generate Website") and st.session_state.img_url is not None:
        response = generate_website_components(website_type, website_content, img_path=st.session_state.img_url)
        html_code = response['html_code']
        css_code = response['css_code']
        js_code = response['js_code']

        css_code = add_background_image_to_css(css_code, st.session_state.img_url)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zip_file:
            zip_file.writestr('webpage.html', html_code)
            zip_file.writestr('style.css', css_code)
            zip_file.writestr('script.js', js_code)
        zip_buffer.seek(0)

        st.code(html_code, language='html')
        st.code(css_code, language='css')
        st.code(js_code, language='javascript')

        st.download_button('Download Website Files', zip_buffer.getvalue(), 'website_files.zip', 'application/zip')

if __name__=="__main__":
    main()
