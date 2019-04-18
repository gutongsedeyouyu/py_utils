from datetime import datetime
from math import ceil
import os.path

from PIL import Image, ImageDraw, ImageFont


def _create_month_image(year, month, width, height, font_file_path):
    image = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(image)
    num_days_a_week, num_rows = 7, 7
    #
    # Draw background
    #
    draw.rectangle((0, 0, width - 1, height - 1), (255, 255, 255))
    font = ImageFont.truetype(font_file_path, int(min(width, height) * 0.5))
    text_size = draw.textsize(str(month), font)
    draw.text(((width - text_size[0]) // 2, (height - text_size[1]) // 2), str(month), (238, 238, 238), font)
    #
    # Calculate dates
    #
    dates = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']
    try:
        for i in range(1, 32):
            date = datetime(year, month, i)
            if i == 1 and date.weekday() < 6:
                for _ in range(date.weekday() + 1):
                    dates.append('')
            dates.append(str(i))
    except ValueError:
        pass
    #
    # Draw dates
    #
    font = ImageFont.truetype(font_file_path, int(min(width // num_days_a_week, height // num_rows) * 0.5))
    for i, date in enumerate(dates):
        text_size = draw.textsize(date, font)
        x = width // num_days_a_week * (i % num_days_a_week) + (width // num_days_a_week - text_size[0]) // 2
        y = height // num_rows * (i // num_days_a_week) + (height // num_rows - text_size[1]) // 2
        fill = (153, 153, 153) if i // num_days_a_week == 0 else (51, 51, 51)
        draw.text((x, y), date, fill, font)
    return image


def _create_year_image(output_folder, year, font_file_path):
    title_height, month_image_width, month_image_height, month_image_margin = 150, 300, 300, 15
    year_image_width = month_image_width * 3 + month_image_margin * 4
    year_image_height = title_height + month_image_height * 4 + month_image_margin * 5
    month_images = list()
    try:
        year_image = Image.new('RGB', (year_image_width, year_image_height))
        #
        # Draw background
        #
        draw = ImageDraw.Draw(year_image)
        draw.rectangle((0, 0, year_image_width - 1, year_image_height - 1), (255, 255, 255))
        #
        # Draw title
        #
        font = ImageFont.truetype(font_file_path, int(title_height * 0.5))
        text_size = draw.textsize(str(year), font)
        draw.text(((title_height - text_size[1]) // 2, (title_height - text_size[1]) // 2), str(year), (153, 153, 153), font)
        #
        # Draw months
        #
        for month in range(1, 13):
            month_images.append(_create_month_image(year, month, month_image_width, month_image_height, font_file_path))
        for i, month_image in enumerate(month_images):
            x1 = month_image_margin + (month_image_width + month_image_margin) * (i % 3)
            y1 = title_height + month_image_margin + (month_image_height + month_image_margin) * (i // 3)
            x2 = x1 + month_image_width
            y2 = y1 + month_image_height
            year_image.paste(month_image, (x1, y1, x2, y2))
        return year_image
    finally:
        for month_image in month_images:
            month_image.close()


def create_year_images(output_folder, years, font_file_path):
    for year in years:
        with _create_year_image(output_folder, year, font_file_path) as year_image:
            year_image.save(os.path.join(output_folder, '{0}.png'.format(year)))
