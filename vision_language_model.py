from abc import ABC, abstractmethod
from PIL import Image
from read_questions import read_questions
import os
from read_write_json import read_json, write_json
from typing import List, Union, Dict, Any
from torchvision import transforms

class VisionLanguageModel(ABC):

    def __init__(self, name: str = None, image_folder: str = "images", questions_file_path: str = "questions.js", json_file_path: str = "image_data.js"):
        self.name = name
        self.image_folder = image_folder
        self.questions_file_path = questions_file_path
        self.json_file_path = json_file_path

    @abstractmethod
    def answer_question(self, image: Image.Image, question: str) -> str:
        """
        Takes a PIL image object and a question about the image, and returns the answer.
        
        :param image: A PIL Image object
        :param question: The question about the image
        :return: The answer to the question
        """
        pass
    
    def answer_questions_for_images(self) -> list:

        json_data = read_json(self.json_file_path)
        questions = read_questions(self.questions_file_path)

        print(f"Answering questions for {self.name}...")
        print(f"Continuing on json data: {self.json_file_path}")
        print(f"With questions data: {self.questions_file_path}")
        
        for index, image_filename in enumerate(os.listdir(self.image_folder)):
            if image_filename.endswith(('.jpg', '.jpeg', '.png')):
                image_path = os.path.join(self.image_folder, image_filename)
                image = Image.open(image_path).convert("RGB")
                print(f"Answering questions for {image_filename}...")
                print(f"Image path: {image_path}")

                # Check if the image filename is in the data, if not, add it
                if image_filename not in json_data:
                    json_data[image_filename] = {f"{self.name}_answers": {}}
                    print(f"Adding {image_filename} to json data")

                # Check if the model is not yet in the data structure
                if f"{self.name}_answers" not in json_data[image_filename]:
                    json_data[image_filename][f"{self.name}_answers"] = {}
                    print(f"Adding {self.name} for {image_filename} to json data")

                data = json_data[image_filename]

                for question in questions:
                    label = question["label"]
                    question_text = question["question"]

                    print(f"Answering question: {label}")
                    
                    # Check if the question is already answered
                    if label in data[f"{self.name}_answers"]:
                        print(f"Question {label} already answered, skipping...")
                        continue
                    
                    # Answer the question and update the data
                    data[f"{self.name}_answers"][label] = self.answer_question(image, question_text)

            if index % 100 == 0:
                write_json(self.json_file_path, json_data)

        write_json(self.json_file_path, json_data)

            