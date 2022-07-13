from gaia import DataLink

retrieval_type = 'ALL'
source_id = [30343944744320, 6196457933368101888]
#source_id = 30343944744320


dl = DataLink(source_id=source_id, retrieval_type=retrieval_type)
dl.download()
objs = dl.get_objects()

