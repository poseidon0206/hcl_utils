from qrelease import QRelease
from QRelease2 import QRelease2

q_release = QRelease()
print(q_release)

# get release for every 2 months
q_release2 = QRelease2(query_date="2009-08-12", every=2)
print(q_release2)

# get release for every 6 months, and get 8 releases for both previous and next.
q_release2 = QRelease2(every=6, num_rels=8)
print(q_release2)
