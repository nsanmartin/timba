def esp_text_to_num_text(text):
    if text == '-': return '0'
    return text.strip().replace('.', '').replace(',', '.')
