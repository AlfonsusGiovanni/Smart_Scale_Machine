def rupiah_format(angka, with_prefix=False, desimal=0):
    formatted_number = "{:,.{}f}".format(angka, desimal)
    formatted_number = formatted_number.replace(",", "X").replace(".", ",").replace("X", ".")

    if with_prefix:
        return "Rp. {}".format(formatted_number)
    return formatted_number

def rupiah_deformat(angka):
    deformatted_number = angka.replace("Rp", "").replace(".", "").replace(" ", "")
    deformatted_number = deformatted_number.replace(",", ".")
    
    if "." in deformatted_number:
        return float(deformatted_number)
    return int(deformatted_number)