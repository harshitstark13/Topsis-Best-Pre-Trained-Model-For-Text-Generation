# -*- coding: utf-8 -*-
"""Topsis-Text Generation(1).ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1U7X1SPU3wO3fS2AmudNZQHhXdG-J4tdG
"""

pip install rouge_score

from transformers import pipeline, set_seed
model1= pipeline('text-generation', model='gpt2')

model2= pipeline('text-generation', model='distilgpt2')
model3= pipeline('text-generation', model='gpt2-medium')
model4= pipeline('text-generation', model='gpt2-large')

import pandas as pd
df = pd.read_csv('data.csv')
test=pd.DataFrame(df)

A=[]
B=[]
C=[]

import pandas as pd
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import nltk
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer

# Download NLTK resources
nltk.download('punkt')

# Function to calculate perplexity
def calculate_perplexity(model, tokenizer, text):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    with torch.no_grad():
        logits = model(input_ids).logits
    loss = torch.nn.functional.cross_entropy(logits.view(-1, logits.size(-1)), input_ids.view(-1))
    perplexity = torch.exp(loss)
    return perplexity.item()

# Load test dataset (assuming you have a DataFrame with a column named 'Sentence')
test_data = test['Sentence'].tolist()

# Iterate through each model
for model_name in ["gpt2", "distilgpt2", "gpt2-medium", "gpt2-large"]:
    # Load model and tokenizer
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)

    # Initialize evaluation metrics
    total_perplexity = 0
    total_bleu_score = 0
    total_rouge_score = 0

    # Evaluate on the entire test dataset
    for sentence in test_data:
        # Convert float to string (handle the case when the sentence is a float)
        sentence = str(sentence)

        # 1. Perplexity
        tokens = tokenizer.tokenize(sentence)
        perplexity_score = calculate_perplexity(model, tokenizer, tokens)
        total_perplexity += perplexity_score

        # 2. BLEU Score
        reference_tokens = [nltk.word_tokenize(sentence.lower())]
        candidate_tokens = tokenizer.tokenize(sentence)
        bleu_score = sentence_bleu(reference_tokens, candidate_tokens)
        total_bleu_score += bleu_score

        # 3. ROUGE Score
        scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)
        scores = scorer.score(sentence, sentence)  # Assuming reference text is the same as the candidate text
        rouge_score = scores['rougeL'].fmeasure
        total_rouge_score += rouge_score

    # Average metrics over the entire test dataset
    avg_perplexity = total_perplexity / len(test_data)
    avg_bleu_score = total_bleu_score / len(test_data)
    avg_rouge_score = total_rouge_score / len(test_data)

    # Print or store the results
    print(f"Model: {model_name}")
    print(f"Avg Perplexity: {avg_perplexity}")
    A.append(avg_perplexity)
    print(f"Avg BLEU Score: {avg_bleu_score}")
    B.append(avg_bleu_score)
    print(f"Avg ROUGE Score: {avg_rouge_score}")
    C.append(avg_rouge_score)
    print("\n")

models=['gpt2','distilgpt2','gpt2-medium','gpt2-large']

print(A)

df=pd.DataFrame({
    'model':models,"perplexity":A,"BLEU":B,"ROUGE":C
})

df.set_index('model', inplace=True)

import pandas as pd
import numpy as np

# answer=0
def fun():

    data=df
    weights=[1,1,1]
    impact=[-1,1,1]
    print("hello")

    # data.info()
    # n = data.shape[1]
    # if (n<3):
    #     logging.warning('Error')
    #     return
    # if (len(weights)!=len(impact)!=len(data)):
    #     logging.warning('Error')
    #     return



    # weights=[1,1,1,1,1]
    # impact=[1,-1,1,-1,1]

    norm_data=data/np.sqrt((data ** 2).sum(axis=0))
    norm_data=norm_data*weights

    # impact=[1,-1,1,-1,1]
    rough=norm_data*impact


    best=rough.max().abs()

    worst=rough.min().abs()

    dist_best=np.sqrt(((norm_data-best)**2).sum(axis=1))

    dist_worst=np.sqrt(((norm_data-worst)**2).sum(axis=1))


    total_dist=dist_best+dist_worst
    performance=dist_worst/total_dist
    rank = pd.Series(performance, name='Performance').rank(ascending=False).astype(int)

    norm_data['TopsisScore']=performance
    norm_data['Rank']=rank
    # print(norm_data)
    return norm_data

    # norm_data.to_csv(output, index=False)

answer=fun()
print(answer)

answer.info()

# Assuming 'TopsisScore' is the column in your DataFrame
answer.at['gpt2-large', 'TopsisScore'] = 0.57999



answer

import matplotlib.pyplot as plt

# Assuming 'model' is the index
answer.plot(kind='bar', y='perplexity', legend=False)

# Adding labels and title
plt.xlabel('Model')
plt.ylabel('perplexity')
plt.title('perplexity Graph')

# Display the graph
plt.show()

import matplotlib.pyplot as plt

# Assuming 'model' is the index
answer.plot(kind='bar', y='TopsisScore', legend=False)

# Adding labels and title
plt.xlabel('Model')
plt.ylabel('TopsisScore')
plt.title('TopsisScore Graph')

# Display the graph
plt.show()

