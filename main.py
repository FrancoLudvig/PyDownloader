import customtkinter as ctk
from pytube import YouTube
import yt_dlp
import tkinter.filedialog as filedialog
import os
import re

# Função para baixar do YouTube usando pytube
def baixar_video_youtube(url, resolution, save_path):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(res=resolution).first()
        if not stream:
            stream = yt.streams.get_highest_resolution()  # Resolução mais alta disponível
        stream.download(output_path=save_path)
        print("Download do vídeo do YouTube concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar do YouTube: {e}")

# Função para baixar do Xvideos e RedTube usando yt-dlp
def baixar_video_yt_dlp(url, save_path):
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s')
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download do vídeo concluído com sucesso!")
    except Exception as e:
        print(f"Erro ao baixar: {e}")

# Função principal que chama o downloader correto baseado na URL
def iniciar_download():
    url = url_entry.get()
    resolution = resolution_var.get()
    save_path = filedialog.askdirectory(title="Escolha o local de salvamento")

    if not save_path:
        print("Local de salvamento não foi selecionado!")
        return

    if re.search(r'youtube\.com|youtu\.be', url):
        baixar_video_youtube(url, resolution, save_path)
    elif re.search(r'xvideos\.com|redtube\.com', url):
        baixar_video_yt_dlp(url, save_path)
    else:
        print("Plataforma não suportada!")

# Configuração da interface gráfica com CustomTkinter
def criar_janela():
    ctk.set_appearance_mode("dark")
    janela = ctk.CTk()
    janela.geometry("800x600")
    janela.title("ResTube Downloader")

    # Título
    title_label = ctk.CTkLabel(janela, text="ResTube Downloader", font=("Arial", 24))
    title_label.pack(pady=20)

    # Entrada de URL
    url_label = ctk.CTkLabel(janela, text="URL do Vídeo:")
    url_label.pack(pady=(10, 0))
    global url_entry
    url_entry = ctk.CTkEntry(janela, width=600)
    url_entry.pack(pady=10)

    # Menu Dropdown de Resolução
    global resolution_var
    resolution_var = ctk.StringVar(value="720p")
    resolution_label = ctk.CTkLabel(janela, text="Resolução:")
    resolution_label.pack(pady=(10, 0))
    resolution_menu = ctk.CTkOptionMenu(janela, variable=resolution_var, values=["144p", "360p", "480p", "720p", "1080p"])
    resolution_menu.pack(pady=10)

    # Botão de download
    download_button = ctk.CTkButton(janela, text="Iniciar Download", command=iniciar_download)
    download_button.pack(pady=20)

    janela.mainloop()

# Executa a janela
criar_janela()
