# PRINTER HANDLER LIBRARY

# Author    : Alfonsus Giovanni
# Version   : 0.1
# Date      : 10 Oktober 2025  

import datetime

PRINTER_PATH = "/dev/usb/lp0"

# ESC/POS control codes
ESC = b"\x1b"
GS  = b"\x1d"

class printer:
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

    def print_receipt(self, input_name, item_data, input_weight, input_price):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cust_name = input_name
        self.total_weight = input_weight
        self.total_price = input_price

        self.item_count = len(item_data)

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

            # Item list
            items = [
                ("Tepung A", 2, 2700),
                ("Tepung B", 1, 2550),
                ("Campur", 3, 2400),
            ]
            total = 0
            for name, qty, price in items:
                subtotal = qty * price
                total += subtotal
                line = f"{name:<12}{qty:>3}x{price:>6} = {subtotal:>7}"
                data += self.escpos_text(line)

            data += self.escpos_text("--------------------------------")
            
            data += self.escpos_text(f"TOTAL: Rp {total:,.0f}", align="right", bold=True)
            data += self.escpos_text("--------------------------------")

            # Footer
            data += self.escpos_text("Terima kasih!", align="center")
            data += self.escpos_text("Dari Bumi Untuk Masyarakat", align="center")

            # Feed and cut
            data += b"\n\n\n" + self.gs + b"V" + b"\x00"

            f.write(data)
            f.flush()

            print("✅ Struk berhasil dicetak.")

if __name__ == "__main__":
    #print_receipt()
    pass
