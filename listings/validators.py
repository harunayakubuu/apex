from django.core.exceptions import ValidationError


def validate_picture_size(value):
    picutre_size = value.size

    if picutre_size > 1024000:
        raise ValidationError(f'File too large. Maximum size allowed is 500kb.')
    else:
        return value
        
def validate_floor_design_size(value):
    floor_design_size = value.size

    if floor_design_size > 1024000:
        floor_design_size = floor_design_size/1024
        raise ValidationError(f'File too large. Maximum size allowed is 50kb.')
    else:
        return value

# 10485760: 10MB

def validate_picture_dimension(width=1200, height=800):
    def validator(picture):
        error = False
        if width is not None and height is not None and picture.width > width and picture.height > height:
            error = True
        if width is not None and height is not None and picture.width < width and picture.height < height:
            error = True

        if error:
            raise ValidationError([f'Dimension should be {width}x{height} pixels.'])
    return f'{width}X{height}'


def validate_video_size(value):
    if value.file.content_type == 'application/mp4':
        video_size = value.size
        if video_size > 5242880:#10485760: # 10MB
        
            raise ValidationError("This file is too large, maximum size is 2MB.")
        else:
            return value
    else:
        raise ValidationError("Invalid file type. Upload video files only.")
    

    # if video_size > 10485760: # 10MB
    #     raise ValidationError("Video size is too large, maximum is 10MB.")
    # else:
    #     return value