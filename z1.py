from gaia import DataLink

#retrieval_type = 'EPOCH_PHOTOMETRY'
retrieval_type = 'ALL'
source_id = [30343944744320, 6196457933368101888]
#source_id = 30343944744320
data_structure = 'INDIVIDUAL'


g = DataLink(source_id, retrieval_type)
g.download()
g.extract()
