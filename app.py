import streamlit as st
import base64
import tempfile
import os
import re
from gtts import gTTS
from euriai import EuriaiClient

# Set page configuration
st.set_page_config(page_title="Recipe Voice Generator", layout="wide")

# Initialize session state variables
if 'formatted_recipe' not in st.session_state:
    st.session_state.formatted_recipe = None
if 'audio_file' not in st.session_state:
    st.session_state.audio_file = None

# Get API key from Streamlit secrets
def get_api_key():
    try:
        return st.secrets["EURIAI_API_KEY"]
    except Exception:
        return None

# Function to clean markdown for voiceover
def clean_text_for_voiceover(text):
    # Remove markdown bold/italic (**, *, __, _)
    text = re.sub(r'[\*]{1,2}|[_]{1,2}', '', text)
    # Remove markdown headers (#, ##, etc.)
    text = re.sub(r'#+ ', '', text)
    # Replace numbered lists (e.g., "1. Step" -> "Step one")
    def replace_numbered_list(match):
        number = int(match.group(1))
        numbers_in_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
        if number <= len(numbers_in_words):
            return f"Step {numbers_in_words[number-1]}: "
        return f"Step {number}: "
    text = re.sub(r'(\d+)\.\s*', replace_numbered_list, text)
    # Remove extra newlines and spaces
    text = ' '.join(text.split())
    return text

# Function to format recipe using Euriai API
def format_recipe(recipe_text, language, model):
    try:
        api_key = get_api_key()
        if not api_key:
            st.error("API key not found. Please configure it in Streamlit secrets.")
            return None
        
        client = EuriaiClient(api_key=api_key, model=model)
        
        if language == "Bengali":
            prompt = f"""
            নিম্নলিখিত রেসিপিটিকে একটি সুসংগঠিত ফর্ম্যাটে রূপান্তর করুন:
            1. শিরোনাম
            2. উপকরণ (তালিকা হিসাবে)
            3. প্রস্তুত প্রণালী (ক্রমিক পদক্ষেপ হিসাবে)
            4. রান্নার সময় এবং পরিবেশনের পরিমাণ
            
            নিশ্চিত করুন যে ভাষা পরিষ্কার, সংক্ষিপ্ত এবং রান্নার ভিডিওর জন্য অনুসরণ করা সহজ।
            
            রেসিপি: {recipe_text}
            """
        else:
            prompt = f"""
            Format the following recipe into a well-structured format with:
            1. Title
            2. Ingredients (as a list)
            3. Instructions (as numbered steps)
            4. Cooking time and servings
            
            Make sure the language is clear, concise, and easy to follow for a cooking video.
            
            Recipe: {recipe_text}
            """
        
        response = client.generate_completion(
            prompt=prompt,
            temperature=0.7,
            max_tokens=800
        )
        
        response_text = None
        if isinstance(response, dict) and "choices" in response:
            choices = response.get("choices", [])
            if choices and isinstance(choices, list) and "message" in choices[0]:
                response_text = choices[0].get("message", {}).get("content")
        
        if response_text and isinstance(response_text, str):
            return response_text.strip()
        else:
            st.error("No valid text found in the API response.")
            return None
    except Exception as e:
        st.error(f"Error formatting recipe: {str(e)}")
        return None

# Function to generate voiceover with different accents
def generate_voiceover(text, language_option):
    try:
        language_map = {
            "American English": {"lang": "en", "tld": "com"},
            "British English": {"lang": "en", "tld": "co.uk"},
            "Australian English": {"lang": "en", "tld": "com.au"},
            "Bangladeshi English": {"lang": "en", "tld": "co.in"},
            "Bengali": {"lang": "bn", "tld": "com"}
        }
        
        lang_settings = language_map.get(language_option)
        if not lang_settings:
            st.error(f"Unsupported language option: {language_option}")
            return None
        
        # Clean text for voiceover
        cleaned_text = clean_text_for_voiceover(text)
        
        # Generate TTS
        tts = gTTS(
            text=cleaned_text,
            lang=lang_settings["lang"],
            tld=lang_settings["tld"],
            slow=False
        )
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_file = fp.name
            tts.save(temp_file)
        
        # Verify file exists
        if not os.path.exists(temp_file):
            st.error(f"Failed to create audio file: {temp_file}")
            return None
        
        return temp_file
    except Exception as e:
        st.error(f"Error generating voiceover: {str(e)}")
        return None

# Function to get download link for audio
def get_audio_download_link(file_path, filename):
    try:
        if not os.path.exists(file_path):
            st.error(f"Audio file not found: {file_path}")
            return None
        with open(file_path, "rb") as file:
            contents = file.read()
        b64 = base64.b64encode(contents).decode()
        return f'<a href="data:audio/mp3;base64,{b64}" download="{filename}">Download Voiceover</a>'
    except Exception as e:
        st.error(f"Error creating download link: {str(e)}")
        return None

# App title and description
st.title("Recipe Voice Generator")
st.write("Convert your recipe descriptions to formatted text and generate voiceovers for your cooking videos")

# Sidebar for API configuration
with st.sidebar:
    st.header("Model Configuration")
    model = st.selectbox(
        "Select Model", 
        ["gpt-4.1-mini", "gemini-2.0-flash-001", "qwen-qwq-32b"],
        index=0
    )
    
    api_key = get_api_key()
    if api_key:
        st.success("API Key: Configured ✓")
    else:
        st.error("API Key: Not configured ✗")
        st.info("Please configure your API key in Streamlit secrets.")
        st.markdown("""
        ### How to configure secrets:
        1. **Local Development**: Create a `.streamlit/secrets.toml` file:
        ```toml
        EURIAI_API_KEY = "your_api_key_here"
        ```
        2. **Streamlit Cloud**: Add your secret in the app dashboard:
           - Go to 'Settings' > 'Secrets'
           - Add `EURIAI_API_KEY` with your API key
        """)
    
    st.header("App Info")
    st.info("This app formats recipes and generates voiceovers for cooking videos. Enter a recipe in English or Bengali to get a structured format and voiceover in your preferred accent.")

# Main app interface
col1, col2 = st.columns(2)

with col1:
    st.header("Recipe Input")
    language_option = st.selectbox(
        "Select Language/Accent", 
        ["American English", "British English", "Australian English", "Bangladeshi English", "Bengali"],
        index=0
    )
    
    format_language = "Bengali" if language_option == "Bengali" else "English"
    
    recipe_text = st.text_area(
        "Enter your recipe description",
        height=300,
        placeholder="Type your recipe here in simple language..."
    )
    
    if st.button("Format Recipe"):
        if get_api_key():
            with st.spinner("Formatting recipe..."):
                formatted_recipe = format_recipe(recipe_text, format_language, model)
                if formatted_recipe:
                    st.session_state.formatted_recipe = formatted_recipe
                    st.session_state.audio_file = None  # Reset audio file on new recipe
                    st.success("Recipe formatted successfully!")
        else:
            st.warning("Please configure your Euriai API Key in Streamlit secrets first")

with col2:
    st.header("Formatted Recipe")
    if st.session_state.formatted_recipe:
        st.markdown(st.session_state.formatted_recipe)
        
        if st.button("Generate Voiceover"):
            with st.spinner(f"Generating voiceover with {language_option} accent..."):
                audio_file = generate_voiceover(st.session_state.formatted_recipe, language_option)
                if audio_file:
                    st.session_state.audio_file = audio_file
                    st.success("Voiceover generated successfully!")
    else:
        st.info("Your formatted recipe will appear here after processing")

# Display audio player and download link
if st.session_state.audio_file:
    st.header("Voiceover")
    try:
        if not os.path.exists(st.session_state.audio_file):
            st.error(f"Audio file not found: {st.session_state.audio_file}")
        else:
            with open(st.session_state.audio_file, "rb") as f:
                audio_bytes = f.read()
            st.audio(audio_bytes, format="audio/mp3")
            
            filename = f"recipe_voiceover_{language_option.lower().replace(' ', '_')}.mp3"
            download_link = get_audio_download_link(st.session_state.audio_file, filename)
            if download_link:
                st.markdown(download_link, unsafe_allow_html=True)
            
            # Clean up temporary file after use
            try:
                os.unlink(st.session_state.audio_file)
                st.session_state.audio_file = None  # Clear session state
            except Exception as e:
                st.warning(f"Failed to delete temporary file: {str(e)}")
    except Exception as e:
        st.error(f"Error playing audio: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Created with ❤️ for cooking enthusiasts")