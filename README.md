# Optical Character Recognition (OCR) - Hidden Markov Model

## Overview

This project aims to implement a 1st order Hidden Markov Model (HMM) for correcting Optical Character Recognition (OCR) outputs. 
The model will use observable sensor outputs and hidden states representing actual letters. 
The transition and emission probabilities will be estimated using provided data, and the model will be evaluated on a separate dataset.

## Problem Statement

- The files include 60244 actual words and their OCR outputs.
- First 50000 of words are used for estimating the transition and emittance probabilities.
- The rest of the data is used for performance analysis. 10244 most likely word sequences is estimated and compared with the actual words.

## Files Provided  

- data_actual_words.txt: Contains a list of actual words.
- data_ocr_outputs.txt: Corresponding OCR readings for the actual words.

