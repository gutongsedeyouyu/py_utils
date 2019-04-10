import unittest

from utils.calendar import create_calendar_images


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(['utils.test.sorting', 'utils.test.text'])


def main():
    action = ['unittest', 'create_calendar_images'][0]
    if action == 'unittest':
        unittest.main(defaultTest='all', verbosity=2)
    elif action == 'create_calendar_images':
        output_folder = '/output/folder/path'
        years = range(2019, 2020)
        font_file_path = '/path/to/font/file'
        create_calendar_images(output_folder, years, font_file_path)
    else:
        pass


if __name__ == '__main__':
    main()
