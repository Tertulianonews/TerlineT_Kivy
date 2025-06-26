# TerlineT Android - Guia de Build

## 📋 Pré-requisitos

### Windows (seu sistema atual)

1. **Python 3.8+** já instalado ✅
2. **Java JDK 8 ou 11**
   ```powershell
   # Baixe e instale o OpenJDK 11
   # https://adoptium.net/temurin/releases/
   ```

3. **Android SDK** (via Android Studio ou command line tools)
   ```powershell
   # Baixe Android Studio: https://developer.android.com/studio
   # Ou apenas as command line tools
   ```

4. **Git** (se não tiver)
   ```powershell
   # Baixe em: https://git-scm.com/download/win
   ```

### Variáveis de Ambiente

Configure estas variáveis no Windows:

```powershell
# Adicione ao PATH do sistema:
JAVA_HOME=C:\Program Files\Eclipse Adoptium\jdk-11.0.x-hotspot
ANDROID_HOME=C:\Users\%USERNAME%\AppData\Local\Android\Sdk
NDK_HOME=%ANDROID_HOME%\ndk\25.1.8937393

# PATH deve incluir:
%JAVA_HOME%\bin
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\tools
%ANDROID_HOME%\build-tools\33.0.0
```

## 🚀 Build Automático

### Método 1: Script Python (Recomendado)

```powershell
# Execute o script de build
python build_android.py
```

### Método 2: Comandos Manuais

```powershell
# Build de debug (desenvolvimento)
buildozer android debug

# Build de release (produção)
buildozer android release

# Limpar cache e rebuild
buildozer android clean
buildozer android debug
```

## 📱 Instalação no Android

### Via USB (Recomendado)

1. Habilite **Opções do Desenvolvedor** no Android
2. Ative **Depuração USB**
3. Conecte o dispositivo via USB
4. Execute:
   ```powershell
   # Instalar APK via ADB
   adb install bin/terlinet-1.0.0-arm64-v8a-debug.apk
   ```

### Via Arquivo APK

1. Copie o APK para o dispositivo
2. Habilite **Fontes Desconhecidas** nas configurações
3. Abra o arquivo APK no dispositivo
4. Siga as instruções de instalação

## 🔧 Configuração do Modelo GGUF no Android

### Caminho do Modelo

No Android, coloque o modelo em:

```
/storage/emulated/0/TerlineT/modelo/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf
```

### Como Copiar o Modelo

1. **Via USB:**
   ```powershell
   adb push "K:/FLUTTER/TerlineT_Kivy/modelo/DeepSeek-R1-0528-Qwen3-8B-Q4_K_M.gguf" "/storage/emulated/0/TerlineT/modelo/"
   ```

2. **Via Aplicativo de Arquivos:**
    - Copie o arquivo .gguf para o Android
    - Crie a pasta `TerlineT/modelo/` no storage interno
    - Mova o arquivo para lá

## 🐛 Solução de Problemas

### Erro: "Command failed: gradlew"

```powershell
# Limpe o cache e tente novamente
buildozer android clean
# Certifique-se de que as variáveis de ambiente estão corretas
```

### Erro: "SDK não encontrado"

```powershell
# Instale o Android SDK via Android Studio
# Configure ANDROID_HOME corretamente
# Instale build-tools versão 33.0.0
```

### Erro: "NDK não encontrado"

```powershell
# Abra Android Studio -> SDK Manager -> SDK Tools
# Instale NDK (versão 23.x)
# Configure NDK_HOME
```

### Erro: "Java não encontrado"

```powershell
# Instale OpenJDK 11
# Configure JAVA_HOME
# Adicione %JAVA_HOME%\bin ao PATH
```

### App não inicia no Android

- Verifique se o modelo GGUF está no caminho correto
- O app funcionará em modo simulado sem o modelo
- Verifique os logs: `adb logcat | findstr python`

## 📊 Arquivos Gerados

Após o build bem-sucedido, você terá:

```
bin/
├── terlinet-1.0.0-arm64-v8a-debug.apk     # APK de debug
└── terlinet-1.0.0-arm64-v8a-release.apk   # APK de release (se assinado)
```

## 🎯 Diferenças Desktop vs Android

| Recurso | Desktop | Android |
|---------|---------|---------|
| Modelo GGUF | ✅ Suportado | ✅ Suportado |
| Interface | Otimizada para desktop | Otimizada para touch |
| Performance | Máxima | Otimizada para mobile |
| Reconhecimento de voz | Simulado | Simulado |
| Síntese de voz | Simulado | Simulado |

## 📝 Notas Importantes

1. **Primeira execução:** O build inicial pode demorar 30-60 minutos
2. **Tamanho do APK:** ~50-100MB dependendo das dependências
3. **Compatibilidade:** Android 5.0+ (API 21+)
4. **Arquitetura:** arm64-v8a (dispositivos modernos)
5. **Permissões:** O app solicita automaticamente as permissões necessárias

## 🔄 Atualizações

Para atualizar o app:

1. Incremente a versão no `buildozer.spec`
2. Execute novo build
3. Desinstale a versão antiga (se necessário)
4. Instale a nova versão

## 📞 Suporte

Em caso de problemas:

1. Verifique os logs de build
2. Consulte a documentação do Buildozer
3. Verifique se todas as dependências estão instaladas
4. Tente um build limpo (`buildozer android clean`)

---

**🎉 Boa sorte com o seu app TerlineT no Android!** 📱