"""Adapter for the managed preview daemon. End users run start.bat instead."""
import argparse
import uvicorn
p=argparse.ArgumentParser();p.add_argument('--host',default='127.0.0.1');p.add_argument('--port',type=int,default=8000)
a,_=p.parse_known_args();uvicorn.run('app.main:app',host=a.host,port=a.port)
