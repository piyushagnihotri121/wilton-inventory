from PIL import Image, ImageDraw, ImageFont
import os

def get_font(size):
    font_path = "/System/Library/Fonts/Supplemental/Arial Narrow Bold.ttf"
    return ImageFont.truetype(font_path, size)

def calculate_optimal_font_size(label_width, label_height, sample_text_lines):
    min_size = 8
    max_size = 28
    padding = 0.25
    available_height = label_height - 0.5 * padding

    best_size = min_size
    for size in range(min_size, max_size + 1):
        font = get_font(size)
        line_heights = []
        max_line_width = 0
        for line in sample_text_lines:
            bbox = font.getbbox(line)
            line_height = bbox[3] - bbox[1]
            line_width = bbox[2] - bbox[0]
            line_heights.append(line_height)
            max_line_width = max(max_line_width, line_width)

        total_text_height = sum(line_heights)
        if total_text_height <= available_height and max_line_width <= (label_width - 2 * padding):
            best_size = size
        else:
            break

    return best_size

def create_invoice_labels():
    print("=== INVOICE LABEL GENERATOR ===")
    print("Creates 65 labels per A4 sheet (38mm x 21mm each)")

    date = input("Enter Date (e.g., 01-07-2024): ").strip()
    invoice_no = input("Enter Invoice Number (e.g., INV-123): ").strip()
    supplier = input(str("Enter Supplier Name: ")).strip()

    num_items = int(input("Number of different items: "))
    items_data = {}
    total_labels = 0

    for i in range(1, num_items + 1):
        pieces = int(input(f"Number of pieces for item {i}: "))
        items_data[i] = pieces
        total_labels += pieces

    print(f"\nTotal labels to generate: {total_labels}")

    DPI = 300
    A4_WIDTH_MM, A4_HEIGHT_MM = 210, 297
    A4_WIDTH_PX = int(A4_WIDTH_MM / 25.4 * DPI)
    A4_HEIGHT_PX = int(A4_HEIGHT_MM / 25.4 * DPI)
    LABEL_WIDTH_MM, LABEL_HEIGHT_MM = 37.02, 20.99
    LABEL_WIDTH_PX = int(LABEL_WIDTH_MM / 25.4 * DPI)
    LABEL_HEIGHT_PX = int(LABEL_HEIGHT_MM / 25.4 * DPI)

    COLS, ROWS = 5, 13
    MAX_LABELS_PER_SHEET = COLS * ROWS

# Margins in mm
    MARGIN_LEFT_RIGHT_MM = 8
    MARGIN_TOP_BOTTOM_MM = 14

    V_SPACING_MM = 0
    H_SPACING_MM = 2

# Convert to pixels
    MARGIN_LEFT_RIGHT_PX = int(MARGIN_LEFT_RIGHT_MM / 25.4 * DPI)
    MARGIN_TOP_BOTTOM_PX = int(MARGIN_TOP_BOTTOM_MM / 25.4 * DPI)

    v_spacing = int(V_SPACING_MM / 25.4 * DPI)
    h_spacing = int(H_SPACING_MM / 25.4 * DPI)

# Available drawing area inside margins
    available_width = A4_WIDTH_PX - 2 * MARGIN_LEFT_RIGHT_PX
    available_height = A4_HEIGHT_PX - 2 * MARGIN_TOP_BOTTOM_PX

# Total occupied width/height by labels and spacings
    total_label_width = (available_width - (COLS - 1) * h_spacing) // COLS
    total_label_height =(available_height - (ROWS - 1) * v_spacing) // ROWS


    max_cols = (available_width + h_spacing) // (LABEL_WIDTH_PX + h_spacing)
    max_rows = (available_height + v_spacing) // (LABEL_HEIGHT_PX + v_spacing)


    if COLS > max_cols:
        print(f"⚠️ Only {max_cols} columns can fit, adjusting COLS.")
        COLS = max_cols

    if ROWS > max_rows:
        print(f"⚠️ Only {max_rows} rows can fit, adjusting ROWS.")
        ROWS = max_rows


    total_label_width = (available_width - (COLS - 1) * h_spacing) // COLS
    total_label_height =(available_height - (ROWS - 1) * v_spacing) // ROWS   


# Absolute start positions (from page margin — no centering)
    start_x = MARGIN_LEFT_RIGHT_PX  
    start_y = MARGIN_TOP_BOTTOM_PX  


    print(f"Available width: {available_width}px, Occupied by labels: {total_label_width}px")
    print(f"Available height: {available_height}px, Occupied by labels: {total_label_height}px")

    for row in range(ROWS):
        for col in range(COLS):
            x = start_x + col * (LABEL_WIDTH_PX + h_spacing)
            y = start_y + row * (LABEL_HEIGHT_PX + v_spacing)

            #Safety: Skip if label crosses right or bottom margin
            if x + LABEL_WIDTH_PX > A4_WIDTH_PX - MARGIN_LEFT_RIGHT_PX:
               

               continue
            if y + LABEL_HEIGHT_PX > A4_HEIGHT_PX - MARGIN_TOP_BOTTOM_PX:
               continue


           
    




    sample_lines = [
        f"DATE: {date}",
        f"INVOICE: {invoice_no}",
        f"SUPPLIER: {supplier[:]}",
        "ITEM: 99",
        "PIECE: 999/999"
    ]

    font_size = calculate_optimal_font_size(LABEL_WIDTH_PX, LABEL_HEIGHT_PX, sample_lines)
    font = get_font(font_size)

    print(f"Using font size: {font_size}pt")

    sheet_number = 1
    label_count = 0
    sheet = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), "white")
    draw = ImageDraw.Draw(sheet)

    for item_num, num_pieces in items_data.items():
        for piece_num in range(1, num_pieces + 1):
            if label_count >= MAX_LABELS_PER_SHEET:
                filename = f"Invoice_Labels_Sheet_{sheet_number}.png"
                sheet.save(filename, dpi=(DPI, DPI))
                print(f"Saved: {filename}")

                sheet_number += 1
                sheet = Image.new("RGB", (A4_WIDTH_PX, A4_HEIGHT_PX), "white")
                draw = ImageDraw.Draw(sheet)
                label_count = 0

            col = label_count % COLS
            row = label_count // COLS

            x = start_x + col * (LABEL_WIDTH_PX + h_spacing)
            y = start_y + row * (LABEL_HEIGHT_PX + v_spacing)

            draw.rectangle(
                [x, y, x + LABEL_WIDTH_PX - 1, y + LABEL_HEIGHT_PX - 1],
                outline="black",
                width=1
            )

            supplier_short = supplier[:]
            text_lines = [
                f" DATE: {date}",
                f" INVOICE: {invoice_no}",
                f" SUPPLIER: {supplier_short}\n",
                f"                        ",
                f" ITEM: {item_num}                 ;               PIECE: {piece_num}/{num_pieces}",
                # f"PIECE: {piece_num}/{num_pieces}"
            ]

            padding = 6
            line_heights = []
            for line in text_lines:
                bbox = font.getbbox(line)
                line_heights.append(bbox[3] - bbox[1])

            total_text_height = sum(line_heights)
            available_label_height = LABEL_HEIGHT_PX - 2 * padding
            remaining_space = available_label_height - total_text_height

            if len(text_lines) > 1:
                line_spacing = int(remaining_space // (len(text_lines) - 1))*0.76
            else:
                line_spacing = 0

            current_y = y + padding
            for i, line in enumerate(text_lines):
                draw.text(
                    (x + padding, current_y),
                    line,
                    fill="black",
                    font=font
                )
                current_y += line_heights[i] + line_spacing

            label_count += 1

    filename = f"Invoice_Labels_Sheet_{sheet_number}.png"
    sheet.save(filename, dpi=(DPI, DPI))
    print(f"Saved: {filename}")

    print(f"\n✅ SUCCESS! Generated {total_labels} labels across {sheet_number} sheet(s). Font size: {font_size}pt")

if __name__ == "__main__":
    create_invoice_labels()

