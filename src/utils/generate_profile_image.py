import base64
import random
from typing import Dict, Tuple


def get_color_palette() -> Dict[str, str]:
    """
    Define uma paleta de cores para o fundo do avatar.
    Você pode expandir esta lista.
    """
    return {
        # Tons de Azul
        'blue': '#3b82f6',  # Azul Google/Tailwind
        'indigo': '#6366f1',  # Índigo
        'sky': '#0ea5e9',  # Azul Celeste
        # Tons de Verde/Amarelo
        'green': '#10b981',  # Verde Esmeralda
        'yellow': '#f59e0b',  # Amarelo Âmbar
        # Tons de Vermelho/Roxo
        'red': '#ef4444',  # Vermelho Padrão
        'purple': '#8b5cf6',  # Roxo Violeta
    }


def generate_svg_avatar(initial: str, background_color_hex: str) -> str:
    """
    Gera o conteúdo SVG (XML) de um avatar circular com uma inicial.

    Args:
        initial (str): A inicial do nome (deve ser uma única letra).
        background_color_hex (str): A cor de fundo em formato hexadecimal (ex: "#3b82f6").

    Returns:
        str: O conteúdo SVG completo como uma string.
    """
    # Garante que a inicial seja maiúscula e tratada
    display_initial = initial.upper().strip()[:1]

    # Define as dimensões do SVG
    size = 100

    # O conteúdo SVG é uma string XML.
    # Usamos f-string para injetar a cor e a inicial.
    svg_content = f"""
<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
    <!-- Fundo Circular -->
    <rect width="{size}" height="{size}" fill="{background_color_hex}" rx="50" ry="50"/>

    <!-- Texto da Inicial -->
    <text
        x="50%"
        y="50%"
        dominant-baseline="middle"
        text-anchor="middle"
        font-family="Arial, sans-serif"
        font-size="{size * 0.5}"
        fill="#FFFFFF"
        font-weight="600"
    >
        {display_initial}
    </text>
</svg>
    """
    return svg_content.strip()


def create_user_avatar(name: str) -> Tuple[str, str]:
    """
    Função principal para gerar o avatar, escolhendo a inicial e a cor.

    Args:
        name (str): O nome completo do usuário.

    Returns:
        Tuple[str, str]: Uma tupla contendo (svg_content, background_color_hex).
    """
    if not name:
        # Se o nome estiver vazio, usa uma inicial padrão ou lida com erro
        initial = '?'
    else:
        # Pega a primeira letra do primeiro nome
        initial = name.strip()[0]

    # Escolhe uma cor aleatória da paleta
    palette = get_color_palette()
    random_color_hex = random.choice(list(palette.values()))

    # Gera o SVG
    svg_code = generate_svg_avatar(initial, random_color_hex)

    return svg_code, random_color_hex
