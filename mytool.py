#!/usr/bin/env python3

import argparse


import os
from pypdf import PdfWriter
import pdb

from pypdf import PdfWriter, PdfReader
from io import BytesIO
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_footer_pdf(text, page_width, page_height):
    """Create a PDF overlay with footer text and white background"""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(page_width, page_height))

    # Footer box dimensions
    box_height = 18
    box_width = 200
    x = page_width - box_width - 30
    y = 10

    # Draw white background
    c.setFillColorRGB(1, 1, 1)   # white
    c.rect(x, y, box_width, box_height, fill=1, stroke=0)

    # Draw text
    c.setFillColorRGB(0, 0, 0)   # black
    c.setFont("Helvetica", 9)
    c.drawRightString(page_width - 40, y + 5, text)

    c.save()
    packet.seek(0)
    return PdfReader(packet)

def merge_pdfs(input_dir, output_file, filter=None, from_page=None, to_page=None):
    writer = PdfWriter()

    pdf_files = sorted(
        f for f in os.listdir(input_dir)
        if f.lower().endswith(".pdf")
        and (filter is None or filter.lower() in f.lower())
    )

    if not pdf_files:
        print("No matching PDF files found")
        return

    for pdf in pdf_files:
        path = os.path.join(input_dir, pdf)
        reader = PdfReader(path)
        total_pages = len(reader.pages)

        start = (from_page - 1) if from_page else 0
        end = to_page if to_page else total_pages

        if start < 0 or end > total_pages or start >= end:
            raise ValueError(
                f"Invalid page range {from_page}-{to_page} for {pdf} "
                f"(total pages: {total_pages})"
            )

        print(f"Adding {pdf} pages {start + 1}–{end}")

        for i in range(start, end):
            page = reader.pages[i]

            width = float(page.mediabox.width)
            height = float(page.mediabox.height)

            footer_pdf = create_footer_pdf(pdf, width, height)
            page.merge_page(footer_pdf.pages[0])

            writer.add_page(page)

    with open(output_file, "wb") as f:
        writer.write(f)

    print(f"Merged PDF saved as: {output_file}")


def greet(args):
    print(f"Hello, {args.name}!")

def sum_numbers(args):
    print(args.a + args.b)

def pdf_join_func(args):
    merge_pdfs(
        input_dir="./data/ks1/",
        output_file="./output/merged.pdf",
        filter=args.filter,
        from_page=args.from_page,
        to_page=args.to_page
    )

# Main function
def main():
    parser = argparse.ArgumentParser(description="A simple command-line tool example")

    # Version argument
    parser.add_argument( "--version", action="version", version="mytool 1.0.0")

    # Create subparsers = actions
    subparsers = parser.add_subparsers(
        title="actions",
        dest="action",
        required=True
    )

    # ---- greet action ----
    greet_parser = subparsers.add_parser(
        "greet",
        help="Greet a person"
    )

    greet_parser.add_argument(
        "name",
        help="Name to greet"
    )

    greet_parser.set_defaults(func=greet)

    # ---- sum action ----
    sum_parser = subparsers.add_parser(
        "sum",
        help="Add two numbers"
    )
    sum_parser.add_argument("a", type=int)
    sum_parser.add_argument("b", type=int)
    sum_parser.set_defaults(func=sum_numbers)

    # pdf joins
    pdf_join = subparsers.add_parser("pdf_join", help="Joining all Pdf")
    pdf_join.add_argument(
        "--filter",
        help="Filter PDFs by filename (optional)",
        default=None
    )

    pdf_join.add_argument(
        "--from-page",
        type=int,
        help="Start page (1-based, inclusive)",
        default=None
    )

    pdf_join.add_argument(
        "--to-page",
        type=int,
        help="End page (1-based, inclusive)",
        default=None
    )

    pdf_join.add_argument(
        "--two-up",
        action="store_true",
        help="Put 2 pages per output page"
    )
    pdf_join.set_defaults(func=pdf_join_func)

    # Parse.
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()
