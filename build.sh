#!/bin/bash

# Para a execução se algum comando falhar
set -e

APP_NAME="cnh-simulated"
VERSION="1.0.0"
MAINTAINER="username <email@gmail.com>"
ARCH="amd64"

echo "🧹 1. Limpando builds anteriores..."
rm -rf build dist "${APP_NAME}_${VERSION}_${ARCH}" "${APP_NAME}_${VERSION}_${ARCH}.deb"

echo "📦 2. Instalando o PyInstaller via uv..."
uv pip install pyinstaller

echo "⚙️ 3. Construindo o executável com PyInstaller..."
# Empacota o programa e inclui os diretórios assets e json.
# O PyInstaller detecta o código python automaticamente.
uv run pyinstaller --name "${APP_NAME}" \
    --windowed \
    --noconfirm \
    --add-data "assets:assets" \
    --add-data "json:json" \
    main.py

echo "📁 4. Criando a estrutura do pacote Debian (.deb)..."
DEB_DIR="${APP_NAME}_${VERSION}_${ARCH}"

mkdir -p "${DEB_DIR}/DEBIAN"
mkdir -p "${DEB_DIR}/opt/${APP_NAME}"
mkdir -p "${DEB_DIR}/usr/share/applications"
mkdir -p "${DEB_DIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${DEB_DIR}/usr/bin"

echo "📝 5. Criando o arquivo control..."
cat <<EOF > "${DEB_DIR}/DEBIAN/control"
Package: ${APP_NAME}
Version: ${VERSION}
Architecture: ${ARCH}
Maintainer: ${MAINTAINER}
Description: CNH Simulated - Preparatório para a Prova Teórica
 Um aplicativo desktop moderno para preparação para o exame teórico da CNH (DETRAN).
 Suporta simulações offline com banco local e geração de novas questões usando Inteligência Artificial (Google Gemini).
EOF

echo "🖥️ 6. Criando o atalho (.desktop)..."
cat <<EOF > "${DEB_DIR}/usr/share/applications/${APP_NAME}.desktop"
[Desktop Entry]
Name=CNH Simulated
Comment=Estude para a CNH com banco local ou IA
Exec=/opt/${APP_NAME}/${APP_NAME}
Icon=${APP_NAME}
Terminal=false
Type=Application
Categories=Education;
EOF

echo "📋 7. Copiando os arquivos para a estrutura..."
# Copia o diretório buildado pelo pyinstaller para /opt/
cp -r dist/${APP_NAME}/* "${DEB_DIR}/opt/${APP_NAME}/"

# Cria um link simbólico relativo na pasta /usr/bin/ para chamar no terminal
ln -s ../../opt/${APP_NAME}/${APP_NAME} "${DEB_DIR}/usr/bin/${APP_NAME}"

# Copia o ícone SVG para o diretório de ícones do sistema
cp assets/car-icon.svg "${DEB_DIR}/usr/share/icons/hicolor/scalable/apps/${APP_NAME}.svg"

echo "🛠️ 8. Construindo o pacote final (.deb)..."
dpkg-deb --build "${DEB_DIR}"

echo "✅ Concluído com Sucesso! Seu pacote gerado é: ${APP_NAME}_${VERSION}_${ARCH}.deb"
