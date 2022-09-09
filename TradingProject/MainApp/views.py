from django.shortcuts import render
from.forms import csvform
from. import models
import csv
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
import mimetypes
from django.http import StreamingHttpResponse
from wsgiref.util import FileWrapper
import json
# Create your views here.
def home(request):
    form=csvform(request.POST or None,request.FILES or None)
    if form.is_valid():
        form.save()
        form=csvform()
   
    obj=models.csv.objects.last()
    time=obj.timeframe
    s=f"{time}min"
    data = pd.read_csv('media/csvs.txt', parse_dates=['TIME'], index_col = 'TIME')
    data['VOLUME'] = pd.to_numeric(data['VOLUME'], errors='coerce')
    ohlc = {
    'OPEN' : 'first',
    'HIGH': 'max',
    'LOW': 'min',
    'CLOSE': 'last',
    'VOLUME': 'sum'
}
    df = data.resample(s).apply(ohlc)
    res = df.to_json()
    parsed = json.loads(res)
    res=json.dumps(parsed, indent=4)
    file1 = open("media/res.txt", "w") 
    file1.write(res)
    
    return render(request,'MainApp/home.html',{'form':form,'obj':obj})
def download(request):
    base_dir=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    filename='res.json'
    filepath=base_dir+'\\media\\'+filename
    thefile=filepath 
    filename=os.path.basename(thefile)
    chunk_size=8192
    response=StreamingHttpResponse(FileWrapper(open(thefile,'rb'),chunk_size),content_type=mimetypes.guess_type(thefile)[0])
    response['Content-Length']=os.path.getsize(thefile)
    response['Content-Disposition']="Attachment;filename=%s" % filename
    return response
