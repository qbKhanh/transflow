

python3 pipeline.py \
    --image dataset/abc \
    --output TEST \
    --device cuda:0 \
    --dt-weight checkpoints/comic-speech-bubble-detector.pt \
    --save-dt-output \
    --ocr-lang jp \
    --save-ocr-output \