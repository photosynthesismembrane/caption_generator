# Caption Generator

This repository can be used to generate image captions using vision language models: Llava, Cogvlm and/or Deepseek. 

Install:
```
git clone https://github.com/deepseek-ai/DeepSeek-VL.git && \
mv DeepSeek-VL deepseek_vl && \
python -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt
```

Run:
```
python answer_questions.py --image_folder="images" --questions_file_path="questions.js" --json_file_path="captions.js" --model="all"
```

VLM's can be run seperately by setting --model to either "llava", "cogvlm" or "deepseek". When set to "all", each VLM is run sequentially, only one model is allocated on the gpu at the time. 

