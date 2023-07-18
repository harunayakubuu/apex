def validate_file_type(value):
    if value.file.content_type != 'application/pdf':
        return value
    else:
        raise ValidationError("Invalid file type. Upload PDF files only.")