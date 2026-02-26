import os
import shutil

from markdown_blocks import markdown_to_html_node
from textnode import TextNode, TextType


def copy_content(source, target, clean=False):
    if clean and os.path.exists(target):
        shutil.rmtree(target)
    if not os.path.exists(target):
        os.mkdir(target)
    for elem in os.listdir(source):
        src_path = os.path.join(source, elem)
        dst_path = os.path.join(target, elem)
        if os.path.isfile(src_path):
            shutil.copy(src_path, dst_path)
        else:
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            copy_content(src_path, dst_path, clean=False)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line[0] == "#" and line[1] != "#":
            return line.split(" ", 1)[1]
    raise Exception("no title found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    md = open(from_path)
    md_content = md.read()
    md.close()
    tp = open(template_path)
    tp_content = tp.read()
    tp.close()
    html_string = markdown_to_html_node(md_content).to_html()
    title = extract_title(md_content)
    new = tp_content.replace("{{ Title }}", title).replace("{{ Content }}", html_string)
    dst = open(dest_path, mode="w")
    dst.write(new)
    dst.close()


def generate_page_recursive(dir_path_content, template_path, des_dir_path):
    for elem in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, elem)
        dst_path = os.path.join(des_dir_path, elem)
        if os.path.isfile(src_path):
            dst_path = dst_path[:-2] + "html"
            generate_page(src_path, template_path, dst_path)
        else:
            if not os.path.exists(dst_path):
                os.mkdir(dst_path)
            generate_page_recursive(src_path, template_path, dst_path)


def main():
    copy_content("static", "public", clean=True)
    generate_page_recursive("content", "template.html", "public")


main()
