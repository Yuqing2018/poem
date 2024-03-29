#!/usr/bin/env python
# -*- coding: utf-8 -*-
import celery
import time
import json
import sys
import datetime
import random
import os
app = celery.Celery('tasks')
app.config_from_object('celeryconfig')

myUI = None
generater = None
jiju = None
ui = None
firstgen = None
songci = None

JJ_code = [-1, 1, 2, 4, 7, 1]
yc = json.loads(open("yc.txt").readline())
#默认：-1
# 隐逸诗：1
# 边塞诗：2
# 思乡诗：4
# 咏史诗：7

class CallbackTask(celery.Task):
    def on_success(self, retval, task_id, args, kwargs):
        print ("----%s is done" % task_id)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass

@app.task(base=CallbackTask)
def main_CT(prom_old):
    global generater
    if(generater == None):
        os.chdir("/var/jiuge/PoemModelHeadFinal/")
        sys.path.append("/var/jiuge/PoemModelHeadFinal/")
        from get_poem import Generator
        generater = Generator()
    prom = json.loads(prom_old)
    print(prom)
    # if(not prom['used'] == None):
    #     prom['result'] = json.loads(prom['used'])
    #     prom['used'] = 'True'
    #     return json.dumps(prom)
    type_top = prom['type_top']
    tmp = type_top['top']+type_top['yan']
    if(type_top['top'] == "德才兼备"):
        if(int(type_top['yan']) == 5):
            prom_result = {"code":0, "content":"德寿同尧舜\t才名异古人\t兼之推第一\t备乐及斯民"}
            prom['result'] = prom_result
            time.sleep(random.random()*5+3)
            return json.dumps(prom)
        else:
            prom_result = {"code":0, "content":"德寿威仪天咫尺\t才名荣耀世多时\t兼资盛事推公等\t备有新诗颂美词"}
            prom['result'] = prom_result
            time.sleep(random.random()*5+3)
            return json.dumps(prom)
    if(type_top['top'] == "任人唯贤"):
        if(int(type_top['yan']) == 7):
            prom_result = {"code":0, "content":"任公何处问交游\t人在江南第一州\t唯有故园春色好\t贤豪相对话悠悠"}
            prom['result'] = prom_result
            time.sleep(random.random()*5+3)
            return json.dumps(prom)

    # prom_result = 'test\ttest'
    try:
        info, poems = generater.generate(type_top['top'].encode("utf-8"), int(type_top['yan']))
    except Exception as e:
        print( e)
        poems = []
        info = "Error"
    if(len(poems) == 0):
        # client._db.lpush("JJ", json.dumps(prom))
        print( info)
        poems = ['该嵌首字无法成诗','请重新输入嵌首字']
    else:
        poems = map(lambda x:x.decode("utf-8"), poems)
    prom_result = {"code":0, "content":"\t".join(poems)}
    prom['result'] = prom_result
    return json.dumps(prom)

@app.task(base=CallbackTask)
def main_JJJ(prom_old):
    global jiju
    if(jiju == None):
        os.chdir("/var/jiuge/jiju_new")
        sys.path.append("/var/jiuge/jiju_new")
        from Jiju import Jiju
        #import sys
        reload(sys)
        sys.setdefaultencoding('utf-8')
        jiju = Jiju()
    prom = json.loads(prom_old)
    print(prom)
    # if(not prom['used'] == None):
    #     prom['result'] = json.loads(prom['used'])
    #     prom['used'] = 'True'
    #     return json.dumps(prom)
    type_top = prom['type_top']
    tmp = type_top['top']+type_top['yan']
    if(tmp in yc):
        if(yc[tmp]['type'] == type_top['type']):
            prom_result = {"code":1, "content":yc[tmp]['content'], "source":yc[tmp]['source']}
            prom['result'] = prom_result
            time.sleep(random.random()*5+4)
            return json.dumps(prom)
    # prom_result = 'test\ttest'
    prom_result = {}
    try:
        poems = jiju.get_jiju(type_top['top'])
    except Exception as e:
        print( e)
        poems = {'msg' : "Error"}
    if(poems['msg'] != ""):
        # client._db.lpush("JJ", json.dumps(prom))
        print( poems['msg'])
        poems = ['该首句无法成诗','请重新输入首句']
        prom_result = {"code":0, "content":"\t".join(poems)}
    else:
        poems_c = [poems['data']['sen1'], poems['data']['sen2'], poems['data']['sen3'], poems['data']['sen4']]
        poems_source = ["", poems['data']['sen2_source'], poems['data']['sen3_source'], poems['data']['sen4_source']]
        prom_result = {"code":1, "content":"\t".join(poems_c), "source":poems_source}
    prom['result'] = prom_result
    return json.dumps(prom)


@app.task(base=CallbackTask)
def main_JJ(prom_old):
    global myUI
    if(myUI == None):
        os.chdir("/var/jiuge/JueJu/")
        sys.path.append("/var/jiuge/JueJu/")
        from KSModel.SampleUI import SampleUI
        myUI = SampleUI()
    prom = json.loads(prom_old)
    print(prom)
    # if(not prom['used'] == None):
    #     prom['result'] = json.loads(prom['used'])
    #     prom['used'] = 'True'
    #     return json.dumps(prom)
    type_top = prom['type_top']
    tmp = type_top['top']+type_top['yan']
    if(tmp in yc):
        if(yc[tmp]['type'] == type_top['type']):
            prom_result = {"code":0, "content": "\t".join(yc[tmp]['result'][int(random.random()*5+0.01)]), "type":2}
            prom['result'] = prom_result
            time.sleep(random.random()*4)
            return json.dumps(prom)
    # prom_result = 'test\ttest'
    try:
        poems, info = myUI.generate(type_top['top'].encode("utf-8"), int(type_top['yan']), 1)
    except Exception as e:
        print( e)
        poems = []
        info = "Error"
    if(len(poems) == 0):
        # client._db.lpush("JJ", json.dumps(prom))
        print( info)
        poems = [['该主题词无法成诗', '请重新选择主题词']]
    prom_result = {"code": 0, "content": "\t".join(poems[0]), "type": 0}
    prom['result'] = prom_result
    return json.dumps(prom)

@app.task(base=CallbackTask)
def main_JJ1(prom_old):
    global firstgen
    global ui
    if(ui == None):
        sys.path.append("/var/jiuge/PoemModel3")
        os.chdir("/var/jiuge/PoemModel3")
        from FirstModel.Generator import Generator
        firstgen = Generator()
        from generate import GeneratorUI
        ui = GeneratorUI()
    prom = json.loads(prom_old)
    print(prom)
    # if(not prom['used'] == None):
    #     prom['result'] = json.loads(prom['used'])
    #     prom['used'] = 'True'
    #     return json.dumps(prom)
    type_top = prom['type_top']
    tmp = type_top['top']+type_top['yan']
    if(tmp in yc):
        if(yc[tmp]['type'] == type_top['type']):
            prom_result = {"code":0, "content": "\t".join(yc[tmp]['result'][int(random.random()*5+0.01)]), "type":2}
            prom['result'] = prom_result
            time.sleep(random.random()*4+2)
            return json.dumps(prom)
    # prom_result = 'test\ttest'
    state = JJ_code[int(random.random()*5)]
    print( "state:", state)
    try:
        sens, info = firstgen.generate(type_top['top'].encode("utf-8"), int(type_top['yan']), mode=2)
        print( sens[0])
        poems = [ui.generate_api(True, 20, sens[0], state).split(" ")]
        print( poems)
    except Exception as e:
        print( e)
        poems = []
        info = "Error"
    if(len(poems) == 0):
        print( info)
        poems = [['该主题词无法成诗', '请重新选择主题词']]
    prom_result = {"code": 0, "content": "\t".join(poems[0]), "state": state, "type": 1}
    prom['result'] = prom_result
    return json.dumps(prom)

@app.task(base=CallbackTask)
def main_SC(prom_old):
    global songci
    if(songci == None):
        sys.path.append("/root/jiuge_test/")
        os.chdir("/root/jiuge_test/")
        from Core.PoetryUI import PoetryUI
        songci = PoetryUI()
    prom = json.loads(prom_old)
    print(prom)
    # if(not prom['used'] == None):
    #     prom['result'] = json.loads(prom['used'])
    #     prom['used'] = 'True'
    #     return json.dumps(prom)
    type_top = prom['type_top']
    tmp = type_top['top']+type_top['yan']
    # prom_result = 'test\ttest'
    # state = JJ_code[int(random.random()*5)]
    # print "state:", state
    try:
        poems, info = songci.generate(type_top['top'].encode("utf-8"), int(type_top['yan'])+1)
        print (poems)
    except Exception as e:
        print( e)
        poems = []
        info = "Error"
    if(len(poems) == 0):
        print( info)
        poems = [['该主题词无法成词', '请重新选择主题词']]
    prom_result = {"code": 0, "content": poems}
    prom['result'] = prom_result
    return json.dumps(prom)


from KeyWrapper.KeyWrapper import KeyWrapper
@app.task(base=CallbackTask)
def main_Tencent(prom_old):
    global songci
    global myUI
    if(songci == None):
        sys.path.append("/var/jiuge/SC/")
        os.chdir("/var/jiuge/SC/")
        from Core.PoetryUI import PoetryUI
        songci = PoetryUI()
    if(myUI == None):
        os.chdir("/var/jiuge/JueJu/")
        sys.path.append("/var/jiuge/JueJu/")
        from KSModel.SampleUI import SampleUI
        myUI = SampleUI()
    prom = json.loads(prom_old)
    print(prom)
    # if(not prom['used'] == None):
    #     prom['result'] = json.loads(prom['used'])
    #     prom['used'] = 'True'
    #     return json.dumps(prom)
    words = type_top['top'].strip().split(" ")
    model, newwords = keywrapper.process(words)
    newwords = " ".join(newwords)
    type_top = prom['type_top']
    tmp = type_top['top']+type_top['yan']
    # prom_result = 'test\ttest'
    # state = JJ_code[int(random.random()*5)]
    # print "state:", state
    yan_map = {"5":0,"7":1}
    if(model == 'wm'):
        try:
            poems, info = songci.generate(newwords.encode("utf-8"), yan_map[type_top['yan']])
            print( poems)
        except Exception as e:
            print( e)
            poems = []
            info = "Error"
    else:
        try:
            poems, info = myUI.generate(newwords.encode("utf-8"), int(type_top['yan']), 1)
            print( poems)
        except Exception as e:
            print( e)
            poems = []
            info = "Error"
    if(len(poems) == 0):
        print( info)
        poems = [['该主题词无法成词', '请重新选择主题词']]
    prom_result = {"code": 0, "content": ans}
    prom['result'] = prom_result
    return json.dumps(prom)
