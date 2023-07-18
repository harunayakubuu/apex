

def validate_file_type(value):
    if value.file.content_type != 'application/pdf':
        raise ValidationError("Invalid file type. Only PDF file is accepted.")
        # video_size = value.size
        # if video_size > 2084:#10485760: # 10MB
        #     raise ValidationError("This file is too large, maximum size is 2MB.")
        # else:
        #     return value
    else:
        return value