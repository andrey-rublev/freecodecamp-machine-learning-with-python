# Machine Learning with Python

Five freeCodeCamp projects prepared using agentic AI for an AI class assignment. All original project tests pass. The official starter code and tests are credited below.

| Project | Source | Verified result |
| --- | --- | --- |
| Rock Paper Scissors | [RPS.py](RPS.py) | All four official tests pass; 99.49% to 100% win rate |
| Cat and Dog Image Classifier | [Notebook](fcc_cat_dog.ipynb) | 94% official test accuracy; required at least 63% |
| Book Recommendation Engine | [Notebook](fcc_book_recommendation_knn.ipynb) | Official recommendation test passes |
| Health Costs Calculator | [Notebook](fcc_predict_health_costs_with_regression.ipynb) | Held-out MAE $1,637.81; required below $3,500 |
| SMS Text Classifier | [Notebook](fcc_sms_text_classification.ipynb) | Official example tests pass; held-out accuracy 98.35% |

The notebooks retain actual training logs and test results. Figures are regenerated when the notebooks run. Datasets and trained model binaries are downloaded or created at runtime.

## Run

Open any notebook in [Google Colab](https://colab.research.google.com/github/andrey-rublev/freecodecamp-machine-learning-with-python/) and run all cells, or install the dependencies locally:

```bash
python -m pip install -r requirements.txt
python -m unittest test_module.py
python run_notebook.py fcc_cat_dog.ipynb
python run_notebook.py fcc_book_recommendation_knn.ipynb
python run_notebook.py fcc_predict_health_costs_with_regression.ipynb
python run_notebook.py fcc_sms_text_classification.ipynb
```

Use a clean Python environment. See [validation.json](validation.json) for the tested package versions and results. Notebook downloads use the official freeCodeCamp CDN repository. Random seeds are fixed, though hardware and library differences can affect training results.

## Methods

- Rock Paper Scissors scores several opponent predictors online and counters the best-performing predictor. Match state resets on the initial empty input.
- Image classification uses rescaled images, six training augmentations, a frozen pretrained MobileNetV2 convolutional base, and a trained dense classifier.
- Book recommendations filter users with fewer than 200 ratings and books with fewer than 100 ratings, then use sparse cosine KNN.
- Health-cost regression uses an 80/20 split, categorical encoding, smoking interactions, and a small neural regressor. Early stopping uses only training-validation rows.
- SMS classification uses training-only unigram and bigram TF-IDF features and a neural classifier. Early stopping uses a separate subset of training messages; the provided holdout is evaluated afterward.

## Official sources

- [Course](https://www.freecodecamp.org/learn/machine-learning-with-python/)
- [Rock Paper Scissors starter](https://github.com/freeCodeCamp/boilerplate-rock-paper-scissors)
- [Image classifier starter](https://github.com/freeCodeCamp/boilerplate-cat-and-dog-image-classifier)
- [Book recommender starter](https://github.com/freeCodeCamp/boilerplate-book-recommendation-engine)
- [Health-cost starter](https://github.com/freeCodeCamp/boilerplate-linear-regression-health-costs-calculator)
- [SMS classifier starter](https://github.com/freeCodeCamp/boilerplate-neural-network-sms-text-classifier)
- [Official datasets](https://github.com/freeCodeCamp/cdn/tree/main/build/project-data)

`RPS_game.py` and all supplied final challenge test cells are unchanged from the official starters.
