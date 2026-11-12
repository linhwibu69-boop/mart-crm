import json,time,unittest,sys
from datetime import datetime,timezone
from pathlib import Path
class Result(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.records=[]
    def startTest(self,t):super().startTest(t);self.started=time.perf_counter()
    def addSuccess(self,t):super().addSuccess(t);self.records.append({'test':t.id(),'status':'PASS','seconds':round(time.perf_counter()-self.started,4)})
    def addFailure(self,t,e):super().addFailure(t,e);self.records.append({'test':t.id(),'status':'FAIL'})
    def addError(self,t,e):super().addError(t,e);self.records.append({'test':t.id(),'status':'ERROR'})
start=time.perf_counter();suite=unittest.defaultTestLoader.discover('test');runner=unittest.TextTestRunner(verbosity=2,resultclass=Result);result=runner.run(suite)
Path('evidence').mkdir(exist_ok=True)
Path('evidence/test_results.json').write_text(json.dumps({'executed_at':datetime.now(timezone.utc).isoformat(),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'skipped':len(result.skipped),'duration_seconds':round(time.perf_counter()-start,3),'cases':result.records},indent=2),encoding='utf-8')
sys.exit(not result.wasSuccessful())
