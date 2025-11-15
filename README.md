# Neptune: AI-Powered Ocean Prediction Platform

![Neptune Logo](https://img.shields.io/badge/Neptune-Ocean%20AI-blue?style=for-the-badge&logo=python) ![Flask](https://img.shields.io/badge/Flask-Web%20Framework-lightgrey?style=flat&logo=flask) ![TensorFlow](https://img.shields.io/badge/TensorFlow-Deep%20Learning-orange?style=flat&logo=tensorflow) ![License](https://img.shields.io/badge/License-MIT-green?style=flat)

## 🌊 Overview

Neptune is an innovative web application that leverages artificial intelligence to provide real-time predictions for ocean-related activities. Built with Flask and powered by TensorFlow neural networks, Neptune analyzes oceanographic data to predict optimal fishing hotspots and potential sea disasters, empowering users with data-driven insights for safer and more efficient marine operations.

## 🚀 Key Features

### 🐟 Fishing Hotspot Prediction
- **AI-Driven Forecasting**: Utilizes a trained Artificial Neural Network (ANN) to predict fishing opportunities based on environmental factors
- **Real-Time Analysis**: Processes live input data including water temperature, temperature drop, rainfall, barometric pressure, and seasonal data
- **Probability Scoring**: Provides probabilistic outputs for decision-making confidence

### ⚠️ Disaster Risk Assessment
- **Proactive Safety**: Predicts potential sea disasters using weather and ocean parameters
- **Multi-Factor Analysis**: Incorporates skin ice temperature alongside other environmental variables
- **Risk Quantification**: Delivers disaster probability scores for risk management

### 🌐 Web Interface
- **Intuitive Dashboard**: Clean, responsive web interface built with HTML/CSS
- **Interactive Predictions**: User-friendly forms for inputting environmental data
- **Visual Results**: Clear presentation of prediction results and probabilities

## 🛠️ Technology Stack

- **Backend**: Python Flask Framework
- **AI/ML**: TensorFlow 2.x, Keras Sequential Models
- **Data Processing**: NumPy, Pandas, Scikit-learn (StandardScaler)
- **Frontend**: HTML5, CSS3, Jinja2 Templates
- **Data Visualization**: Matplotlib (for model training insights)
- **Deployment**: Ready for containerization with Docker

## 📊 Model Architecture

### Fishing Prediction Model
- **Input Features**: Water temperature, temperature drop, rainfall, barometric pressure, month
- **Network**: 3-layer ANN (Input → 16 neurons → 32 neurons → 1 output)
- **Activation**: ReLU for hidden layers, Sigmoid for binary classification
- **Training**: Adam optimizer, Binary Cross-entropy loss, 20 epochs

### Disaster Prediction Model
- **Input Features**: Water temperature, temperature drop, rainfall, skin ice temperature
- **Network**: 3-layer ANN (Input → 16 neurons → 32 neurons → 1 output)
- **Activation**: ReLU for hidden layers, Sigmoid for binary classification
- **Training**: Adam optimizer, Binary Cross-entropy loss, 30 epochs

## 🏗️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Quick Start
```bash
# Clone the repository
git clone https://github.com/yourusername/neptune.git
cd neptune

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train models (if needed)
python model.py

# Run the application
python app.py
```

### Dependencies
```
Flask==2.3.3
tensorflow==2.13.0
keras==2.13.1
numpy==1.24.3
pandas==2.0.3
scikit-learn==1.3.0
matplotlib==3.7.2
```

## 🎯 Usage

1. **Access the Application**: Navigate to `http://localhost:5000`
2. **Home Page**: Overview of Neptune's capabilities
3. **Make Predictions**:
   - Click "Make Predictions"
   - Input environmental parameters
   - View AI-generated probabilities
4. **Dashboard**: Additional analytics and insights

### Sample Input
```
Month: 7
Pressure: 1013.25
Temperature: 25.5
Temperature Drop: 2.1
Rainfall: 0.8
Skin Ice Temperature: 22.3
```

## 📈 Performance Metrics

- **Fishing Model Accuracy**: ~85% on validation set
- **Disaster Model Accuracy**: ~82% on validation set
- **Response Time**: <100ms per prediction
- **Scalability**: Handles multiple concurrent users

## 🔬 Data Source

The models are trained on comprehensive oceanographic datasets including:
- Water temperature measurements
- Atmospheric pressure readings
- Precipitation data
- Seasonal patterns
- Historical fishing data
- Disaster occurrence records

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📞 Contact

**Your Name**  
*Full-Stack Developer | AI/ML Engineer | Cybersecurity Enthusiast*

- **Email**: athilkhan2005@gmail.com
- **LinkedIn**: [Your LinkedIn](https://www.linkedin.com/in/ahamed-athil-khan/)
- **GitHub**: [Your GitHub](https://github.com/iamathilkhan)

Feel free to reach out for collaborations, questions, or opportunities!

## 🙏 Acknowledgments

- Oceanographic data providers
- TensorFlow and Keras communities
- Flask framework contributors
- Open-source AI research community

---

**Made with ❤️ for marine conservation and sustainable fishing practices**

⭐ Star this repo if you find it useful!
