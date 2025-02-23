import nodriver as uc
# import json
from hclick4 import hClick4
import pyautogui as pagui
# import time
import numpy as np
import asyncio
from chumbaScratchImageProcessor import chumbaOCR
from siteCollect2Helpers import chumbaGenerateCoords
from hmoveVGW2 import hmoveVGW2
import collections
# import requests
from PIL import Image
from io import BytesIO
from codeOCR import singleOCR
import threading
from humanPause import humanPause
import base64
# from customScreenshot import customScreenshot
from helper.nodriverElementScreenshot import customScreenshotElement
from collect_ml import mlCollect2
from collect_sk import skCollect2
from collect_gp import gpCollect2
from collect_pz import pzCollect2
from settingsObj import SettingsObj
from helper.coordsObj import CoordsObj,createCoordsObj,relativeCoordsObjPosition
from siteCollect2Helpers import scratchEvent
from pathlib import 

class NoOCRException(Exception):
    pass

class HelperSitecollect2:
    def __init__(self,codeVisible,finished,settings:SettingsObj):
        self.codeVisible = codeVisible
        self.finished = finished
        self.settings = settings

async def siteCollect2(page:uc.Tab,siteName:str,settings:SettingsObj)->str:
    """captcha should exit when captcha finishes. if no captcha, no post processing is done. returns string (either code or filepath. check settings for OCR for info)"""
    codeVisible=[False]
    finished = [False]


    # return string of code on page 
    helper = HelperSitecollect2(codeVisible,finished,settings)
    if (siteName == "sk"):
        string = await skCollect2(page,helper)
        return string 
    elif (siteName == "pz"):
        string = await pzCollect2(page,helper)
        return string 
    elif(siteName == "cb"): # working
        string = await cbCollect2(page,helper)
        return string 
    elif(siteName == "ml"): # working
        string = await mlCollect2(page)
        return string 
    elif (siteName == "cp"): # working
        string = await cpCollect2(page,helper)
        return string
    elif (siteName == "gp"):
        string = await gpCollect2(page,helper)
        return string

async def cpCollect2(page:uc.Tab,helper:HelperSitecollect2)-> str:
    prq = await page.query_selector('[class="KHKWidgetAmoeRootContainer__code"]')
    cpCodeFilename = "./cache/cpCode.jpeg"

    # codeImage = await prq.save_screenshot(filename=cpCodeFilename)
    coords = await prq.get_position()
    # await asyncio.get_event_loop().run_in_executor(None,customScreenshot,coords,cpCodeFilename)
    await customScreenshotElement(page,coords,cpCodeFilename)

    # await customScreenshot(coords,cpCodeFilename)
    if helper.settings.mainSettings['OCR']==1:
        code = singleOCR(cpCodeFilename)
    if helper.settings.mainSettings['OCR']==0:
        return cpCodeFilename
    return code






async def printCodeVisible(codeVisible):
    while True:
        print(codeVisible[0])
        await asyncio.sleep(1)

async def cbCollect2(page:uc.Tab,helper:HelperSitecollect2) -> str:

    pixelRatio = await page.evaluate('window.devicePixelRatio')
    # this code is fundamentally not compatable with broken OCR. 
    if helper.settings.mainSettings['OCR']==0:
        raise NoOCRException

    #for later
    stopScratch = threading.Event()
    asyncStopEvent = asyncio.Event()



    # page.add_handler(uc.cdp.network.ResponseReceived,  lambda event: print('\nnetwork event => %s' % event.response.url))

    
    code = ""
    codeImageFilename = "./cache/chumbaCode.png"
    imageURI = [""]
    
    listen(page,imageURI,stopScratch,asyncStopEvent)


    # setup
    chumbaScratcherCacheFilename = "./cache/chumbaScratcher.jpeg"

    # await asyncio.to_thread(input)

    # NOTE USE THIS IN THE FUTURE FOR SCRATCHING
    keepScratching = await page.find('Keep Scratching')
    # keepScratchingPos = await keepScratching.get_position()
    keepScratching = await CoordsObj.createCoordsObj(page,keepScratching)
    if helper.settings.debug:
        print(f"{keepScratching=}")
    # await asyncio.to_thread(input)

    # screenshot "scratch here"
    # await page.wait_for(selector="#overlay")
    scratcher = await page.select_all("#scratch-canvas",include_frames=True)
    scratcher = scratcher[0]
    # await scratcher.save_screenshot(filename=chumbaScratcherCacheFilename)

    # get scratcher coords and save screenshot
    # print("screenshot")
    scratcherCoords = await scratcher.get_position()
    scratcherCoords = await createCoordsObj(page,scratcherCoords)
    if helper.settings.debug:
        print(f"{scratcherCoords=}")
    


    # print("try screenshot")
    await customScreenshotElement(page,scratcher,chumbaScratcherCacheFilename)
    # await asyncio.get_event_loop().run_in_executor(None,customScreenshot,scratcherCoords,chumbaScratcherCacheFilename)



    # finding bounding box of text (relative to box)
    
    boundingBox = chumbaOCR(chumbaScratcherCacheFilename)
    if helper.settings.debug:
        print(f"{boundingBox=}")

    keepScratching = await relativeCoordsObjPosition(scratcherCoords,keepScratching)

    if helper.settings.debug:
        print(f"{keepScratching=}")

    keepScratching.top = min(boundingBox['top'],keepScratching.top)
    keepScratching.left = min(boundingBox['left'],keepScratching.left)
    keepScratching.right = max(boundingBox['right'],keepScratching.right)
    keepScratching.bottom = max(boundingBox['bottom'],keepScratching.bottom)

    if helper.settings.debug:
        print(f"{keepScratching=}")

    

    # generate scratch coordinates for "scratch here" 
    
    # relative to box
    initialScratchCoords = chumbaGenerateCoords(scratcherCoords=scratcherCoords,boundingBox=keepScratching)
    if helper.settings.debug:
        print(f"preadjusted {initialScratchCoords=}")
    # relative to page 
    # i have a feeling this doesnt do anything
    for coord in initialScratchCoords:
        coord=coord+[scratcherCoords.left,scratcherCoords.top]
    
    if helper.settings.debug:
        print(f"{initialScratchCoords=}")

    # move to scratch box
    xInit = scratcherCoords.left+np.mean(np.random.randint(0,scratcherCoords.width,3))
    yInit = scratcherCoords.top+np.mean(np.random.randint(0,scratcherCoords.height,3))

    coordInit = [[int(xInit),int(yInit)]]
    await hmoveVGW2(page,coordInit)
    await page.sleep(np.mean(np.random.random(2))*0.5+0.03)






    # setup scratch and listen for finish
    scratchThread = threading.Thread(target = scratchEvent,args=(page,initialScratchCoords,scratcherCoords,stopScratch,asyncStopEvent))
    scratchThread.daemon = True

    # wait for codeVisible signal packet
    
    listen(page,imageURI,stopScratch,asyncStopEvent)
    # start scratch thread
    scratchThread.start()


    

    await asyncStopEvent.wait()

    pagui.mouseUp()

    scratchThread.join()

    # save image for ocr
    convertToImageFile(imageURI[0],codeImageFilename)

    # convert to string 
    
    code = singleOCR(codeImageFilename)
    
    # cleanup
    page.handlers = collections.defaultdict(list)
    # await page.get()

    
    # debug cleanup
    # debug.cancel()


    return code
    
async def cbCollect2Old(page:uc.Tab,helper:HelperSitecollect2) -> str:
    # this code is fundamentally not compatable with broken OCR. 
    if helper.settings.mainSettings['OCR']==0:
        raise NoOCRException

    #for later
    stopScratch = threading.Event()
    asyncStopEvent = asyncio.Event()



    # page.add_handler(uc.cdp.network.ResponseReceived,  lambda event: print('\nnetwork event => %s' % event.response.url))

    
    code = ""
    codeImageFilename = "./cache/chumbaCode.png"
    imageURI = [""]
    # debug=asyncio.create_task(printCodeVisible(codeVisible))
    # def listen(page:uc.Tab,imageURI:list[str],stopScratch:threading.Event,asyncStopEvent:asyncio.Event):
    listen(page,imageURI,stopScratch,asyncStopEvent)


    # setup
    chumbaScratcherCacheFilename = "./cache/chumbaScratcher.jpeg"

    # screenshot "scratch here"
    await page.wait_for(selector="#overlay")
    scratcher = await page.query_selector("#scratch-canvas")
    # await scratcher.save_screenshot(filename=chumbaScratcherCacheFilename)

    # get scratcher coords and save screenshot
    print("screenshot")
    scratcherCoords = await scratcher.get_position()
    scratcherCoords = await createCoordsObj(page,scratcherCoords)
    # print("try screenshot")
    # await asyncio.get_event_loop().run_in_executor(None,customScreenshot,scratcherCoords,chumbaScratcherCacheFilename)
    await customScreenshotElement(page,scratcherCoords,chumbaScratcherCacheFilename)




    # finding bounding box of text (relative to box)
    
    boundingBox = chumbaOCR(chumbaScratcherCacheFilename)

    # generate scratch coordinates for "scratch here" 
    
    # relative to box
    initialScratchCoords = chumbaGenerateCoords(scratcherCoords=scratcherCoords,boundingBox=boundingBox)
    
    # relative to page 
    # i have a feeling this doesnt do anything
    for coord in initialScratchCoords:
        coord=coord+[scratcherCoords.left,scratcherCoords.top]
    if helper.settings.debug:
        print(f"{initialScratchCoords=}")

    # move to scratch box
    xInit = scratcherCoords.left+np.mean(np.random.randint(0,scratcherCoords.width,3))
    yInit = scratcherCoords.top+np.mean(np.random.randint(0,scratcherCoords.height,3))

    coordInit = [[int(xInit),int(yInit)]]
    await hmoveVGW2(page,coordInit)
    await page.sleep(np.mean(np.random.random(2))*0.5+0.03)






    # setup scratch and listen for finish
    # stopScratch = threading.Event()
    # pixelRatio = await page.evaluate('window.devicePixelRatio')
    if helper.settings.debug:
        print('creating scratchThread')
    scratchThread = threading.Thread(target = scratchEvent,args=(page,initialScratchCoords,scratcherCoords,stopScratch,asyncStopEvent))
    scratchThread.daemon = True

    # wait for codeVisible signal packet
    # def listen(page:uc.Tab,imageURI:list[str],stopScratch:threading.Event,asyncStopEvent:asyncio.Event):
    listen(page,imageURI,stopScratch,asyncStopEvent)
    if helper.settings.debug:
        print('start scratch thread')
    # start scratch thread
    scratchThread.start()


    

    await asyncStopEvent.wait()

    pagui.mouseUp()

    scratchThread.join()




    
    
    # save image for ocr
    convertToImageFile(imageURI[0],codeImageFilename)
    # await page.get()

    # convert to string 
    
    code = singleOCR(codeImageFilename)
    
    # cleanup
    page.handlers = collections.defaultdict(list)
    # await page.get()

    
    # debug cleanup
    # debug.cancel()


    return code


# def scratchEvent(initialScratchCoords,scratcherCoords,stopScratch,asyncStopEvent:asyncio.Event):
#     task = asyncio.run(scratchEventAsync(initialScratchCoords,scratcherCoords,stopScratch))
#     # global stopScratch
#     # asyncio.run( asyncStopEvent.wait())
#     # task.cancel()

# async def scratchEventAsync(initialScratchCoords,scratcherCoords,stopScratch:threading.Event):


#     # scratch
#     pagui.mouseDown()
#     await hmoveVGW2(initialScratchCoords,speedKeyword="scratch")
#     await asyncio.sleep(1)
#     # test = input()
#     # continue scratching until finish
#     scratcherCoordsDict = {"top":0,"right":scratcherCoords.right-scratcherCoords.left,"bottom":scratcherCoords.bottom-scratcherCoords.top,"left":0}
#     while not stopScratch.is_set():
#         continueScratch = chumbaGenerateCoords(scratcherCoords,scratcherCoordsDict,scratchCount=3)
#         await hmoveVGW2(continueScratch,speedKeyword="scratch")
#         await humanPause(0.5)



def listen(page:uc.Tab,imageURI:list[str],stopScratch:threading.Event,asyncStopEvent:asyncio.Event):
    test=[]
    async def handler(evt:uc.cdp.network.ResponseReceived):
        # get ajax requests
        # if (evt.type_ is uc.cdp.network.ResourceType.IMAGE) and "png" in evt.response.url:
        # print(evt.type_)
        # print(evt.response.url)
        if (evt.type_ is uc.cdp.network.ResourceType.IMAGE):
            print("image detected")
            # networkRequests.append([evt.response.url])
            # global last_xhr_request
            # last_xhr_request = time.time()
            # global codeVisible
            # codeVisible[0]=True
            nonlocal imageURI
            nonlocal stopScratch
            imageURI[0] = evt.response.url
            print("image received")
            stopScratch.set()
            asyncStopEvent.set()
        print("exit processing response")

    page.add_handler(uc.cdp.network.ResponseReceived, handler)
    # page.add_handler(uc.cdp.network.ResponseReceived,  lambda event: print('\nnetwork event => %s' % event.response.url))


    print("added handler")



def convertToImageFile(image_uri:str,filename:str)->None:#
    # The 'data:image/png;base64,' part should be removed
    # If it's a different image format, adjust accordingly.
    header = "data:image/png;base64,"
    if image_uri.startswith(header):
        image_uri = image_uri[len(header):]

    # Decode the base64 string
    image_data = base64.b64decode(image_uri)

    # Write the decoded image data to a file
    with open(filename, 'wb') as file:
        file.write(image_data)
    print(f"Image saved as {filename}")
