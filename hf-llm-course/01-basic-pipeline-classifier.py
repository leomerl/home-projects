from transformers import pipeline

classifier = pipeline("sentiment-analysis")
print(classifier(["The astronaut is playing basketball",]))

textGenerator = pipeline("text-generation")
print(textGenerator("The astronaut is playing basketball", max_length=50))

featureExtractor = pipeline('feature-extraction')
print(featureExtractor("The astronaut is playing basketball", max_length=50))

zeroShotClassifier = pipeline("zero-shot-classification")
print(zeroShotClassifier("The astronaut is playing basketball", candidate_labels=["sport", "business", "politics"]))