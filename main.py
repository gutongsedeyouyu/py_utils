import unittest

import config
from utils.calendar import create_year_images


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(['utils.test.sorting', 'utils.test.text'])


def main():
    if config.main_action == 'unittest':
        unittest.main(defaultTest='all', verbosity=2)
    elif config.main_action == 'create_year_images':
        create_year_images(config.create_year_images_output_folder,
                           config.create_year_images_years,
                           config.create_year_images_font_file_path)
    else:
        pass


if __name__ == '__main__':
    main()
