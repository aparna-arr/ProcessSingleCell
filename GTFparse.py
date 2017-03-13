import re
import operator

def parseValidLine(line):
    line_ar = line.rstrip('\n\r').split('\t')

    if len(line_ar) < 9:
        return {}
    
    id_string = line_ar[8]
    gene_id = re.search(r'gene_id \"(.+?)\";', id_string).group(1)

    result = {
        'chrom': line_ar[0],
        'feature': line_ar[2],
        'start': int(line_ar[3]),
        'end': int(line_ar[4]),
        'strand': line_ar[6],
        'gene_id': gene_id
        }

    if result['feature'] != "gene":
        return {}

    return result

def sortGTFStructure(data):
    for chrom in data:
        for strand in data[chrom]:
            data[chrom][strand].sort(key=operator.itemgetter('start', 'end'))

def parseGTFFile (gtf_fp):
    parsedData = dict()

    for line in gtf_fp:
        if line.startswith('#'):
            continue

        fields = parseValidLine(line)

        if not fields:
            continue
        
        if fields['chrom'] not in parsedData:
            parsedData[fields['chrom']] = {
                '+':list(),
                '-':list()
                }

        parsedData[fields['chrom']][fields['strand']].append({
            'gene_id':fields['gene_id'],
            'start':fields['start'],
            'end':fields['end'],
            'reads':list()
            })
        
        # guarantee sorted GTF data
        sortGTFStructure(parsedData)

    return parsedData
