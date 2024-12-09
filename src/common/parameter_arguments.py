import argparse
from argparse import Namespace

def parse_opt():
    parser = argparse.ArgumentParser(description='Automatic SUNAT notification extraction from mailbox')
    parser.add_argument('--extractor', dest='extractor', action='store', 
                        default="manual", choices=['manual', 'llm'],
                        help='List of notifications extractor from HTML', required=False)
    
    return parser
