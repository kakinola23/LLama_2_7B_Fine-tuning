# -*- coding: utf-8 -*-
"""Zero_Shot_Inference.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1UoNaS7sSTLI2tgEl5sRAgPeGWdTMpqpy
"""

!pip uninstall -y tensorflow --quiet
!pip install ludwig
!pip install ludwig[llm]

!pip uninstall -y tensorflow --quiet
!pip install git+https://github.com/ludwig-ai/ludwig.git@master --quiet
!pip install "git+https://github.com/ludwig-ai/ludwig.git@master#egg=ludwig[llm]" --quiet

"""### **Setup Your HuggingFace Token**

Obtain a [HuggingFace API Token](https://huggingface.co/settings/tokens).

"""

import locale; locale.getpreferredencoding = lambda: "UTF-8"
import logging
import yaml
import os
import torch
import getpass



os.environ["HUGGING_FACE_HUB_TOKEN"] = getpass.getpass("Token:")
assert os.environ["HUGGING_FACE_HUB_TOKEN"]

import numpy as np; np.random.seed(123)
import pandas as pd

df = pd.read_json("https://raw.githubusercontent.com/sahil280114/codealpaca/master/data/code_alpaca_20k.json")

# We're going to create a new column called `split` where:
# 90% will be assigned a value of 0 -> train set
# 5% will be assigned a value of 1 -> validation set
# 5% will be assigned a value of 2 -> test set
# Calculate the number of rows for each split value
total_rows = len(df)
split_0_count = int(total_rows * 0.9)
split_1_count = int(total_rows * 0.05)
split_2_count = total_rows - split_0_count - split_1_count

# Create an array with split values based on the counts
split_values = np.concatenate([
    np.zeros(split_0_count),
    np.ones(split_1_count),
    np.full(split_2_count, 2)
])

# Shuffle the array to ensure randomness
np.random.shuffle(split_values)

# Add the 'split' column to the DataFrame
df['split'] = split_values
df['split'] = df['split'].astype(int)

# We can use 2000 rows for this project
df = df.head(n=2000)

"""- **Zero Shot Inference**

"""

from ludwig.api import LudwigModel
# Specify the path to your YAML configuration file
config_file_path = 'zero_shot_config.yaml'

# Initialize the model using the YAML configuration
model = LudwigModel(config=config_file_path, logging_level=logging.INFO)

# 30 rows from the dataset
results = model.train(dataset=df[:30])
# Now, you can use the model for various tasks, such as training, prediction, etc.

test_examples = pd.DataFrame([
      {
            "instruction": "Create an array of length 7 containing all even numbers between 1 and 14.",
            "input": ''
      },
      {
            "instruction": "Generate the square root of 4",
            "input": "",
      },
      {
            "instruction": "Generate an array of length 12 with numbers that are divisible by 4 up to 48",
            "input": ""
      },
      {
            "instruction": "Generate a function that print all the missing data from a dataset",
            "input": "",
      },
      {
            "instruction": "Write a nested loop to print every combination of numbers between 0 and 7.",
            "input": "",
      },

      {
            "instruction": "Create a function that finds the maximum number in a given list.",
            "input": "",
      },
      {
            "instruction": "Design a class to store employee names, ages, and salaries.",
            "input": "",
      },
      {
            "instruction": "Create an array of length 6 containing all odd numbers between 1 and 11",
            "input": "",
      },
      {
            "instruction": "Generate an array of length 10 with numbers that are divisible by 5 up to 50.",
            "input": "",
      },
      {
            "instruction": "Write a nested loop to print every combination of letters 'A' to 'C' and numbers 1 to 3.",
            "input": "",
      },
      {
            "instruction": "Create a function called kunle_average that calculates the average of numbers in a given list.",
            "input": "",
      },
      {
            "instruction": "Print out the values in the following dictionary.",
            "input": "my_dict = {\n  'name': 'Sarah',\n  'age': 25,\n  'city': 'Plano'\n}",
            },
      ])

predictions = model.predict(test_examples)[0]
for input_with_prediction in zip(test_examples['instruction'], test_examples['input'], predictions['output_response']):
  print(f"Instruction: {input_with_prediction[0]}")
  print(f"Input: {input_with_prediction[1]}")
  print(f"Generated Output: {input_with_prediction[2][0]}")
  print("\n\n")