"""
Minimal Reproducible Example (MRE) para el error en agnara-cli==0.1.0a8.

Este script demuestra que el framework falla al ser importado debido a un
SyntaxError en `agnara/capability/registry.py`.
"""
import sys
import traceback

def main():
    try:
        import agnara_cli
        print("Import successful!")
        sys.exit(0)
    except SyntaxError as e:
        print("¡Hallazgo confirmado! SyntaxError al importar agnara_cli.")
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"Otro error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
