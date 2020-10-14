#!/usr/bin/env python3

import pandas as pd, xlrd, argparse, os.path


def main(xls, csv):
    print("xls='{}', csv= '{}'".format(xls,csv))
    try:
        data_xls = pd.read_excel(xls, 'Sheet1', index_col=None)
    except:
        data_xls = pd.read_excel(xls, index_col=None)
    data_xls.to_csv(csv, encoding='utf-8', index=False)



def parse_args():
    parser = argparse.ArgumentParser(
        description='Convert xlsx file into csv file')
    parser.add_argument('--source', type=str, required=True,
                        help='Name of excel file')
    parser.add_argument('--csv', type=str, required=False,
                        help='name of csv output file')
    return parser.parse_args()


if __name__ == '__main__':

    '''
    #dump(o)
    #print 'fields: {info}'.format(**{u'info': u'CloudClient[0xc8f0500] connected, creating MediaCloud', u'subject': u'Master', u'proc': u'13949', u'time': u'2017-05-03T08:23:19.194812928Z'})
    #print 'fields: {info}'.format(**o[0]["(u'conf', None)"][1])
    #coord = {'latitude': '37.24N', 'longitude': '-115.81W'}
    #print 'Coordinates: {latitude}, {longitude}'.format(**coord)
    '''
    args = parse_args()
    if(os.path.isfile(args.source)):
        if(None == args.csv):
            basename=os.path.basename(args.source)
            name, ext = os.path.splitext(args.source)
            print("Source = '{}{}'".format(name,ext))
            args.csv=basename.replace(ext,'.csv')
        if(os.path.isfile(args.csv)):
            print("File already exists '{}'".format(args.csv))
        else:
            main(xls=args.source, csv=args.csv)
 