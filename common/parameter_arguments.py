import argparse
from argparse import Namespace

def parse_opt():
    parser = argparse.ArgumentParser(description='Automatic SUNAT notification extraction from mailbox')
    parser.add_argument('--extractor', dest='extractor', action='store', 
                        default="manual", choices=['manual', 'llm'],
                        help='List of notifications extractor from HTML', required=False)

    parser.add_argument('--save_to', dest='save_to', action='store', 
                        default="excel", choices=['excel', 'db'],
                        help='Save notifications to', required=False)

    return parser
