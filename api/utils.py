def get_image_url(image_field):
    if image_field and hasattr(image_field, 'url'):
        return image_field.url
    return None