from fastapi import Body, FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, constr
from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline,AutoModelForQuestionAnswering
import uvicorn
import string
#for iow
from parrot import Parrot

class IOWRequest(BaseModel):
    content: constr(max_length=512000)


app = FastAPI(
    title="ryanlai",
    description="demo",
    version="0.1.0",
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


#iow model loading
parrot = Parrot(model_tag="prithivida/parrot_paraphraser_on_T5")


@app.get("/")
async def root():
    return RedirectResponse("docs")


@app.get("/page/{page_name}", response_class=HTMLResponse)
async def page(request: Request, page_name: str):
    return templates.TemplateResponse(f"{page_name}.html", {"request": request})


@app.post("/iow")
async def iow(
    iow_request: IOWRequest = Body(
        None,
        
    )
):
    print("-"*100)
    print("Input_phrase: ", iow_request.content)
    print("-"*100)
    #test="The Taiwan Professional Baseball Warriors defeated the Phillies 5-3 today."
    split_contents=iow_request.content.split('.')
    split_contents[-1]=''
    for sentent in split_contents:
        sentent+='.'
        print('sentent: '+sentent+'*')
    #print(split_contents)
    return_para_phrases=""
    sentence_no=0#句子編號
    for sentent in split_contents:
        sentence_no+=1
        if sentent!='.':
            para_phrases = parrot.augment(input_phrase=sentent, use_gpu=False)
            print(type(para_phrases))
            if para_phrases !=None:
                p_para_phrases=para_phrases[0][0].capitalize()+'.'#字首大寫
                return_para_phrases+=p_para_phrases
                print("round:"+str(sentence_no)+"-"*100)
                print("new_sentence:"+p_para_phrases)
                print("-"*100)


#    para_phrases = parrot.augment(input_phrase=iow_request.content, use_gpu=False)
#    print(para_phrases)


#    for para_result in para_phrases:
#        print("-"*100)
#        print("Output_phrase: ",para_result,para_result[0],para_result[1])
#        print("-"*100)
    print("-"*100)
    print("return_phrase")
    print(return_para_phrases)

    
    return return_para_phrases



if __name__== "__main__":
    uvicorn.run(app='iow:app',host='0.0.0.0',port=8000,reload=True,debug=True)