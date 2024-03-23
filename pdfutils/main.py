import argparse
import os

from PyPDF2 import PdfWriter, PdfReader, PdfMerger

RED = "\033[0;31m"
ENDC = "\033[0m"


def colorize(txt, start, end, color=RED):
    return f"{txt[:start]}{color}{txt[start:end]}{ENDC}{txt[end:]}"


def user_confirm(msg):
    answer = input(f"{msg} [y/N]: ").lower()
    return answer in ["y", "yes"]


def imgs2pdf(args):
    from PIL import Image

    if args.load_truncated:
        from PIL import ImageFile

        ImageFile.LOAD_TRUNCATED_IMAGES = True

    img1, *imgsN = [Image.open(img) for img in args.images]
    img1.save(args.output, "PDF", resolution=100.0, save_all=True, append_images=imgsN)


def insert(args):
    with open(args.input, "rb") as ifd, open(args.insert, "rb") as ifd2, open(args.output, "wb") as ofd:
        inputpdf = PdfReader(ifd)
        insertpdf = PdfReader(ifd2)
        output = PdfWriter()

        for i, page in enumerate(inputpdf.pages):
            if i == args.page:
                for page_i in insertpdf.pages:
                    output.add_page(page_i)
            output.add_page(page)

        output.write(ofd)


def rotate(args):
    pages = list(map(int, args.page_angles[:-1:2]))
    rots = list(map(float, args.page_angles[1::2]))

    with open(args.input, "rb") as ifd, open(args.output, "wb") as ofd:
        inputpdf = PdfReader(ifd)
        output = PdfWriter()

        for i, page in enumerate(inputpdf.pages):
            try:
                idx = pages.index(i + 1)
                page.rotate(rots[idx])
            except ValueError:
                pass
            output.add_page(page)

        output.write(ofd)


def search(args):
    import re

    with open(args.input, "rb") as fp:
        reader = PdfReader(fp)
        flags = args.case_insensitive and re.IGNORECASE

        for pagenum, page in enumerate(reader.pages):
            txt = page.extract_text()

            for i, l in enumerate(txt.split("\n")):
                match = re.match(args.pattern, l, flags)
                if match is not None:
                    print(f"{pagenum+1}:{i+1}: {colorize(l, *match.span())}")


def join(args):
    merger = PdfMerger()
    for pdf in args.inputs:
        merger.append(pdf)
    merger.write(args.output)
    merger.close()


def remove(args):
    with open(args.input, "rb") as ifd, open(args.output, "wb") as ofd:
        inputpdf = PdfReader(ifd)
        output = PdfWriter()

        for i, page in enumerate(inputpdf.pages):
            if i + 1 in args.pages:
                continue
            output.add_page(page)

        output.write(ofd)


def scale(args):
    pages = list(map(int, args.page_scales[:-1:2]))
    scales = list(map(float, args.page_scales[1::2]))

    with open(args.input, "rb") as ifd, open(args.output, "wb") as ofd:
        inputpdf = PdfReader(ifd)
        output = PdfWriter()

        for i, page in enumerate(inputpdf.pages):
            try:
                idx = pages.index(i + 1)
                page.scale(scales[idx], scales[idx])
            except ValueError:
                pass
            output.add_page(page)

        output.write(ofd)


def pick(args):
    with open(args.input, "rb") as ifd, open(args.output, "wb") as ofd:
        inputpdf = PdfReader(ifd)
        output = PdfWriter()

        for pagenum in args.pages:
            output.add_page(inputpdf.pages[pagenum - 1])

        output.write(ofd)


def main():
    parser = argparse.ArgumentParser(description="Some simple PDF utilities")
    subparsers = parser.add_subparsers(dest="cmd")
    subparsers.required = True

    imgs2pdf_parser = subparsers.add_parser("imgs2pdf", help="Convert images to PDF")
    imgs2pdf_parser.set_defaults(func=imgs2pdf)
    imgs2pdf_parser.add_argument("images", nargs="+", help="Input image file(s)")
    imgs2pdf_parser.add_argument("output", help="Output PDF file")
    imgs2pdf_parser.add_argument("--load-truncated", action="store_true", help="Set this flag to load truncated images")

    join_parser = subparsers.add_parser("join", help="Join multiple PDFs into one")
    join_parser.set_defaults(func=join)
    join_parser.add_argument("inputs", nargs="+", help="Input PDF file(s) to join")
    join_parser.add_argument("output", help="Output PDF file")

    pick_parser = subparsers.add_parser("pick", help="Pick specific pages from a PDF")
    pick_parser.set_defaults(func=pick)
    pick_parser.add_argument("input", help="Input PDF file")
    pick_parser.add_argument("pages", nargs="+", type=int, help="Page numbers to pick")
    pick_parser.add_argument("output", help="Output PDF file")

    remove_parser = subparsers.add_parser("remove", help="Remove specific pages from a PDF")
    remove_parser.set_defaults(func=remove)
    remove_parser.add_argument("input", help="Input PDF file")
    remove_parser.add_argument("pages", nargs="+", type=int, help="Page numbers to remove")
    remove_parser.add_argument("output", help="Output PDF file")

    insert_parser = subparsers.add_parser("insert", help="Insert a PDF into another PDF")
    insert_parser.set_defaults(func=insert)
    insert_parser.add_argument("input", help="Input PDF file")
    insert_parser.add_argument("insert", help="PDF to be inserted")
    insert_parser.add_argument("page", type=int, help="Page number to insert at")
    insert_parser.add_argument("output", help="Output PDF file")

    scale_parser = subparsers.add_parser("scale", help="Scale specific pages in a PDF")
    scale_parser.set_defaults(func=scale)
    scale_parser.add_argument("input", help="Input PDF file")
    scale_parser.add_argument("page_scales", nargs="+", type=float, metavar="page-scales", help="Page numbers and scales. e.g. 1 0.7 2 1.5 ...")
    scale_parser.add_argument("output", help="Output PDF file")

    rotate_parser = subparsers.add_parser("rotate", help="Rotate specific pages in a PDF")
    rotate_parser.set_defaults(func=rotate)
    rotate_parser.add_argument("input", help="Input PDF file")
    rotate_parser.add_argument("page_angles", nargs="+", metavar="page-angles", type=int, help="Page numbers and angles. e.g. 1 90 2 270 ...")
    rotate_parser.add_argument("output", help="Output PDF file")

    search_parser = subparsers.add_parser("search", help="Search for text in a PDF")
    search_parser.set_defaults(func=search)
    search_parser.add_argument("input", help="Input PDF file")
    search_parser.add_argument("pattern", help="Text/regex to search")
    search_parser.add_argument("--case_insensitive", "-i", action="store_true", help="Case insensitive search")

    args = parser.parse_args()
    if getattr(args, 'output', None):
        import os
        if os.path.exists(args.output) and not user_confirm(f"'{args.output}' already exists. Overwrite?"):
            return 1

    args.func(args)


if __name__ == "__main__":
    main()
