import streamlit as st
import os
import base64
from io import BytesIO
from PIL import Image
from dotenv import load_dotenv
from stability_utils import StabilityAPI
import time

# Page configuration
st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🐝",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
def local_css():
    st.markdown("""
    <style>
        :root {
            --main-bg-color: #0f1117;
            --card-bg: #1a1c24;
            --text-color: #e0e0e0;
            --highlight-color: #6c63ff;
            --secondary-color: #4a4599;
            --input-bg: #272935;
            --error-color: #ff4757;
        }
        
        body {
            background-color: var(--main-bg-color) !important;
            color: var(--text-color);
        }
        
        .main {
            background-color: var(--main-bg-color);
            padding: 1rem;
        }
        
        .main-header {
            background: linear-gradient(90deg, #2d2b55, #4a4599);
            color: white;
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 2rem;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
        }
        
        .main-header h1 {
            margin: 0;
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .main-header p {
            margin-top: 0.5rem;
            font-size: 1.1rem;
            opacity: 0.9;
        }
        
        .content-card {
            background-color: var(--card-bg);
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            margin-bottom: 1.5rem;
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }

        .button-centered-wrapper {
            display: flex;
            align-items: center;
            justify-content: center;
            height: 60vh;
            width: 100%;
        }

        .center-button-container {
            display: flex;
            justify-content: center;
            margin: 1.5rem 0;
            width: 100%;
        }

        .center-button-container > div,
        .button-centered-wrapper > div {
            margin: 0 auto;
        }
        
        .center-button-container button,
        .button-centered-wrapper button {
            background: linear-gradient(90deg, #6c63ff, #4a4599) !important;
            color: white !important;
            padding: 0.6rem 1.5rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            cursor: pointer !important;
            transition: all 0.3s ease !important;
            min-width: 200px;
        }
        
        .center-button-container button:hover,
        .button-centered-wrapper button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3) !important;
        }
        
        .center-button-container button:disabled,
        .button-centered-wrapper button:disabled {
            opacity: 0.6 !important;
            cursor: not-allowed !important;
        }
        
        .loading-animation {
            animation: pulse 1.5s infinite;
            text-align: center;
            padding: 2rem;
        }
        
        .generated-image-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1rem;
            background-color: var(--card-bg);
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            max-width: 800px;
            margin-left: auto;
            margin-right: auto;
        }
        
        @keyframes pulse {
            0% { opacity: 0.6; }
            50% { opacity: 1; }
            100% { opacity: 0.6; }
        }
    </style>
    """, unsafe_allow_html=True)

local_css()

def loading_animation():
    placeholder = st.empty()
    loading_phrases = [
        "Analisando seu prompt...",
        "Criando conceitos visuais...",
        "Mesclando estilos e formas...", 
        "Refinando detalhes...",
        "Dando vida à sua ideia...",
        "Aplicando toques finais..."
    ]
    for i in range(6):
        with placeholder.container():
            st.markdown(f"""
            <div class="loading-animation">
                <h3>{loading_phrases[i % len(loading_phrases)]}</h3>
            </div>
            """, unsafe_allow_html=True)
        time.sleep(0.5)

# Initial setup
load_dotenv()
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY")

if not STABILITY_API_KEY:
    st.error("Chave da API não encontrada. Crie um arquivo `.env` com `STABILITY_API_KEY=sua_chave_aqui`")
    st.stop()

stability_api = StabilityAPI(STABILITY_API_KEY)

# UI Components
st.markdown("""
<div class="main-header">
    <h1>Gerador de Imagens AI</h1>
    <p>Transforme suas ideias em arte com a tecnologia da Stability AI</p>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="content-card center-text">', unsafe_allow_html=True)

st.markdown("""
<h3 style="color: #6c63ff; margin-bottom: 1rem; text-align: center;">Descreva sua imagem</h3>
""", unsafe_allow_html=True)

with st.expander("Dicas para prompts"):
    st.markdown("""
    **Exemplos de prompts eficazes:**
    - "Um dragão de cristal azul voando sobre uma cidade futurista ao pôr do sol, estilo digital art 4k"
    - "Retrato fotorrealista de um idoso sorrindo, iluminação cinematográfica, ultra detalhado"
    """)

st.markdown('<div class="text-container">', unsafe_allow_html=True)
prompt = st.text_area("", height=150, 
                    placeholder="Ex: Uma raposa samurai meditando em uma floresta de bambu ao luar...")
st.markdown('</div>', unsafe_allow_html=True)

with st.expander("Configurações avançadas"):
    steps = st.slider("Passos de geração", 10, 150, 30)
    cfg_scale = st.slider("Aderência ao prompt", 1, 20, 7)

# Centered Button
if 'generate_clicked' not in st.session_state:
    st.session_state.generate_clicked = False

col1, col2, col3 = st.columns([1,2,1])
with col2:
    generate_clicked = st.button("Gerar Imagem", key="generate_btn", disabled=not prompt, use_container_width=True)  

if generate_clicked:
    st.session_state.generate_clicked = True

st.markdown('</div>', unsafe_allow_html=True)

# Image Generation and Display
st.markdown('<div class="generated-image-container">', unsafe_allow_html=True)

if generate_clicked and prompt:
    loading_animation()
    
    try:
        model = "stable-diffusion-xl-1024-v1-0"
        width, height = 1024, 1024
        
        response = stability_api.generate_image(
            prompt=prompt,
            model=model,
            steps=steps,
            cfg_scale=cfg_scale,
            width=width,
            height=height
        )
        
        if response and isinstance(response, list):
            for img_data in response:
                if isinstance(img_data, dict) and 'base64' in img_data:
                    image_data = base64.b64decode(img_data['base64'])
                    image = Image.open(BytesIO(image_data))
                    
                    st.image(image, use_column_width=True)
                    
                    st.markdown(f"""
                    <div class="image-caption">
                        <p><strong>Prompt:</strong> {prompt}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    buf = BytesIO()
                    image.save(buf, format="PNG")
                    st.download_button(
                        label="⬇️ Baixar Imagem PNG",
                        data=buf.getvalue(),
                        file_name=f"ai_art_{int(time.time())}.png",
                        mime="image/png",
                        use_container_width=True
                    )
                else:
                    st.warning("Formato de resposta inesperado da API")
        else:
            st.error("Nenhuma imagem foi gerada. Verifique o prompt e tente novamente.")
            
    except Exception as e:
        st.error(f"Erro ao gerar imagem: {str(e)}")
else:
    st.markdown("""
    <div style="text-align: center; padding: 4rem 2rem;">
        <h3>Sua criação aparecerá aqui</h3>
        <p style="color: #a0a0a0;">
            Digite um prompt detalhado acima e clique em "Gerar Imagem"
        </p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; margin-top: 2rem; padding: 1rem; color: #a0a0a0; font-size: 0.8rem;">
    Desenvolvido Por @IannXz  - usando Streamlit e Stability AI
</div>
""", unsafe_allow_html=True)
