# Caption Generator

This repository can be used to generate image captions using vision language models: Llava, Cogvlm and/or Deepseek.  

## Install:
```
git clone https://github.com/deepseek-ai/DeepSeek-VL.git && \
mv DeepSeek-VL deepseek_vl && \
python -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt
```
When generating captions with the Deepseek model, it requires to clone its github repository. For the models Llava and Cogvlm, they will be downloaded from Huggingface automatically when running the program as described below.  

## Run:
```
python answer_questions.py --image_folder="images" --questions_file_path="questions.js" --model="all" --json_file_path="captions.js"
```

*Images:*  
The captions will be generated for all the images in a specified folder --image_folder="images".

*Questions:*  
You can generate one or multiple captions per image, based on a set of questions. The questions must come in the following .js format, replacing <question_label_#> and <Question #> with your custom request:

```
const questions = [
    {"label": "<question_label_1>", "question": "<Question 1>"},
    {"label": "<question_label_2>", "question": "<Question 2>"},
    {"label": "<question_label_3>", "question": "<Question 3>"},
    {"label": "<question_label_4>", "question": "<Question 4>"},
    {"label": "<question_label_5>", "question": "<Question 5>"}
];
```

*Models:*  
VLM's can be run seperately by setting --model to either "llava", "cogvlm" or "deepseek". When set to "all", each VLM is run sequentially, only one model is allocated on the gpu at the time. 

*Captions:*  
The resulting captions will be saved to the specified file --json_file_path="captions.js" in a json format.

> The questions and captions are formatted in a JavaScript file in order for the results to be displayed easily on a website interface, which is implemented in the repository: [caption_interface](https://github.com/photosynthesismembrane/caption_interface)
