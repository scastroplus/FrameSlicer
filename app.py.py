import os
import shutil
import tempfile
import cv2
import streamlit as st

# Configurando o título da aba do navegador
st.set_page_config(page_title="Frame Slicer", page_icon="✂️")

# Injetando a "roupa" (CSS) para criar o efeito Glassmorphism
st.markdown("""
<style>
    /* Criando um fundo colorido suave para destacar o efeito de vidro */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Aplicando o visual de vidro fosco no bloco principal */
    .block-container {
        background: rgba(255, 255, 255, 0.35);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.2);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.4);
        padding: 3rem !important;
        margin-top: 3rem;
        margin-bottom: 3rem;
    }

    /* Garantindo que os textos fiquem escuros e legíveis */
    h1, p, .stMarkdown {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

# Novos textos solicitados
st.title("✂️ Frame Slicer 🎥")
st.write("Envie seu vídeo para extrair todos os quadros e baixe as imagens")

# Lista de formatos ampliada
video_file = st.file_uploader("Escolha um vídeo", type=["mp4", "mov", "avi", "mkv", "webm"])

if video_file is not None:
    if st.button("Gerar ZIP"):
        with st.spinner("Processando..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                # Mantendo a extensão original (ex: .mkv, .mov)
                extensao = os.path.splitext(video_file.name)[1]
                video_path = os.path.join(temp_dir, f"input{extensao}")
                
                with open(video_path, "wb") as f:
                    f.write(video_file.read())

                pasta_imagens = os.path.join(temp_dir, "quadros")
                os.makedirs(pasta_imagens, exist_ok=True)

                video = cv2.VideoCapture(video_path)
                contador = 0
                sucesso = True

                while sucesso:
                    sucesso, imagem = video.read()
                    if sucesso:
                        cv2.imwrite(os.path.join(pasta_imagens, f"quadro_{contador:04d}.jpg"), imagem)
                        contador += 1
                video.release()

                zip_path = os.path.join(temp_dir, "imagens")
                shutil.make_archive(zip_path, "zip", pasta_imagens)

                with open(f"{zip_path}.zip", "rb") as fp:
                    st.success("Pronto!")
                    st.download_button("Baixar ZIP", data=fp, file_name="quadros.zip", mime="application/zip")
