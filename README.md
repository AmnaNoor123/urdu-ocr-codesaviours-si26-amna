# Urdu OCR Project | Code Saviours SI-26 | Amna Noor

## What is OCR (Optical Character Recognition)?

OCR is a technology that helps recognize text, images, drawings, and hand written notes and converts them into digital text that a computer can understand, because when we simply put a picture, the computer doesn't understand what's in it, so OCR extracts text and data from the image. Example: Google Lens extracts data from an image.

## Why is Urdu OCR harder than English OCR?

Urdu OCR is more difficult than English OCR because English is written left to right and its letters are separate, not connected to each other. Urdu, on the other hand, is written right to left, which is already a challenge for the computer to process. Also, Urdu letters are joined together within a word, making it hard for the computer to understand where one letter ends and another begins, or where a word starts and ends.

## What are 2 real-world situations where Urdu OCR would be useful?

Urdu OCR can be used in apps like Google Lens to scan and extract text from Urdu poetry, making it easy to read, copy, or search the poetry digitally. Another example is scanning official documents like a Nikahnama (marriage certificate), which are usually written in Urdu, so OCR can help convert them into digital text for easy storage and record-keeping.

## Dataset

The full image dataset contains 200 images across 6 categories: Newspaper, Books, Sign boards, Synthetic (generated with Nastaliq and Naskh fonts), Handwritten, and Other.

Due to GitHub file upload limitations, the full image dataset is available here: [Dataset](https://drive.google.com/file/d/1_Tq2I7q33ndChQqyQR1VCMSOTNZ-sw9E/view?usp=sharing). The `labels.csv` file in this repository contains ground-truth text for all 200 images.

## Why We Need a Better Model

To understand the scope of the Urdu OCR problem, we tested Tesseract (a popular general-purpose OCR engine) on 5 sample images from the full 200-image dataset — a mix of a full sentence, newspaper text, and isolated Urdu characters.

**Image 1: م_96.png**
- Actual text: `م`
- Tesseract output: *(blank)*
- What went wrong: Isolated single letter — with no surrounding context, Tesseract failed to detect anything and returned a blank output.

**Image 2: 6652.png**
- Actual text: `والے کشمیر سیمینار کے ساتھ بھر پو تعاون کا فیصلہ`
- Tesseract output: `الات ناک مت گر اھ`
- What went wrong: The entire sentence was misread — not a single word came out correctly, and word order was also lost. The newspaper scan's low contrast/noise made this especially hard for Tesseract.

**Image 3: ذ_99.png**
- Actual text: `ذ`
- Tesseract output: `الا`
- What went wrong: Tesseract misread the isolated letter ذ as something entirely different. Isolated characters keep failing — whether the output is blank or garbled.

**Image 4: Screenshot 2026-07-21 184154.png**
- Actual text: `ٹی ایل پی سربراہ سعد رضوی اور ان کے بھائی کی گمشدگی کا معمہ برقرار`
- Tesseract output: `ٹی ئیل پی سریراہ سحد رضوی اور ات کے بھاکی کی گمعدگی کا مسا یرظراں...` (plus extra garbage lines and stray symbols)
- What went wrong: The closest match — several words were recognized, but nearly every word had a small spelling distortion, and extra nonsense lines/symbols were generated at the end.

**Image 5: 10003.png**
- Actual text: `فروخت اور قیمت خرید میں بالترتیب 21 پیسے اور 20`
- Tesseract output: `فا یی نپ 2ا1`
- What went wrong: Only a faint trace of the numbers survived; the rest of the sentence came out completely garbled and unreadable.

This run confirms a consistent pattern: isolated single letters consistently produce either a blank or garbled output, since Tesseract relies on surrounding context it doesn't have; full sentences/phrases are either completely misread or come out with mostly-recognizable words marred by spelling errors and extra garbage lines. This reinforces the limitations of Tesseract's pretrained Urdu model on connected/cursive script — confirming the need for a custom-trained OCR model, which was built starting in Week 3.

## Data Pipeline Note

During Week 4 training, a data pipeline bug was diagnosed and fixed: an outdated `labels.csv` on GitHub (with filename mismatches against the actual image files) was causing 31 of 200 images to be silently dropped during dataset loading. The corrected `labels.csv`, verified against all 200 image files, is now the version tracked in this repository, and training now correctly uses the full 200-image dataset.

A second, separate bug was also found and fixed during Week 4: label sequences were padded to a fixed length without masking the padding tokens as `-100`, so the model was initially learning to predict padding instead of real characters. This was corrected before the final training run described below.

## Model Training — TrOCR Fine-tuning (Week 3–4)

We fine-tuned `microsoft/trocr-base-printed` (a Vision Encoder-Decoder transformer) on the 200-image labeled dataset using transfer learning, with an 80/20 train/test split (160 train / 40 test), batch size 4, AdamW optimizer at lr=5e-5, for **12 epochs** (after the fixes above).

**Training loss trend:** Loss stayed flat between **3.1 and 3.3 across all 12 epochs** — it did not meaningfully decrease with more training, unlike what a normal fine-tuning run would show.

**Evaluation result:** 0.0% exact-match accuracy (0/40) on the held-out test set. Predictions consistently decoded as `�` (replacement characters), blank, or repeated single characters instead of valid Urdu text.

**Why this happened:** `microsoft/trocr-base-printed` uses a `RobertaTokenizer` — a byte-level tokenizer trained on English/Latin text. Since Arabic-script characters (used for Urdu) weren't part of its original vocabulary, each Urdu character has to be reconstructed from a precise sequence of byte-level tokens; if even one byte in that sequence is predicted incorrectly, the whole character fails to decode. The flat loss across all 12 epochs (rather than a normal decreasing curve) shows the model wasn't meaningfully learning this byte-sequence mapping at all — not just an accuracy-metric artifact, but a genuine training plateau.

**Example mismatches:**
- Actual: `علم بڑی دولت ہے، ہم اسے حاصل کرنے کے لیے صرف محن` → Predicted: `اااااااااااااااااااا` (model just repeats "ا")
- Actual: `آج کا موسم خوشگوار ہے` → Predicted: `��������������������`
- Actual: single letters (`ل`, `ظ`, `ٹ`, `ذ`, `ط`, `ع`, `گ`, `م`) → Predicted: blank or invalid characters

**Takeaway:** A pretrained English OCR model's tokenizer is a hard bottleneck for Urdu — more fine-tuning data or epochs alone won't fix this, since the underlying vocabulary can't represent Urdu characters efficiently (confirmed here by 4x more epochs and a corrected, full 200-image dataset still producing a flat loss curve). A model with a multilingual or Urdu-aware tokenizer (e.g., an mBERT/XLM-R-based decoder, or an Urdu-specific OCR checkpoint) is a more realistic direction for future work.

## Pivoting to EasyOCR (Week 5)

Given the internship timeline, and since the TrOCR limitation was architectural rather than a training issue, the project pivoted to **EasyOCR** — a pretrained OCR library with native Urdu (`ur`) language support — to deliver a genuinely working live demo.

Tested on multiple real and synthetic Urdu images, EasyOCR produced largely accurate, readable extractions without any fine-tuning — a significant improvement over TrOCR's output. For example:
- Actual: `بارش کے بعد ہوا خوشگوار ہو گئی` → Predicted: `بارش کے بعد ہوا خوشگوار ہو` (near-exact match)
- Actual: `پاکستان زندہ باد` → Predicted: `اکستا . زندہ باد` (mostly correct)

Performance was noticeably weaker on handwritten samples, which is expected — EasyOCR's pretrained model is optimized for printed/typed text.

## Live Demo

🔗 **[Try the app here](https://urdu-ocr-codesaviours-si26-amna-jsxqqbxcat8xugyguf4soy.streamlit.app/)**

Deployed on **Streamlit Community Cloud**. (HuggingFace Spaces now requires a paid plan for Gradio/Docker SDKs, so Streamlit was used as a free alternative to deliver a permanent, working live demo.)

## Run It Locally

```bash
git clone <your-repo-url>
cd <your-repo-folder>
pip install -r requirements.txt
streamlit run app.py
```

## Results Summary

| Approach | Result |
|---|---|
| Tesseract (baseline, no training) | Fails on isolated letters (blank/garbled); full sentences mostly or completely misread |
| TrOCR (fine-tuned, 12 epochs) | 0.0% exact-match accuracy (0/40) — tokenizer/script mismatch, not a training-time issue |
| EasyOCR (used for live demo) | Largely accurate on printed/synthetic Urdu text, no fine-tuning required; weaker on handwriting |

## What Would Improve This

- A multilingual or Urdu-aware tokenizer/decoder instead of an English-only tokenizer
- A larger, more diverse training dataset (500+ images)
- Better handwriting samples and augmentation for handwritten text specifically

## Credit

Amna — Built during the Code Saviours ML/AI Internship, Batch SI-26.
