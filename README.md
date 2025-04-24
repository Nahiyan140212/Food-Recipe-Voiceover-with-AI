Recipe Voice Generator
A Streamlit-based web application that converts raw recipe descriptions into a well-structured format and generates voiceovers for cooking videos. The app supports English and Bengali recipes with customizable voice accents, making it ideal for creating engaging cooking content.
Features

Recipe Formatting: Converts unstructured recipe text into a structured format with title, ingredients, instructions, cooking time, and servings using an AI model via the Euriai API.
Voiceover Generation: Generates audio voiceovers for recipes in multiple accents (American English, British English, Australian English, Bangladeshi English, Bengali) using Google Text-to-Speech (gTTS).
User-Friendly Interface: Built with Streamlit for an intuitive experience, featuring recipe input, formatted output, and audio playback/download.
Multilingual Support: Handles English and Bengali recipes with corresponding voiceovers.
Customizable Models: Supports multiple AI models (e.g., gpt-4.1-mini, gemini-2.0-flash-001, qwen-qwq-32b) for recipe formatting.

Prerequisites

Python: Version 3.8 or higher.
Euriai API Key: Required for recipe formatting. Obtain from your API provider.
Google Text-to-Speech (gTTS): Used for voiceover generation, installed via pip.
Streamlit: For the web interface, installed via pip.
Git: For version control (optional, if cloning the repository).

Installation

Clone the Repository (if using Git):
git clone <repository-url>
cd recipe-voice-generator


Create a Virtual Environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


Install Dependencies:Create a requirements.txt file with the following content:
streamlit==1.31.0
gTTS==2.5.3
euriai==<version>  # Replace with the specific version or install manually

Then run:
pip install -r requirements.txt

Note: The euriai package may require specific installation instructions from your API provider. Contact them if the package is not available on PyPI.

Configure the Euriai API Key:

Create a .streamlit directory in the project root:mkdir .streamlit


Create a secrets.toml file in .streamlit/:EURIAI_API_KEY = "your_api_key_here"


Ensure .streamlit/secrets.toml is listed in .gitignore to prevent committing sensitive data.


Verify .gitignore:Ensure your .gitignore includes:
.env
.streamlit/secrets.toml
__pycache__/
*.pyc
venv/
*.mp3
.streamlit/cache/
.streamlit/logs/
.vscode/
.idea/
.DS_Store



Usage

Run the App Locally:
streamlit run app.py

This opens the app in your default browser (e.g., http://localhost:8501).

Format a Recipe:

Select a language/accent (e.g., American English, Bengali).
Choose an AI model (e.g., gpt-4.1-mini).
Enter a raw recipe description in the text area (e.g., "Egg fry: 1 egg, 1 tbsp oil. Heat pan, add oil, crack egg, cook 2-3 min, flip, cook 1-2 min. Serves 1.").
Click Format Recipe to generate a structured recipe.


Generate a Voiceover:

After formatting, click Generate Voiceover to create an audio narration of the recipe.
Play the audio directly in the app or download the MP3 file.


Example Output:

Input: "Egg fry: 1 egg, 1 tbsp oil. Heat pan, add oil, crack egg, cook 2-3 min, flip, cook 1-2 min. Serves 1."
Formatted Recipe:**Simple Fried Egg**

**Ingredients:**
- 1 egg
- 1 tablespoon oil (or as needed)

**Instructions:**
1. Heat a pan over medium heat and add the oil.
2. Crack the egg into the pan.
3. Cook until the egg white is fully set and the edges start to crisp.
4. Carefully flip the egg using a spatula.
5. Cook the other side until done to your preference.
6. Transfer the fried egg to a plate and enjoy.

**Cooking Time:** Approximately 5 minutes
**Servings:** 1 egg


Voiceover: "Simple Fried Egg. Ingredients: 1 egg, 1 tablespoon oil or as needed. Instructions: Step one: Heat a pan over medium heat and add the oil. Step two: Crack the egg into the pan..."



Deployment to Streamlit Cloud

Push to GitHub:

Ensure your repository is pushed to GitHub with app.py, requirements.txt, and .gitignore.
Do not commit .streamlit/secrets.toml.


Create a Streamlit Cloud App:

Go to Streamlit Cloud.
Click New App and connect your GitHub repository.
Select the branch and specify app.py as the main file.


Configure Secrets:

In the Streamlit Cloud dashboard, go to your app’s Settings > Secrets.
Add:EURIAI_API_KEY = "your_api_key_here"




Deploy:

Click Deploy. The app will build and be available at a URL like https://your-app-name.streamlit.app.


Troubleshooting Deployment:

Check the build logs in Streamlit Cloud for errors (e.g., missing dependencies).
Ensure euriai is installable in the cloud environment. If proprietary, contact your API provider for deployment instructions.



File Structure
recipe-voice-generator/
├── .gitignore              # Ignores sensitive and temporary files
├── .streamlit/
│   └── secrets.toml        # Stores Euriai API key (not committed)
├── app.py                  # Main Streamlit application
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation

Troubleshooting

Error: "API key not found":

Ensure EURIAI_API_KEY is set in .streamlit/secrets.toml (local) or Streamlit Cloud secrets.
Verify the key is valid with your API provider.


Error: "No valid text found in the API response":

Check the API response structure in app.py (format_recipe function).
Ensure the selected model (e.g., gpt-4.1-mini) is supported by your Euriai API key.


Error: "FileNotFoundError" for MP3 files:

Verify write permissions in the system’s temporary directory (e.g., C:\Users\<YourUser>\AppData\Local\Temp on Windows).
Test locally before deploying to Streamlit Cloud, as temporary file handling differs.


Voiceover Issues:

If the voice reads markdown (e.g., "asterisk"), ensure clean_text_for_voiceover is working.
For better voice quality, consider integrating Google Cloud Text-to-Speech (requires API key).


Contact Support:

For euriai issues, contact your API provider.
For Streamlit issues, check the Streamlit Community.



Contributing
Contributions are welcome! To contribute:

Fork the repository.
Create a feature branch (git checkout -b feature/your-feature).
Commit changes (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a pull request.

Please include tests and update documentation as needed.
License
This project is licensed under the MIT License. See the LICENSE file for details (create a LICENSE file if needed).
Acknowledgments

Built with Streamlit for the web interface.
Powered by gTTS for text-to-speech.
Uses the Euriai API for recipe formatting (proprietary, contact provider for access).

