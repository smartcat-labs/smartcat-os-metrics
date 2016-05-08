from ftools import fincore


def main():
    header = ['filename', 'file size', 'total pages', 'pages cached', 'cached size', 'percentage cached']
    result = fincore.execute("ftools/ftools.c", False)
    print fincore.matrix_to_string(result, header)

if __name__ == '__main__':
    main()

