import sys
from urllib.parse import urlparse


def main(args):
    onshape_url = input('OnShape document URL:')
    doc_id = urlparse(onshape_url).path.split('/')[2]
    print(doc_id)
    assembly_name = input('Aseembly name:')

    # https://cad.onshape.com/documents/XXXXXXXXX/w/YYYYYYYY/e/ZZZZZZZZ


if __name__ == '__main__':
    main(sys.argv[1:])
