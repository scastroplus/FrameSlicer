import os
import shutil
import tempfile
import cv2
import streamlit as st

st.title("Extrator de quadros")
st.write("Envie seu vídeo MP4 para extrair todos os quadros e baixar em um ZIP.")

video_file = st.file_uploader("Escolha um vídeo", type=["mp4"])

if video_file is not None:
    if st.button("Gerar ZIP"):
        with st.spinner("Processando..."):
            with tempfile.TemporaryDirectory() as temp_dir:
                video_path = os.path.join(temp_dir, "input.mp4")
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