import unittest


def all():
    return unittest.defaultTestLoader.loadTestsFromNames(['utils.test.sorting', 'utils.test.text'])


def main():
    unittest.main(defaultTest='all', verbosity=2)


if __name__ == '__main__':
    main()
