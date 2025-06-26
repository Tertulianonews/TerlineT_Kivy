#!/usr/bin/env python3
"""
Script para configurar o ambiente Android no Windows
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path


def print_header(title):
    print(f"\n{'=' * 50}")
    print(f"🔧 {title}")
    print(f"{'=' * 50}")


def run_command(cmd):
    """Executa um comando e retorna True se bem-sucedido"""
    print(f"Executando: {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def check_java():
    """Verifica se Java está instalado"""
    print_header("Verificando Java")

    try:
        result = subprocess.run(['java', '-version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Java encontrado!")
            print(result.stderr)  # Java version vai para stderr
            return True
        else:
            print("❌ Java não encontrado!")
            return False
    except FileNotFoundError:
        print("❌ Java não encontrado!")
        return False


def install_java():
    """Instruções para instalar Java"""
    print_header("Instalação do Java")
    print("🔗 Baixe e instale o OpenJDK 11:")
    print("   https://adoptium.net/temurin/releases/")
    print("\n📋 Após a instalação:")
    print("   1. Adicione JAVA_HOME às variáveis de ambiente")
    print("   2. Adicione %JAVA_HOME%\\bin ao PATH")
    print("   3. Reinicie o terminal")


def check_android_sdk():
    """Verifica se Android SDK está instalado"""
    print_header("Verificando Android SDK")

    android_home = os.environ.get('ANDROID_HOME')
    if android_home and Path(android_home).exists():
        print(f"✅ Android SDK encontrado em: {android_home}")
        return True
    else:
        print("❌ Android SDK não encontrado!")
        return False


def install_android_sdk():
    """Instruções para instalar Android SDK"""
    print_header("Instalação do Android SDK")
    print("🔗 Opção 1 - Android Studio (Recomendado):")
    print("   https://developer.android.com/studio")
    print("\n🔗 Opção 2 - Command Line Tools:")
    print("   https://developer.android.com/studio#cmdline-tools")
    print("\n📋 Após a instalação:")
    print("   1. Configure ANDROID_HOME apontando para o SDK")
    print("   2. Adicione os seguintes ao PATH:")
    print("      - %ANDROID_HOME%\\platform-tools")
    print("      - %ANDROID_HOME%\\tools")
    print("      - %ANDROID_HOME%\\build-tools\\33.0.0")


def check_git():
    """Verifica se Git está instalado"""
    print_header("Verificando Git")

    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Git encontrado!")
            print(result.stdout.strip())
            return True
        else:
            print("❌ Git não encontrado!")
            return False
    except FileNotFoundError:
        print("❌ Git não encontrado!")
        return False


def install_git():
    """Instruções para instalar Git"""
    print_header("Instalação do Git")
    print("🔗 Baixe e instale o Git:")
    print("   https://git-scm.com/download/win")


def check_python_packages():
    """Verifica se os pacotes Python necessários estão instalados"""
    print_header("Verificando Pacotes Python")

    packages = ['buildozer', 'kivy', 'llama-cpp-python']
    missing = []

    for package in packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} instalado")
        except ImportError:
            print(f"❌ {package} não encontrado")
            missing.append(package)

    return len(missing) == 0, missing


def install_python_packages(missing_packages):
    """Instala os pacotes Python necessários"""
    print_header("Instalando Pacotes Python")

    for package in missing_packages:
        print(f"Instalando {package}...")
        if run_command(f"pip install {package}"):
            print(f"✅ {package} instalado com sucesso!")
        else:
            print(f"❌ Falha ao instalar {package}")


def show_environment_setup():
    """Mostra como configurar as variáveis de ambiente"""
    print_header("Configuração de Variáveis de Ambiente")

    print("🔧 Configure estas variáveis no Windows:")
    print("\n1. Abra 'Configurações do Sistema' → 'Variáveis de Ambiente'")
    print("\n2. Adicione/edite as seguintes variáveis:")
    print("   JAVA_HOME=C:\\Program Files\\Eclipse Adoptium\\jdk-11.x.x-hotspot")
    print("   ANDROID_HOME=C:\\Users\\%USERNAME%\\AppData\\Local\\Android\\Sdk")
    print("   NDK_HOME=%ANDROID_HOME%\\ndk\\25.1.8937393")
    print("\n3. Adicione ao PATH:")
    print("   %JAVA_HOME%\\bin")
    print("   %ANDROID_HOME%\\platform-tools")
    print("   %ANDROID_HOME%\\tools")
    print("   %ANDROID_HOME%\\build-tools\\33.0.0")
    print("\n4. Reinicie o terminal após as alterações")


def check_adb():
    """Verifica se ADB está funcionando"""
    print_header("Verificando ADB")

    try:
        result = subprocess.run(['adb', 'version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ ADB funcionando!")
            print(result.stdout.strip())
            return True
        else:
            print("❌ ADB não está funcionando!")
            return False
    except FileNotFoundError:
        print("❌ ADB não encontrado!")
        return False


def main():
    """Função principal"""
    print("🚀 Configurador do Ambiente Android para TerlineT")
    print("=" * 60)

    # Verificações
    java_ok = check_java()
    android_ok = check_android_sdk()
    git_ok = check_git()
    adb_ok = check_adb()
    python_ok, missing_packages = check_python_packages()

    # Resumo
    print_header("Resumo")
    print(f"Java JDK:      {'✅' if java_ok else '❌'}")
    print(f"Android SDK:   {'✅' if android_ok else '❌'}")
    print(f"Git:           {'✅' if git_ok else '❌'}")
    print(f"ADB:           {'✅' if adb_ok else '❌'}")
    print(f"Pacotes Python: {'✅' if python_ok else '❌'}")

    # Instalar pacotes Python faltantes
    if not python_ok:
        install_python_packages(missing_packages)

    # Instruções para componentes faltantes
    if not java_ok:
        install_java()

    if not android_ok:
        install_android_sdk()

    if not git_ok:
        install_git()

    # Mostrar configuração de ambiente
    if not (java_ok and android_ok and adb_ok):
        show_environment_setup()

    # Próximos passos
    print_header("Próximos Passos")
    if java_ok and android_ok and git_ok and python_ok and adb_ok:
        print("🎉 Ambiente configurado com sucesso!")
        print("📱 Agora você pode executar:")
        print("   python build_android.py")
    else:
        print("⚠️  Configure os componentes faltantes e execute este script novamente")
        print("📋 Após configurar tudo, teste com:")
        print("   python setup_android_env.py")


if __name__ == "__main__":
    main()
