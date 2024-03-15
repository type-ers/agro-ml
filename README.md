<p align="center">
  <img src="web/static/images/banner.png" alt="Agro-ml Banner">
</p>

<h1 align="center">Agriculture Machine Learning (AGRO-ML)</h1>

<p>
<b>Team: Type-ers</b><br>
<ul style="list-style:none">
    <li><a href="https://github.com/ItsSitanshu">Sitanshu Shrestha</a></li>
    <li><a href="https://github.com/suvashish26">Suvashish Shrestha</a></li>
    <li><a href="https://github.com/abiral-manandhar">Abiral Manandhar</a></li>
    <li><a href="https://github.com/Krampussss">Biraj Sapkota</a></li>
</ul>
</p>

---

<h3>Problem Statement</h3>
<p>
  Agriculture in resource-constrained regions faces significant challenges due to the lack of affordable and accessible diagnostic tools. Our project, Agro-ml, aims to address these issues by providing Machine Learning (ML) and Artificial Intelligence (AI) services tailored for small-scale farmers in impoverished areas.
</p>

### Features:
1. **Leaf Disease Detection:**
   - Predicting disease in plants by passing leaf images through a Convolutional Neural Network (CNN).
   - Supported plants: corn, rice, tomato, apple, leaf, potato.

2. **Market Price Predictor:**
   - Predicting prices of crops and vegetables by analyzing market trends.

3. **Fertilizer Manager:**
   - Predicting suitable fertilizers to be used by analyzing crop combinations and other environmental conditions.


<h3>Datasets</h3>

- Tarkari Price Kalimati Dataset
- Fertilizer Prediction
- Various leaf disease datasets:
  - Corn or Maize Leaf Disease
  - Rice Leaf Disease
  - Tomato Leaf Disease Detection
  - Apple Leaf Diseases
  - Potato Leaf Disease
- Assessing the Impact of Fertilizer on Crop Yield

---


<h3>Contributing</h3>

We welcome contributions from the community! If you'd like to contribute to Agro-ml, please fork the repository and submit a pull request.

```
git clone https://github.com/ItsSitanshu/agro-ml.git

// train
cd models/ && python3 train.py

// flask-app
python3 src/main.py
```


This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

For any inquiries or feedback, please contact us:
- Email: [sitanshu15shrestha@gmail.com](mailto:sitanshu15shrestha@gmail.com)
- GitHub Issues: [Agro-ml Issues](https://github.com/ItsSitanshu/agro-ml/issues)

<h3>Data Sets</h3>
[models/data/fertilizer.csv](https://www.kaggle.com/datasets/gdabhishek/fertilizer-prediction)
[models/data/disease/*]
- [corn](https://www.kaggle.com/datasets/smaranjitghose/corn-or-maize-leaf-disease-dataset/data)
- [apple](https://www.kaggle.com/datasets/mhantor/apple-leaf-diseases/data)
- [tomato](https://www.kaggle.com/datasets/kaustubhb999/tomatoleaf)
- [rice](https://www.kaggle.com/datasets/dedeikhsandwisaputra/rice-leafs-disease-dataset?resource=download)
- [potato](https://www.kaggle.com/datasets/muhammadardiputra/potato-leaf-disease-dataset)
[models/data/market.csv](https://opendatanepal.com/dataset/activity/kalimati-tarkari-dataset)