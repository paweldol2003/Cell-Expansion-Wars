#image_coder.py
import base64
import os

def generate_image_py(input_folder, output_py):
    with open(output_py, "w") as f:
        f.write("import base64\n")
        f.write("import pygame\n")
        f.write("import io\n\n")
        f.write("def load_images():\n")
        f.write("    images = {}\n\n")

        for filename in os.listdir(input_folder):
            if filename.lower().endswith(".png"):
                # Zamień np. cell_player_standard.png -> ID_UNIT_PLAYER_STANDARD
                name = os.path.splitext(filename)[0].upper()  # CELL_PLAYER_STANDARD
                if name.startswith("CELL_"):
                    name = name.replace("CELL_", "")
                key = f"ID_UNIT_{name}"

                path = os.path.join(input_folder, filename)

                with open(path, "rb") as image_file:
                    encoded = base64.b64encode(image_file.read()).decode("utf-8")

                f.write(f"    images[\"{key}\"] = pygame.image.load(io.BytesIO(base64.b64decode(\"" + encoded + "\"))).convert_alpha()\n")

        f.write("\n    return images\n")

    print(f"Wygenerowano plik: {output_py}")

# Przykład użycia:
generate_image_py("assets", "assets/resources.py")
