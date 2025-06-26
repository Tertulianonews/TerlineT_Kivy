#!/usr/bin/env python3
"""
Script de build automatizado para TerlineT Android
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(cmd):
    """Executa um comando e retorna True se bem-sucedido"""
    print(f"Executando: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Sucesso!")
        if result.stdout:
            print(result.stdout)
        return True
    else:
        print("❌ Erro!")
        if result.stderr:
            print(result.stderr)
        if result.stdout:
            print(result.stdout)
        return False


def check_requirements():
    """Verifica se os requisitos estão instalados"""
    print("🔍 Verificando requisitos...")

    # Verifica se buildozer está instalado
    if not shutil.which('buildozer'):
        print("❌ Buildozer não encontrado. Instalando...")
        if not run_command("pip install buildozer"):
            return False

    # Verifica se o arquivo buildozer.spec existe
    if not Path('buildozer.spec').exists():
        print("❌ buildozer.spec não encontrado!")
        return False

    print("✅ Requisitos verificados!")
    return True


def clean_build():
    """Limpa arquivos de build anteriores"""
    print("🧹 Limpando builds anteriores...")

    dirs_to_clean = ['.buildozer', 'bin']
    for directory in dirs_to_clean:
        if Path(directory).exists():
            print(f"Removendo {directory}/")
            shutil.rmtree(directory)

    print("✅ Limpeza concluída!")


def build_debug():
    """Constrói APK de debug"""
    print("🔨 Construindo APK de debug...")
    return run_command("buildozer android debug")


def build_release():
    """Constrói APK de release"""
    print("🔨 Construindo APK de release...")
    return run_command("buildozer android release")


def copy_apk():
    """Copia o APK para o diretório APK"""
    apk_dir = Path('APK')
    if apk_dir.exists():
        apk_files = list(apk_dir.glob('*.apk'))
        if apk_files:
            for apk in apk_files:
                print(f"✅ APK disponível: {apk}")
        else:
            print("❌ Nenhum APK encontrado na pasta APK!")
    else:
        print("❌ Diretório APK/ não encontrado!")

    # Também verifica a pasta bin (caso buildozer coloque lá)
    bin_dir = Path('bin')
    if bin_dir.exists():
        apk_files = list(bin_dir.glob('*.apk'))
        if apk_files:
            # Cria a pasta APK se não existir
            apk_dir.mkdir(exist_ok=True)
            for apk in apk_files:
                dest = apk_dir / apk.name
                shutil.copy2(apk, dest)
                print(f"✅ APK copiado para: {dest}")
        else:
            print("❌ Nenhum APK encontrado na pasta bin!")

    # Lista arquivos finais na pasta APK
    if apk_dir.exists():
        apk_files = list(apk_dir.glob('*.apk'))
        if apk_files:
            print(f"\n📱 APKs disponíveis em K:/FLUTTER/TerlineT_Kivy/APK/:")
            for apk in apk_files:
                size = apk.stat().st_size / (1024 * 1024)  # MB
                print(f"   {apk.name} ({size:.1f} MB)")
        else:
            print("\n❌ Nenhum APK final encontrado!")


def main():
    """Função principal"""
    print("🚀 TerlineT Android Builder")
    print("=" * 40)

    if not check_requirements():
        print("❌ Falha na verificação de requisitos!")
        sys.exit(1)

    # Menu de opções
    print("\nOpções de build:")
    print("1. Debug APK (desenvolvimento)")
    print("2. Release APK (produção)")
    print("3. Limpar e Debug")
    print("4. Limpar e Release")
    print("0. Sair")

    try:
        choice = input("\nEscolha uma opção (0-4): ").strip()
    except KeyboardInterrupt:
        print("\n\n👋 Build cancelado!")
        sys.exit(0)

    success = False

    if choice == "1":
        success = build_debug()
    elif choice == "2":
        success = build_release()
    elif choice == "3":
        clean_build()
        success = build_debug()
    elif choice == "4":
        clean_build()
        success = build_release()
    elif choice == "0":
        print("👋 Até logo!")
        sys.exit(0)
    else:
        print("❌ Opção inválida!")
        sys.exit(1)

    if success:
        copy_apk()
        print("\n🎉 Build concluído com sucesso!")
        print("📱 Instale o APK no seu dispositivo Android!")
    else:
        print("\n❌ Build falhou!")
        print("💡 Verifique os logs acima para mais detalhes.")
        sys.exit(1)


if __name__ == "__main__":
    main()
