import os
import shutil

from textnode import TextNode, TextType
from blocks import markdown_to_html, extract_title

STATIC_PATH = "./static"
PUBLIC_PATH = "./public"
CONTENT_PATH = "./content"
TEMPLATE_PATH = "./template.html"

def move_static_files_to_public():
    if os.path.exists(STATIC_PATH):
        if os.path.exists(PUBLIC_PATH):
            shutil.rmtree(PUBLIC_PATH)
        os.mkdir(PUBLIC_PATH)
        move_static_files_to_public_r(STATIC_PATH)
    else:
        raise Exception("Static directory not found")

def move_static_files_to_public_r(total_path):
    for p in os.listdir(total_path):
        current_path = total_path + "/" + p
        mirror_path = PUBLIC_PATH + current_path.removeprefix(STATIC_PATH)
        if os.path.isfile(current_path):
            shutil.copy(current_path, mirror_path)
        elif os.path.isdir(current_path):
            os.mkdir(mirror_path)
            move_static_files_to_public_r(current_path)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as t:
        template = t.read()
    html_string = markdown_to_html(markdown).to_html()
    title = extract_title(markdown)
    html_file = template.replace(r"{{ Title }}", title)
    html_file = html_file.replace(r"{{ Content }}", html_string)
    
    try:
        os.makedirs(os.path.dirname(dest_path))
    except FileExistsError:
        pass
    with open(dest_path, 'w') as d:
        d.write(html_file)

def generate_pages(dir_path_content, template_path, dest_dir_path):
    if os.path.exists(dir_path_content):
        generate_pages_r(dir_path_content, dir_path_content, template_path, dest_dir_path)
    else:
        raise Exception(f"{dir_path_content} not found")

def generate_pages_r(dir_path_content, total_path, template_path, dest_dir_path):
    for p in os.listdir(total_path):
        current_path = total_path + "/" + p
        print("current: " + current_path)
        if os.path.isfile(current_path):
            if current_path.endswith(".md"):
                mirror_path = dest_dir_path + current_path.removeprefix(dir_path_content).removesuffix(".md") + ".html"
                print("mirror: " + mirror_path)
                generate_page(current_path, template_path, mirror_path)
        elif os.path.isdir(current_path):
            # os.mkdir(mirror_path)
            generate_pages_r(dir_path_content, current_path, template_path, dest_dir_path)



def main():
    move_static_files_to_public()
    generate_pages(CONTENT_PATH, TEMPLATE_PATH, PUBLIC_PATH)

main()

