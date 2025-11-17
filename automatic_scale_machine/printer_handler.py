# PRINTER HANDLER LIBRARY

# Author    : Alfonsus Giovanni
# Version   : 0.1
# Date      : 10 Oktober 2025  

import datetime

PRINTER_PATH = "/dev/rfcomm0"

# ESC/POS control codes
ESC = b"\x1b"
GS  = b"\x1d"

class Printer:
    def __init__(self, esc_code, gs_code):
        # Control codes
        self.esc = esc_code
        self.gs = gs_code

    def escpos_text(self, text: str, align="left", bold=False, double=False):
        """Format text with ESC/POS commands."""
        cmd = b""

        # Alignment: 0=left, 1=center, 2=right
        alignments = {"left": 0, "center": 1, "right": 2}
        cmd += self.esc+ b"a" + bytes([alignments.get(align, 0)])

        # Font style (bold, double size)
        cmd += self.esc + b"!" + bytes([
            (8 if bold else 0) + (32 if double else 0)
        ])

        # Encode text + newline
        cmd += text.encode("ascii", "replace") + b"\n"

        # Reset style
        cmd += self.esc + b"!" + b"\x00"
        cmd += self.esc + b"a" + b"\x00"

        return cmd

    def print_receipt(self, input_name, items, item_count, manpower):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cust_name = input_name

        with open(PRINTER_PATH, "wb") as f:
            data = b""

            # Header
            data += self.escpos_text("UD. Soenarto YS", align="center", bold=True, double=True)
            data += self.escpos_text("Jl. Sukowati No 24", align="center")
            data += self.escpos_text("Telp: 0813-2778-8448", align="center")
            data += self.escpos_text("--------------------------------")

            # Transaction info
            data += self.escpos_text(f"Date: {now}")
            data += self.escpos_text(f"Name: {self.cust_name}")
            data += self.escpos_text("--------------------------------")

            total_price = 0
            total_weight = 0

            for name, weight, price in items:
                subtotal = int(weight*price)
                total_price += subtotal
                total_weight += weight
                line = f"{name:<12}{weight:>4}x{int(price):>5} = {subtotal:>7}"
                data += self.escpos_text(line)

            data += self.escpos_text("--------------------------------")
            data += self.escpos_text(f"JUMLAH SAK    : {item_count:,.0f}", align="left", bold=True)
            data += self.escpos_text(f"BERAT TOTAL   : {total_weight:,.0f}Kg", align="left", bold=True)
            data += self.escpos_text(f"ONGKOS TENAGA : Rp {manpower:,.0f}", align="left", bold=True)

            data += self.escpos_text(f" ",  align="left", bold=False)

            data += self.escpos_text(f"HARGA         : Rp {total_price:,.0f}", align="left", bold=True)
            data += self.escpos_text(f"HARGA TOTAL   : Rp {total_price-manpower:,.0f}", align="left", bold=True)
            data += self.escpos_text("--------------------------------")

            # Footer
            data += self.escpos_text("Terima kasih!", align="center")
            data += self.escpos_text("-Dari Bumi Untuk Masyarakat-", align="center")

            # Feed and cut
            data += b"\n\n\n" + self.gs + b"V" + b"\x00"

            f.write(data)
            f.flush()

            print("✅ Struk berhasil dicetak.")

MyPrinter = Printer(ESC, GS)