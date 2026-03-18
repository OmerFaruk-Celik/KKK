#!/bin/bash

# Mevcut dizini al
INSTALL_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
SCRIPT_PATH="$INSTALL_DIR/kkk.py"

echo "🔧 Koduğum Kodunu Kurtar (KKK) kuruluyor..."

# Dosyaya çalışma izni ver
chmod +x "$SCRIPT_PATH"

# Hangi kabuk kullanılıyor? (.bashrc veya .zshrc)
if [[ $SHELL == *"zsh"* ]]; then
    CONF_FILE="$HOME/.zshrc"
elif [[ $SHELL == *"bash"* ]]; then
    CONF_FILE="$HOME/.bashrc"
else
    CONF_FILE="$HOME/.profile"
fi

# Alias zaten var mı kontrol et
if grep -q "alias kkk=" "$CONF_FILE"; then
    echo "⚠️  KKK zaten $CONF_FILE dosyasına eklenmiş."
else
    echo "" >> "$CONF_FILE"
    echo "# KKK - Kodugum Kodunu Kurtar Tool" >> "$CONF_FILE"
    echo "alias kkk='python3 \"$SCRIPT_PATH\"'" >> "$CONF_FILE"
    echo "✅ Alias $CONF_FILE dosyasına eklendi."
fi

echo "--------------------------------------------------"
echo "🎉 Kurulum tamamlandı!"
echo "🚀 Terminali yeniden başlatın veya şu komutu yazın: source $CONF_FILE"
echo "Artık istediğiniz klasörde 'kkk' yazarak kurtarma yapabilirsiniz."
