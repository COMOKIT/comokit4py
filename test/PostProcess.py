from testfacility import test, testheader, testdir
from comokit4py import comokitreport as rp
from os.path import join as joinpath
from pandas import read_csv as readcsv

testheader("Post process testing")
datadir = joinpath(testdir(), "testdata")
reportfile = joinpath(datadir, "report.csv")
df0 = readcsv(reportfile).select_dtypes(int)
exname = "HeadlessNoPolicy"

@test("Generate report")
def _():
	dfs = rp.gatherData(datadir, exname)
	df = rp.generateReport(dfs).select_dtypes(int)
	return df0.to_numpy().all() == df.to_numpy().all()
