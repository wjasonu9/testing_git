from pathlib import Path #os works too
folder = Path("images_folder")
for file in folder.glob("*.jpg"):
    file.rename(file.with_name("q" + file.name))
