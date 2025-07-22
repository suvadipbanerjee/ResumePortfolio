# Resume to Portfolio Converter

Turn your boring resume into a beautiful portfolio in just **1 click**!
Built using **OpenAI**, **Streamlit**, **FastAPI**, and **Jinja2**, and deployed with **Netlify** 

## Tech Stack

* **OpenAI** – Smart content generation
* **FastAPI** – Fast and modern backend
* **Jinja2** – Dynamic HTML templates
* **Streamlit** – Simple and beautiful frontend
* **Netlify** – Fast deployment

## How It Works

1. Upload your resume
2. Choose Your Template
3. AI reads your data
4. Generates a clean, stylish portfolio
5. View your personal published website

## Run Locally

```bash
# 1. Clone this repo
git clone https://github.com/suvadipbanerjee/ResumePortfolio.git
cd Resume-Portfolio

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run backend
uvicorn backend.main:app --reload

# 4. Run frontend
streamlit run app.py
```

