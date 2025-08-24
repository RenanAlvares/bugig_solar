
# alterar para quando for fazer as imagens de edição do usuario


'''<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title>Perfil com Imagem Expandível</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      background-color: #f8f9fa;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }

    .perfil {
      text-align: center;
    }

    .foto-perfil {
      width: 100px;
      height: 100px;
      object-fit: cover;
      border-radius: 50%;
      border: 3px solid #007bff;
      cursor: pointer;
      transition: transform 0.3s ease;
    }

    /* Estilo do modal */
    .modal {
      display: none;
      position: fixed;
      z-index: 999;
      left: 0;
      top: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0,0,0,0.8);
      justify-content: center;
      align-items: center;
    }

    .modal img {
      max-width: 90%;
      max-height: 90%;
      border-radius: 10px;
    }
  </style>
</head>
<body>

  <div class="perfil">
    <img src="https://via.placeholder.com/150" alt="Foto de perfil" class="foto-perfil" onclick="expandirImagem(this)">
    <p>Editar Perfil</p>
  </div>

  <div class="modal" id="modalImagem" onclick="fecharModal()">
    <img id="imagemExpandida" src="" alt="Imagem expandida">
  </div>

  <script>
    function expandirImagem(img) {
      const modal = document.getElementById("modalImagem");
      const imagemExpandida = document.getElementById("imagemExpandida");
      imagemExpandida.src = img.src;
      modal.style.display = "flex";
    }

    function fecharModal() {
      document.getElementById("modalImagem").style.display = "none";
    }
  </script>

</body>
</html>
'''