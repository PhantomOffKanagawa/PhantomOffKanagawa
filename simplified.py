from turtle import back
from PIL import Image, ImageDraw, ImageFont
import requests
from typing import List, Tuple
import time

# Hardcoded configuration
USERNAME = "PhantomOffKanagawa"
FONT_PATH = "./JetBrainsMonoNerdFont-Regular.ttf"
FONT_SIZE = 16
LINE_SPACING = 6
PADDING = 20

# Colors (Dark+ Theme)
COLORS = {
    "foreground": "#cccccc",
    "background": "#1e1e1e",
    "cursorColor": "#cccccc",
    "black": "#000000",
    "red": "#c62f37",
    "green": "#37be78",
    "yellow": "#e2e822",
    "blue": "#396ec7",
    "purple": "#b835bc",
    "cyan": "#3ba7cc",
    "white": "#e5e5e5",
    "brightBlack": "#666666",
    "brightRed": "#e94a51",
    "brightGreen": "#45d38a",
    "brightYellow": "#f2f84a",
    "brightBlue": "#4e8ae9",
    "brightPurple": "#d26ad6",
    "brightCyan": "#49b7da",
    "brightWhite": "#e5e5e5"
}

COLOR_MAP = {
    "prompt": COLORS['green'],
    "command": COLORS['blue'],
    "ascii": COLORS['brightBlack'],
    "info_label": COLORS['cyan'],
    "info_value": COLORS['white'],
    "info_header": COLORS['green'],
}

COLOR_BLOCKS = [["black", "red", "green", "yellow", "blue", "purple", "cyan", "white"],
                ["brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightPurple", "brightCyan", "brightWhite"]]

# ASCII art (Merlin with color codes)
ASCII_ART = [
        "            @@@%%%%%%%%%@@           ",
        "         @@@%%%%%%%%%#######%@@      ",
        "       @@@@%%%%%%%######?######%@    ",
        "      @@@@%%%%%%%#######:########%@  ",
        "    @@@@@%%%%%%#########:??#######%  ",
        "    @@@%%%%%####???###?+:??####?###@ ",
        "   @@@%%%%%%#?+???###?:+?##??###?##@ ",
        " @??%@%%%##????????++:;+?+????????#@ ",
        " #  ;?%#?+; ..::+?+ ::;++++++?+???#  ",
        " %  :?%;;;:  ....:#+ :;+++????+???@  ",
        " #;;+??+++:   ...;##: ;;;++???++?%   ",
        " %#%+::++?#+;:::;?##+ ;;;;++??++#    ",
        " %?% : :???+?++???######?+;;+??#     ",
        " @%# ; ;??;;+ ;???+;;:..::.:+?%      ",
        "  @???;;?+;;;+ ;:;;......;;;#@       ",
        "  %##?++?+++;+ ??% @%%@@@@           ",
        "  @_:?_:+_:_:#%                      "
    ]

def get_github_info():
    """Fetch basic GitHub stats or return hardcoded values"""
    try:
        response = requests.get(f"https://api.github.com/users/{USERNAME}")
        data = response.json()
        return {
            'login': data.get('login', USERNAME),
            'name': data.get('name', 'Harrison Surma'),
            'bio': data.get('bio', 'Developer'),
            'blog': data.get('blog', 'Unknown'),
            'followers': str(data.get('followers', 0)),
            'following': str(data.get('following', 0)),
            'repos': str(data.get('public_repos', 0)),
            'gists': str(data.get('public_gists', 0)),
            'location': data.get('location', 'Unknown')
        }
    except:
        return {
            'login': USERNAME,
            'name': 'Harrison Surma',
            'bio': 'Mizzou Senior Computer Science Student',
            'blog': 'harrison.surma.family',
            'followers': '2',
            'following': '4',
            'repos': '32',
            'gists': '5',
            'location': 'None'
        }

def measure_ascii_art(art: List[str], font: ImageFont.FreeTypeFont) -> Tuple[int, int]:
    """Measure the width and height of ASCII art."""
    max_width = int(max(font.getlength(line) for line in art))
    total_height = len(art) * (FONT_SIZE + 2)
    return max_width, total_height

def create_terminal_image(include_cursor: bool = False):
    """Create the terminal-style image with optional cursor"""
    # Initialize font
    font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
    
    # Get info first to calculate dimensions
    info = get_github_info()
    
    # Calculate ASCII art dimensions
    ascii_width, ascii_height = measure_ascii_art(ASCII_ART, font)
    
    # Prepare info items
    info_items = [
        ("Name:", str(info['name'])),
        ("Bio:", str(info['bio'])),
        ("Blog: ", str(info['blog'])),
        ("Languages:", "Typescript, Python, Java, C"),
        ("Skills:", "Communication, Problem Solving, Goal Oriented"),
        ("Repos:", str(info['repos'])),
        ("Gists:", str(info['gists'])),
        ("Followers:", str(info['followers'])),
        ("Following:", str(info['following'])),
    ]
    
    # Calculate maximum label width
    max_label_width = int(max(font.getlength(label) for label, _ in info_items))
      # Calculate info section width by considering wrapped lines
    # First calculate the available width we'd have
    initial_width = int(max_label_width + max(
        font.getlength(value) for _, value in info_items
    ) + 50)  # Start with basic width
    
    # Now check if any wrapped lines would need more space
    max_content_width = 0
    test_wrap_width = initial_width - int(max_label_width + 20)  # Space after label
    
    for _, value in info_items:
        # Split on newlines first
        lines = [(font.getlength(line), line) for line in value.split('\n')]
        # Get the width needed for the widest line
        if lines:
            max_line_width = max(width for width, _ in lines)
            max_content_width = max(max_content_width, max_line_width)
    
    # Calculate final section width needed
    info_section_width = int(max_label_width + max_content_width + 30)  # Add some padding
    
    # Calculate prompt width for cursor positioning
    prompt = f"{USERNAME}@github:~$ "
    prompt_width = int(font.getlength(prompt))
    
    # Calculate required width and height
    total_width = int(PADDING * 3 + ascii_width + info_section_width)
    command_height = int((FONT_SIZE + LINE_SPACING) * 4 + LINE_SPACING * 2)  # Added space for new prompt
    info_height = int((FONT_SIZE + LINE_SPACING) * (len(info_items) + 3))  # +3 for header and spacing
    total_height = int(PADDING * 2 + max(command_height + ascii_height, command_height + info_height) + 40)
    
    # Create image with calculated dimensions
    img = Image.new("RGB", (total_width, total_height), COLORS['background'])
    draw = ImageDraw.Draw(img)
    
    # Start position
    y = PADDING
    x = PADDING
      # Draw command history
    commands = [
        [(f"{USERNAME}@github:~$", COLOR_MAP['prompt']), (" whoami", COLOR_MAP['command'])],
        [("Harrison Surma", COLOR_MAP['info_value'])],
        [(f"{USERNAME}@github:~$", COLOR_MAP['prompt']), (" neofetch", COLOR_MAP['command'])],
    ]
    
    for command_segments in commands:
        x_pos = x
        for text, color in command_segments:
            draw.text((x_pos, y), text, font=font, fill=color)
            x_pos += font.getlength(text)
        y += FONT_SIZE + LINE_SPACING
    
    y += LINE_SPACING * 2
    start_y = y
    
    # Draw ASCII art
    ascii_start_y = start_y
    y = start_y
    for line in ASCII_ART:
        x_pos = PADDING
        content = line.replace("${c1}", "")
        draw.text((x_pos, y), content, font=font, fill=COLOR_MAP['ascii'])
        y += FONT_SIZE + 2
    
    # Draw info section
    y = start_y  # Reset y to start_y for info section
    info_x = PADDING * 2 + ascii_width
    
    # Header
    draw.text((info_x, y), f"{info['login']}@github", font=font, fill=COLOR_MAP['info_header'])
    y += FONT_SIZE + LINE_SPACING
    draw.text((info_x, y), "-" * 20, font=font, fill=COLOR_MAP['info_header'])
    y += FONT_SIZE + LINE_SPACING
      # Draw info items with proper alignment and text wrapping
    for label, value in info_items:
        initial_y = y  # Store initial y position
        # Draw label
        draw.text((info_x, y), label, font=font, fill=COLOR_MAP['info_label'])

        # Split value on actual newlines first
        value_parts = value.split('\n')
        max_lines = 0
        
        # Handle each part separately for wrapping
        for part_idx, part in enumerate(value_parts):
            # Only add extra spacing between paragraphs, not between wrapped lines
            # if part_idx > 0:
            #     y += FONT_SIZE
            
            # Draw the text directly without wrapping
            line_y = y
            lines = [part]  # Create lines list with the current part
            if part.strip():
                draw.text((info_x + max_label_width + 10, line_y), part, 
                    font=font, fill=COLOR_MAP['info_value'])
                
            # Update y position for this part
            if lines:
                y = y + (FONT_SIZE + LINE_SPACING) * len(lines)
        
        # Add spacing after the entire value section
        # y += LINE_SPACING
      # Color blocks
    y += FONT_SIZE + LINE_SPACING * 2
    x = info_x
    
    x_size = font.getlength("███")
    x_space = font.getlength("")
    for i, color_row in enumerate(COLOR_BLOCKS):
        for j, color in enumerate(color_row):
            block_color = COLORS[color]
            draw.rectangle([x, y, x + x_size, y + FONT_SIZE + LINE_SPACING], fill=block_color)
            x += x_size + x_space
        y += FONT_SIZE + LINE_SPACING
        x = info_x
    # for color in :
    #     draw.text((x, y), "●", font=font, fill=color)
    #     x += font.getlength("● ")
        
    y = max(ascii_start_y + ascii_height, y)  # Ensure y is below ASCII art
    
    # Add final prompt at the bottom of all content
    y += FONT_SIZE + LINE_SPACING
    x = PADDING
    if include_cursor:
        draw.text((x, y), prompt, font=font, fill=COLOR_MAP['prompt'])
        draw.text((x + prompt_width, y), "█", font=font, fill=COLORS['cursorColor'])
    else:
        draw.text((x, y), prompt, font=font, fill=COLOR_MAP['prompt'])

    return img

def create_terminal_gif():
    """Create an animated GIF with a blinking cursor"""
    frames = []
    
    # Create frames with and without cursor
    frames.append(create_terminal_image(include_cursor=True))
    frames.append(create_terminal_image(include_cursor=False))
    
    # Save as animated GIF
    frames[0].save(
        "terminal.gif",
        save_all=True,
        append_images=[frames[1]],
        duration=500,  # 500ms per frame
        loop=0
    )

if __name__ == "__main__":
    # Create and save the static image
    img = create_terminal_image()
    img.save("terminal.png")
    print("Generated terminal.png")
    
    # Create animated version
    create_terminal_gif()
    print("Generated terminal.gif")