# ForTrace Chatbot

This chatbot converts a forensic scenario into a YAML file for ForTrace.

![Personas](./images/screenshot1.png)

![Relations](./images/screenshot2.png)

![YAML](./images/screenshot3.png)

## How to use

You can run the app either locally or with `docker`. Ensure to install all dependencies when running locally.

Add your OpenAI API key to `./.streamlit/secrets.toml`.

## Dependencies

```bash
pip install faiss-cpu langchain langchain-core \
    langchain-openai langchain-community langgraph streamlit \
    python-dotenv langchain-google-genai ruamel.yaml \
     langchain-google-genai
```

### Run app locally

Before you run the app locally ensure that you change the file path of the vector store in the function `__create_vector_storage` to your local path.

Run app locally:
```bash
python -m venv env
source env/bin/activate
pip3 install -r requirements.txt
streamlit run app.py
```

### Run with docker

The configuration is mounted into the container.  
You can change the configuration and reload rerun the streamlit app by pressing `r`.
```bash
docker build -t streamlit-app .
docker run --rm -p 8501:8501 -v $(pwd)/configuration.yaml:/app/configuration.yaml streamlit-app
```

Go to `http://localhost:8501`.

Alternatively you can mount the whole application and enable hot-reload.
Changes in the code will immediately take effect after pressing `r`.
```bash
docker build -t streamlit-app .
docker run --rm -p 8501:8501 -v $(pwd):/app streamlit-app
```
