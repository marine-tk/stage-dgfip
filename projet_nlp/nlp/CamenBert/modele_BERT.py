#%%

## Importation des librairies

# Importing standard libraries for every machine/deep learning pipeline
import pandas as pd

import torch

from tqdm import tqdm, trange

import numpy as np


# Importing specific libraries for data prerpcessing, model archtecture choice, training and evaluation
from sklearn.model_selection import train_test_split

from keras.preprocessing.sequence import pad_sequences

from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

from transformers import CamembertTokenizer, CamembertForSequenceClassification

from transformers import AdamW

import torch.optim as optim

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

import seaborn as sns

#%%

# Defining constants
epochs = 5

MAX_LEN = 128

batch_size = 16

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')


#%%

# Load the dataset, I selected only 5000 sample because of memory limitation
df = pd.read_csv('/content/database.csv') #.sample(5000).reset_index(drop=True)

del df['Unnamed: 0']

df = df[df['Sentiment'] != 'Neutre']

df['Sentiment'] = df['Sentiment'].map({'Positif':1,
                          'Négatif':0})

df.head()

#%%

# Initialize CamemBERT tokenizer
tokenizer = CamembertTokenizer.from_pretrained('camembert-base',do_lower_case=True)
   

#%%

# Creates list of texts and labels
text = df['Avis'].to_list()

labels = df['Sentiment'].to_list()

#user tokenizer to convert sentences into tokenizer
input_ids  = [tokenizer.encode(sent,add_special_tokens=True,max_length=MAX_LEN) for sent in text]

# Pad our input tokens
input_ids = pad_sequences(input_ids, maxlen=MAX_LEN, dtype="long", truncating="post", padding="post")

# Create attention masks
attention_masks = []
# Create a mask of 1s for each token followed by 0s for padding
for seq in input_ids:
    
    seq_mask = [float(i>0) for i in seq]  
    
    attention_masks.append(seq_mask)

   
#%%

# Use train_test_split to split our data into train and validation sets for training
train_inputs, validation_inputs, train_labels, validation_labels, train_masks, validation_masks = train_test_split(input_ids, labels, attention_masks,
                                                            random_state=42, test_size=0.1)

# Convert all of our data into torch tensors, the required datatype for our model
train_inputs = torch.tensor(train_inputs)

validation_inputs = torch.tensor(validation_inputs)

train_labels = torch.tensor(train_labels)

validation_labels = torch.tensor(validation_labels)

train_masks = torch.tensor(train_masks)

validation_masks = torch.tensor(validation_masks)

# Create an iterator of our data with torch DataLoader. This helps save on memory during training because, unlike a for loop, 
# with an iterator the entire dataset does not need to be loaded into memory

train_data = TensorDataset(train_inputs, train_masks, train_labels)

train_sampler = RandomSampler(train_data)

train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=batch_size)

validation_data = TensorDataset(validation_inputs, validation_masks, validation_labels)

validation_sampler = SequentialSampler(validation_data)

validation_dataloader = DataLoader(validation_data, sampler=validation_sampler, batch_size=batch_size)
   
#%%

model = CamembertForSequenceClassification.from_pretrained("camembert-base", num_labels=2)

model.to(device)
   
    
#%%

param_optimizer = list(model.named_parameters())

no_decay = ['bias', 'gamma', 'beta']

optimizer_grouped_parameters = [
    {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
     'weight_decay_rate': 0.01},
    {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
     'weight_decay_rate': 0.0}
]

optimizer = AdamW(optimizer_grouped_parameters, lr=2e-5, eps=10e-8)

#%%

# Function to calculate the accuracy of our predictions vs labels
def flat_accuracy(preds, labels):
    
    pred_flat = np.argmax(preds, axis=1).flatten()
    
    labels_flat = labels.flatten()
    
    return np.sum(pred_flat == labels_flat) / len(labels_flat)

#%%

# Store our loss and accuracy for plotting if we want to visualize training evolution per epochs after the training process
train_loss_set = []

# trange is a tqdm wrapper around the normal python range
for _ in trange(epochs, desc="Epoch"):  
    # Tracking variables for training
    tr_loss = 0
    
    nb_tr_examples, nb_tr_steps = 0, 0
  
    # Train the model
    model.train()
    
    for step, batch in enumerate(train_dataloader):
        
        # Add batch to device CPU or GPU
        batch = tuple(t.to(device) for t in batch)
        
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch
        
        # Clear out the gradients (by default they accumulate)
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(b_input_ids,token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
        
        # Get loss value
        loss = outputs[0]
        
        # Add it to train loss list
        train_loss_set.append(loss.item())    
        
        # Backward pass
        loss.backward()
        
        # Update parameters and take a step using the computed gradient
        optimizer.step()
    
        # Update tracking variables
        tr_loss += loss.item()
        
        nb_tr_examples += b_input_ids.size(0)
        
        nb_tr_steps += 1

    print("Train loss: {}".format(tr_loss/nb_tr_steps))
    
    


    # Tracking variables for validation
    eval_loss, eval_accuracy = 0, 0
    
    nb_eval_steps, nb_eval_examples = 0, 0
    
    # Validation of the model
    model.eval()
    
    # Evaluate data for one epoch
    for batch in validation_dataloader:
        
        # Add batch to device CPU or GPU
        batch = tuple(t.to(device) for t in batch)
        
        # Unpack the inputs from our dataloader
        b_input_ids, b_input_mask, b_labels = batch
        
        # Telling the model not to compute or store gradients, saving memory and speeding up validation
        with torch.no_grad():
            
            # Forward pass, calculate logit predictions
            outputs =  model(b_input_ids,token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)
            
            loss, logits = outputs[:2]
    
        # Move logits and labels to CPU if GPU is used
        logits = logits.detach().cpu().numpy()
        
        label_ids = b_labels.to('cpu').numpy()

        tmp_eval_accuracy = flat_accuracy(logits, label_ids)
    
        eval_accuracy += tmp_eval_accuracy
        
        nb_eval_steps += 1

    print("Validation Accuracy: {}".format(eval_accuracy/nb_eval_steps))

#%%













    
