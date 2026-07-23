# urdu-ocr-codesaviours-si26-amna
Urdu OCR Project | Code Saviours SI-26 | Amna Noor

**What is OCR (Optical Character Recognition)?**

OCR is a technology that helps recognize text, images, drawings, and hand written notes and converts them into digital text that a computer can understand, because when we simply put a picture, the computer doesn't understand what's in it, so OCR extracts text and data from the image.
Example: Google Lens extracts data from an image.

**Why is Urdu OCR harder than English OCR?**

Urdu OCR is more difficult than English OCR because English is written left to right and its letters are separate, not connected to each other. Urdu, on the other hand, is written right to left, which is already a challenge for the computer to process. Also, Urdu letters are joined together within a word, making it hard for the computer to understand where one letter ends and another begins, or where a word starts and ends.

**What are 2 real-world situations where Urdu OCR would be useful?**

Urdu OCR can be used in apps like Google Lens to scan and extract text from Urdu poetry, making it easy to read, copy, or search the poetry digitally. Another example is scanning official documents like a Nikahnama (marriage certificate), which are usually written in Urdu, so OCR can help convert them into digital text for easy storage and record-keeping.

## Dataset Images
Due to GitHub file upload limitations, the full collected image dataset (133 images across 5 categories: newspaper, books, signboards, synthetic, other) is available here:
[Dataset - Google Drive Link](https://drive.google.com/file/d/1_Tq2I7q33ndChQqyQR1VCMSOTNZ-sw9E/view?usp=sharing)

The `labels.csv` file with ground-truth text for all images is available in this repository.

## Why We Need a Better Model

To understand the scope of the Urdu OCR problem, we tested Tesseract (a popular 
general-purpose OCR engine) on 5 of our processed images — a mix of a full 
sentence and isolated Urdu characters.

**Image 1: urdu_2.png**
- Actual text: آج کا موسم خوشگوار ہے
- Tesseract output: آج کا موم خوشوارے
- What went wrong: Words got merged and mispelled — "موسم" became "موم" (letters 
  dropped), and "خوشگوار ہے" became "خوشوارے" (multiple letters missing, words 
  incorrectly joined).

**Image 2: ذ_98.png**
- Actual text: ذ
- Tesseract output: 0
- What went wrong: A single Urdu letter was misread entirely as the number "0" — 
  complete character misclassification.

**Image 3: س_97.png**
- Actual text: س
- Tesseract output: (blank)
- What went wrong: Tesseract failed to detect any text at all — isolated Urdu 
  characters without surrounding context are not recognized.

**Image 4: ا_974.png**
- Actual text: ا
- Tesseract output: (blank)
- What went wrong: Same as above — no text detected.

**Image 5: ا_973.png**
- Actual text: ا
- Tesseract output: (blank)
- What went wrong: Same as above — no text detected.

**Tesseract fails on Urdu because** it struggles with the connected, cursive 
nature of Urdu script — letters change shape depending on their position in a 
word, and Tesseract's model isn't well-trained to handle this joining behavior. 
It performs worst on single isolated characters (returning blank output or 
mistaking them for unrelated symbols entirely), and even on full sentences it 
drops or merges letters, producing text that looks similar to the original but 
is factually incorrect. This confirms the need for a custom-trained OCR model 
specifically built for Urdu's script structure.

