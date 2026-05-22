import streamlit as st
import streamlit.components.v1 as components
import random
import pandas as pd
import numpy as np
import pickle
import sqlite3
import plotly.graph_objects as go
import plotly.express as px
import os
import json
import time
import hashlib
import io
import base64
from datetime import datetime, date

# ──────────────────────────────────────────────────────────────
# PAGE CONFIG  (must be first Streamlit call)
# ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SkillForge AI",
    page_icon="🌱",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ──────────────────────────────────────────────────────────────
# YOUTUBE RESOURCES PER ROADMAP TASK
# ──────────────────────────────────────────────────────────────
YOUTUBE_RESOURCES = {
    # Data Scientist
    "Learn Python Basics & OOP":                    ("Python Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=rfscVS0vtbw"),
    "Master Pandas & NumPy":                        ("Pandas & NumPy Tutorial – Keith Galli", "https://www.youtube.com/watch?v=vmEHCJofslg"),
    "Learn SQL & Database Querying":                ("SQL Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=HXV3zeQKqGY"),
    "Study Data Visualization (Matplotlib / Seaborn / Plotly)": ("Matplotlib & Seaborn – Corey Schafer", "https://www.youtube.com/watch?v=UO98lJQ3QGI"),
    "Understand Statistics & Probability":          ("Statistics for Data Science – StatQuest", "https://www.youtube.com/watch?v=qBigTkBLU6g"),
    "Study Supervised Machine Learning":            ("Supervised ML – StatQuest", "https://www.youtube.com/watch?v=Gv9_4yMHFhI"),
    "Study Unsupervised Machine Learning":          ("Unsupervised Learning – StatQuest", "https://www.youtube.com/watch?v=IUn8k5zSI6g"),
    "Learn Model Evaluation & Tuning":              ("Model Evaluation – Krish Naik", "https://www.youtube.com/watch?v=85dtiMz9tSo"),
    "Build End-to-End ML Projects":                 ("End-to-End ML Project – Krish Naik", "https://www.youtube.com/watch?v=fiz1ORTBGpY"),
    "Deploy Models with Streamlit / FastAPI":       ("Deploy ML with Streamlit – Patrick Loeber", "https://www.youtube.com/watch?v=Klqn--Mu2pE"),
    # ML Engineer
    "Learn Python & Software Engineering Best Practices": ("Python for Engineers – Tech With Tim", "https://www.youtube.com/watch?v=mDKM-JtUhhc"),
    "Study Linear Algebra & Calculus for ML":       ("Linear Algebra for ML – 3Blue1Brown", "https://www.youtube.com/watch?v=fNk_zzaMoSs"),
    "Master Machine Learning Fundamentals":         ("ML Crash Course – Google", "https://www.youtube.com/watch?v=gmvvaobm7eQ"),
    "Learn Deep Learning (Neural Networks, CNNs, RNNs)": ("Deep Learning Specialization – Andrew Ng", "https://www.youtube.com/watch?v=CS4cs9xVecg"),
    "Study TensorFlow & PyTorch":                   ("PyTorch Full Course – Patrick Loeber", "https://www.youtube.com/watch?v=c36lUUr864M"),
    "Learn MLOps Fundamentals (MLflow, DVC)":       ("MLOps Tutorial – Krish Naik", "https://www.youtube.com/watch?v=9BgIDqAzfuA"),
    "Practice Model Deployment (Docker, FastAPI)":  ("FastAPI + Docker – Tech With Tim", "https://www.youtube.com/watch?v=0sOvCWFmrtA"),
    "Study Cloud ML Services (AWS SageMaker / GCP Vertex AI)": ("AWS SageMaker Tutorial – freeCodeCamp", "https://www.youtube.com/watch?v=uQc8Itd4UTs"),
    "Build Production ML Pipelines":                ("ML Pipelines – Made With ML", "https://www.youtube.com/watch?v=C5KAZbBPMeI"),
    "Contribute to Open-Source ML Projects":        ("How to Contribute to Open Source – freeCodeCamp", "https://www.youtube.com/watch?v=yzeVMecydCE"),
    # Frontend Developer
    "Learn HTML5 Semantic Markup":                  ("HTML Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=pQN-pnXPaVg"),
    "Master CSS3 & Flexbox / Grid":                 ("CSS Flexbox & Grid – Kevin Powell", "https://www.youtube.com/watch?v=u044iM9xsWU"),
    "Learn JavaScript (ES6+)":                      ("JavaScript Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=PkZNo7MFNFg"),
    "Study React & Component Architecture":         ("React Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=bMknfKXIFA8"),
    "Learn State Management (Redux / Zustand)":     ("Redux Toolkit Tutorial – Dave Gray", "https://www.youtube.com/watch?v=NqzdVN2tyvQ"),
    "Study TypeScript Basics":                      ("TypeScript Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=30LWjhZzg50"),
    "Learn Responsive & Accessible Design":         ("Responsive Design – Kevin Powell", "https://www.youtube.com/watch?v=srvUrASNj0s"),
    "Practice Testing (Jest, Cypress)":             ("Jest Testing – Traversy Media", "https://www.youtube.com/watch?v=7r4xVDI2vho"),
    "Build Responsive Websites & Deploy to Vercel": ("Deploy to Vercel – Fireship", "https://www.youtube.com/watch?v=ysEN5RaKOlA"),
    "Contribute to Open-Source Frontend Projects":  ("Open Source Contribution Guide – freeCodeCamp", "https://www.youtube.com/watch?v=yzeVMecydCE"),
    # Backend Developer
    "Learn Python or Node.js Fundamentals":         ("Node.js Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=Oe421EPjeBE"),
    "Study RESTful API Design":                     ("REST API Design – Traversy Media", "https://www.youtube.com/watch?v=SLwpqD8n3d0"),
    "Learn Database Design (SQL & NoSQL)":          ("Database Design – Caleb Curry", "https://www.youtube.com/watch?v=ztHopE5Wnpc"),
    "Study Authentication & Authorization (JWT, OAuth)": ("JWT Auth Tutorial – Web Dev Simplified", "https://www.youtube.com/watch?v=mbsmsi7l3r4"),
    "Learn Caching (Redis)":                        ("Redis Crash Course – Traversy Media", "https://www.youtube.com/watch?v=jgpVdJB2sKQ"),
    "Study Message Queues (Kafka / RabbitMQ)":      ("Kafka Tutorial – freeCodeCamp", "https://www.youtube.com/watch?v=gg5anlL6D4I"),
    "Learn Docker & Containerization":              ("Docker Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=fqMOX6JJhGo"),
    "Study CI/CD Pipelines":                        ("CI/CD Tutorial – TechWorld with Nana", "https://www.youtube.com/watch?v=R8_veQiYBjI"),
    "Build Scalable Backend Services":              ("Scalable Backend – Hussein Nasser", "https://www.youtube.com/watch?v=xpDnVSmNFX0"),
    "Deploy Backend Systems to Cloud":              ("AWS for Beginners – freeCodeCamp", "https://www.youtube.com/watch?v=3hLmDS179YE"),
    # UI UX Designer
    "Learn Design Principles & Visual Hierarchy":   ("Design Principles – The Futur", "https://www.youtube.com/watch?v=ZK86XQ1iFVs"),
    "Study Color Theory & Typography":              ("Color Theory – The Futur", "https://www.youtube.com/watch?v=_2LLXnUdUIc"),
    "Master Figma for UI Design":                   ("Figma Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=jwCmIBJ8Jtc"),
    "Practice Wireframing & Prototyping":           ("Wireframing in Figma – DesignCourse", "https://www.youtube.com/watch?v=d8PJ--MfPMw"),
    "Learn User Research & Usability Testing":      ("User Research Methods – Google UX Design", "https://www.youtube.com/watch?v=MTaFqRfcDNE"),
    "Study Interaction Design Patterns":            ("Interaction Design – Mizko", "https://www.youtube.com/watch?v=c9Wg6Cb_YlU"),
    "Build a Design System":                        ("Design Systems in Figma – Figma", "https://www.youtube.com/watch?v=Dtd40cHQQlk"),
    "Create End-to-End UX Case Studies":            ("UX Case Study – AJ&Smart", "https://www.youtube.com/watch?v=_ZDOQ_QoMoQ"),
    "Learn Motion Design Basics":                   ("Motion Design for UI – Google Design", "https://www.youtube.com/watch?v=cNMRe5pCWjY"),
    "Build a Strong Portfolio":                     ("UX Portfolio Tips – Google UX Design", "https://www.youtube.com/watch?v=_Dp-kENiywE"),
    # Cybersecurity
    "Learn Networking Fundamentals (TCP/IP, DNS, HTTP)": ("Networking Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=qiQR5rTSshw"),
    "Study Linux & Command Line":                   ("Linux Command Line – freeCodeCamp", "https://www.youtube.com/watch?v=rowRoy6od1o"),
    "Understand Security Fundamentals (CIA Triad)": ("Cybersecurity Basics – Professor Messer", "https://www.youtube.com/watch?v=ULGILG-ZhO0"),
    "Learn Ethical Hacking Basics":                 ("Ethical Hacking Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=3Kq1MIfTWCE"),
    "Practice Penetration Testing (Metasploit, Burp Suite)": ("Burp Suite Tutorial – TCM Security", "https://www.youtube.com/watch?v=G3hpAeoZ4ek"),
    "Study Cryptography Basics":                    ("Cryptography Crash Course – Computerphile", "https://www.youtube.com/watch?v=AQDCe585Lnc"),
    "Learn SIEM Tools (Splunk)":                    ("Splunk Tutorial – freeCodeCamp", "https://www.youtube.com/watch?v=xSG0HFXSCP0"),
    "Practice CTF Challenges":                      ("CTF Guide for Beginners – John Hammond", "https://www.youtube.com/watch?v=8ev9ZX9J45A"),
    "Study Incident Response & Forensics":          ("Digital Forensics – freeCodeCamp", "https://www.youtube.com/watch?v=YY7A5qH1lEk"),
    "Get CompTIA Security+ Certification":          ("Security+ Full Course – Professor Messer", "https://www.youtube.com/watch?v=9Hd8QJmZQUc"),
    # Software Engineer
    "Master Programming Fundamentals":              ("CS50 – Harvard", "https://www.youtube.com/watch?v=8mAITcNt710"),
    "Study Data Structures & Algorithms":           ("DSA Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=pkYVOmU3MgA"),
    "Learn Git & Version Control":                  ("Git & GitHub – freeCodeCamp", "https://www.youtube.com/watch?v=RGOj5yH7evk"),
    "Study System Design Principles":               ("System Design – Gaurav Sen", "https://www.youtube.com/watch?v=xpDnVSmNFX0"),
    "Learn Object-Oriented & Functional Design":    ("OOP in Python – Corey Schafer", "https://www.youtube.com/watch?v=ZDa-Z5JzLYM"),
    "Practice Code Reviews & Clean Code":           ("Clean Code – Traversy Media", "https://www.youtube.com/watch?v=7EmboKQH8lM"),
    "Study Databases (SQL & NoSQL)":                ("Databases Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=HXV3zeQKqGY"),
    "Learn API Design & Microservices":             ("Microservices – freeCodeCamp", "https://www.youtube.com/watch?v=lL_j7ilk7rc"),
    "Build and Deploy Full-Stack Projects":         ("Full Stack Project – Traversy Media", "https://www.youtube.com/watch?v=dtKciwk_si4"),
    "Contribute to Open-Source & Build Portfolio":  ("Open Source Guide – freeCodeCamp", "https://www.youtube.com/watch?v=yzeVMecydCE"),
    # Cloud Engineer
    "Learn Linux & Bash Scripting":                 ("Bash Scripting – freeCodeCamp", "https://www.youtube.com/watch?v=e7BufAVwDiM"),
    "Study Networking (VPC, Subnets, Load Balancers)": ("AWS Networking – freeCodeCamp", "https://www.youtube.com/watch?v=2d3OcMArfUk"),
    "Learn AWS / GCP / Azure Fundamentals":         ("AWS Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=3hLmDS179YE"),
    "Master Docker & Kubernetes":                   ("Kubernetes Full Course – TechWorld with Nana", "https://www.youtube.com/watch?v=X48VuDVv0do"),
    "Study Infrastructure as Code (Terraform)":     ("Terraform Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=SLB_c_ayRMo"),
    "Learn CI/CD for Cloud (GitHub Actions)":       ("GitHub Actions – TechWorld with Nana", "https://www.youtube.com/watch?v=R8_veQiYBjI"),
    "Study Cloud Security Best Practices":          ("Cloud Security – freeCodeCamp", "https://www.youtube.com/watch?v=M988_fsOSWo"),
    "Learn Monitoring & Observability (Prometheus, Grafana)": ("Prometheus & Grafana – TechWorld with Nana", "https://www.youtube.com/watch?v=h4Sl21AKiDg"),
    "Build Cloud-Native Applications":              ("Cloud Native Apps – CNCF", "https://www.youtube.com/watch?v=18jIzE41fJ4"),
    "Get AWS Solutions Architect Certification":    ("AWS SAA Prep – freeCodeCamp", "https://www.youtube.com/watch?v=Ia-UEYYR44s"),
    # DevOps Engineer
    "Learn Linux Administration":                   ("Linux Administration – freeCodeCamp", "https://www.youtube.com/watch?v=rowRoy6od1o"),
    "Master Git & Branching Strategies":            ("Git Branching – Atlassian", "https://www.youtube.com/watch?v=e2IbNHi4uCI"),
    "Study CI/CD Pipelines (Jenkins, GitHub Actions)": ("Jenkins Tutorial – TechWorld with Nana", "https://www.youtube.com/watch?v=7KCS70sCoK0"),
    "Learn Docker & Container Orchestration":       ("Docker Tutorial – TechWorld with Nana", "https://www.youtube.com/watch?v=3c-iBn73dDE"),
    "Master Kubernetes":                            ("Kubernetes – TechWorld with Nana", "https://www.youtube.com/watch?v=X48VuDVv0do"),
    "Study Infrastructure as Code (Terraform, Ansible)": ("Ansible Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=1id6ERvfozo"),
    "Learn Cloud Platforms (AWS / GCP / Azure)":    ("GCP Full Course – freeCodeCamp", "https://www.youtube.com/watch?v=jpno8FSqpc8"),
    "Study Monitoring (Prometheus, Grafana, ELK Stack)": ("ELK Stack Tutorial – freeCodeCamp", "https://www.youtube.com/watch?v=4X0WLg05ASw"),
    "Practice Incident Management & SRE Principles": ("SRE Fundamentals – Google", "https://www.youtube.com/watch?v=uTEL8Ff1Zvk"),
    "Build DevOps Portfolio Projects":              ("DevOps Projects – TechWorld with Nana", "https://www.youtube.com/watch?v=7KCS70sCoK0"),
}


# ──────────────────────────────────────────────────────────────
# SKILL CHALLENGE QUIZ DATA (50+ questions per career)
# ──────────────────────────────────────────────────────────────
QUIZ_DATA = {
    "Data Scientist": [
        {"q": "Which Python library is used for data manipulation?", "opts": ["NumPy", "Pandas", "Matplotlib", "Scikit-learn"], "ans": 1},
        {"q": "What does 'overfitting' mean in ML?", "opts": ["Model too simple", "Model memorizes training data", "Data has missing values", "Low accuracy"], "ans": 1},
        {"q": "Which algorithm is used for classification?", "opts": ["Linear Regression", "K-Means", "Random Forest", "PCA"], "ans": 2},
        {"q": "What is a confusion matrix used for?", "opts": ["Data cleaning", "Evaluating classification models", "Feature selection", "Normalization"], "ans": 1},
        {"q": "What does PCA stand for?", "opts": ["Partial Computation Analysis", "Principal Component Analysis", "Primary Cluster Algorithm", "Predictive Classification Approach"], "ans": 1},
        {"q": "Which metric is best for imbalanced datasets?", "opts": ["Accuracy", "F1-Score", "MSE", "R²"], "ans": 1},
        {"q": "What is the purpose of train/test split?", "opts": ["Speed up training", "Evaluate generalization", "Clean data", "Reduce features"], "ans": 1},
        {"q": "Which is an unsupervised learning algorithm?", "opts": ["Logistic Regression", "SVM", "K-Means", "Decision Tree"], "ans": 2},
        {"q": "What does SQL stand for?", "opts": ["Structured Query Language", "Simple Queue Logic", "Standard Query List", "Structured Queue Layer"], "ans": 0},
        {"q": "Which library is used for deep learning in Python?", "opts": ["Pandas", "Seaborn", "TensorFlow", "Requests"], "ans": 2},
        {"q": "What is a p-value?", "opts": ["Prediction value", "Probability of null hypothesis being true", "Percentage variance", "Performance value"], "ans": 1},
        {"q": "Which chart shows distribution of data?", "opts": ["Bar chart", "Histogram", "Pie chart", "Scatter plot"], "ans": 1},
        {"q": "What is cross-validation?", "opts": ["Testing on multiple machines", "Technique to assess model generalization", "Comparing two models", "Cleaning duplicate data"], "ans": 1},
        {"q": "What does 'feature engineering' mean?", "opts": ["Building hardware", "Creating or transforming input variables", "Removing features", "Normalizing output"], "ans": 1},
        {"q": "Which regression predicts continuous values?", "opts": ["Logistic Regression", "Linear Regression", "K-NN", "Naive Bayes"], "ans": 1},
        {"q": "What is the role of an activation function in neural networks?", "opts": ["Initialize weights", "Add non-linearity", "Reduce overfitting", "Normalize inputs"], "ans": 1},
        {"q": "What does ROC-AUC measure?", "opts": ["Regression accuracy", "Classification model performance", "Cluster quality", "Data distribution"], "ans": 1},
        {"q": "Which is a dimensionality reduction technique?", "opts": ["Random Forest", "LSTM", "PCA", "K-Means"], "ans": 2},
        {"q": "What is 'bias' in machine learning?", "opts": ["Overfitting", "Error from wrong assumptions", "Missing data", "High variance"], "ans": 1},
        {"q": "What is the purpose of regularization?", "opts": ["Speed training", "Prevent overfitting", "Increase accuracy", "Add more data"], "ans": 1},
        {"q": "Which is NOT a type of gradient descent?", "opts": ["Stochastic", "Mini-batch", "Full-batch", "Circular"], "ans": 3},
        {"q": "What does RMSE stand for?", "opts": ["Root Mean Square Error", "Relative Model Score Evaluation", "Random Mean Squared Estimate", "Root Model Standard Error"], "ans": 0},
        {"q": "Which is used to handle missing data?", "opts": ["One-hot encoding", "Imputation", "Normalization", "Tokenization"], "ans": 1},
        {"q": "What is a hyperparameter?", "opts": ["Output of a model", "Parameter set before training", "Feature of dataset", "Error measure"], "ans": 1},
        {"q": "Which plot shows correlation between two variables?", "opts": ["Histogram", "Box plot", "Scatter plot", "Bar chart"], "ans": 2},
    ],
    "ML Engineer": [
        {"q": "What is MLOps?", "opts": ["A Python library", "Practices for deploying ML systems reliably", "A type of neural network", "A dataset format"], "ans": 1},
        {"q": "What does Docker do?", "opts": ["Train ML models", "Containerize applications", "Store databases", "Build APIs"], "ans": 1},
        {"q": "What is a REST API?", "opts": ["A database type", "An interface using HTTP for communication", "A neural network layer", "A Python framework"], "ans": 1},
        {"q": "Which is used for model versioning?", "opts": ["Docker", "MLflow", "Pandas", "NumPy"], "ans": 1},
        {"q": "What is feature store?", "opts": ["A shop for datasets", "Centralized repository for ML features", "GPU storage", "Model registry"], "ans": 1},
        {"q": "What does 'inference' mean in ML?", "opts": ["Training a model", "Using a trained model to make predictions", "Evaluating accuracy", "Cleaning data"], "ans": 1},
        {"q": "Which framework is used for model serving?", "opts": ["Pandas", "TensorFlow Serving", "Matplotlib", "Seaborn"], "ans": 1},
        {"q": "What is model drift?", "opts": ["Model getting faster", "Degradation in model performance over time", "Overfitting during training", "Missing data issue"], "ans": 1},
        {"q": "What is Kubernetes used for?", "opts": ["Data cleaning", "Container orchestration", "Model training", "Feature engineering"], "ans": 1},
        {"q": "Which is a CI/CD tool?", "opts": ["TensorFlow", "Jenkins", "Pandas", "Matplotlib"], "ans": 1},
        {"q": "What does GPU stand for?", "opts": ["General Processing Unit", "Graphics Processing Unit", "Global Program Utility", "Gradient Processing Unit"], "ans": 1},
        {"q": "Which loss function is used for binary classification?", "opts": ["MSE", "Binary Cross-Entropy", "MAE", "Huber Loss"], "ans": 1},
        {"q": "What is transfer learning?", "opts": ["Moving data between servers", "Using pre-trained models for new tasks", "Copying model weights randomly", "Converting models to new frameworks"], "ans": 1},
        {"q": "What is A/B testing in ML?", "opts": ["Testing two algorithms on paper", "Comparing two model versions with real users", "Alpha-Beta pruning", "Asynchronous batch testing"], "ans": 1},
        {"q": "Which is a message queue system?", "opts": ["Redis", "Kafka", "PostgreSQL", "TensorFlow"], "ans": 1},
        {"q": "What does API stand for?", "opts": ["Application Programming Interface", "Advanced Python Integration", "Automated Process Input", "Application Protocol Index"], "ans": 0},
        {"q": "What is batch inference?", "opts": ["Real-time predictions", "Predictions on large datasets at once", "Training in batches", "Mini-batch gradient descent"], "ans": 1},
        {"q": "Which is a cloud ML platform?", "opts": ["GitHub", "AWS SageMaker", "VS Code", "Postman"], "ans": 1},
        {"q": "What is model quantization?", "opts": ["Adding more layers", "Reducing model size/precision for efficiency", "Training faster", "Adding regularization"], "ans": 1},
        {"q": "What is the purpose of a load balancer?", "opts": ["Train models faster", "Distribute traffic across servers", "Balance class weights", "Normalize features"], "ans": 1},
        {"q": "What is ONNX?", "opts": ["A programming language", "Open format for ML models", "A cloud provider", "A data format"], "ans": 1},
        {"q": "What is data pipeline?", "opts": ["A Python package", "Automated flow of data from source to destination", "Database schema", "Neural network layer"], "ans": 1},
        {"q": "Which is used for experiment tracking?", "opts": ["Docker", "MLflow", "Nginx", "Redis"], "ans": 1},
        {"q": "What is shadow deployment?", "opts": ["Running models at night", "Running new model alongside old without affecting users", "Dark mode for APIs", "Backup model storage"], "ans": 1},
        {"q": "What is the purpose of monitoring in MLOps?", "opts": ["Track server uptime only", "Detect model drift and data quality issues", "Train models continuously", "Store predictions"], "ans": 1},
    ],
    "Frontend Developer": [
        {"q": "What does HTML stand for?", "opts": ["Hyper Text Markup Language", "High Transfer Markup Language", "Hyper Transfer Module Language", "Hyper Text Module List"], "ans": 0},
        {"q": "Which CSS property controls spacing inside an element?", "opts": ["margin", "padding", "border", "spacing"], "ans": 1},
        {"q": "What is the virtual DOM in React?", "opts": ["A real browser DOM copy", "A lightweight in-memory representation of the DOM", "A CSS framework", "A server-side rendering tool"], "ans": 1},
        {"q": "What does CSS Flexbox mainly handle?", "opts": ["3D transforms", "One-dimensional layouts", "Animations", "Grid layouts"], "ans": 1},
        {"q": "What is a React Hook?", "opts": ["An event listener", "Function that lets you use state in functional components", "A CSS class", "A router component"], "ans": 1},
        {"q": "What does 'responsive design' mean?", "opts": ["Fast load time", "Design adapts to different screen sizes", "Server-side rendering", "Lazy loading"], "ans": 1},
        {"q": "What is TypeScript?", "opts": ["A database", "Typed superset of JavaScript", "A CSS preprocessor", "A testing framework"], "ans": 1},
        {"q": "Which hook manages state in React?", "opts": ["useEffect", "useState", "useContext", "useRef"], "ans": 1},
        {"q": "What is lazy loading?", "opts": ["Loading all assets upfront", "Loading resources only when needed", "Slow network simulation", "CSS animation technique"], "ans": 1},
        {"q": "What is the purpose of CSS Grid?", "opts": ["1D layout", "2D layout system", "Animation", "Typography"], "ans": 1},
        {"q": "What does 'semantic HTML' mean?", "opts": ["HTML with animations", "Using elements that describe their meaning", "Minified HTML", "HTML with inline styles"], "ans": 1},
        {"q": "Which is NOT a JavaScript framework?", "opts": ["React", "Vue", "Django", "Angular"], "ans": 2},
        {"q": "What is a CSS preprocessor?", "opts": ["Tool that extends CSS with variables and nesting", "A JavaScript bundler", "A browser plugin", "An animation library"], "ans": 0},
        {"q": "What does 'accessibility' mean in web development?", "opts": ["Fast performance", "Making apps usable for people with disabilities", "Mobile optimization", "SEO optimization"], "ans": 1},
        {"q": "What is webpack?", "opts": ["A CSS framework", "A module bundler for JavaScript", "A testing library", "A state manager"], "ans": 1},
        {"q": "What is the purpose of useEffect in React?", "opts": ["Manage state", "Handle side effects like API calls", "Style components", "Routing"], "ans": 1},
        {"q": "Which is a CSS-in-JS library?", "opts": ["Sass", "Styled-components", "Bootstrap", "Tailwind"], "ans": 1},
        {"q": "What is a Single Page Application (SPA)?", "opts": ["App with one route", "App that loads one HTML page and updates dynamically", "Simple HTML page", "Server-rendered app"], "ans": 1},
        {"q": "What does CORS stand for?", "opts": ["Cross-Origin Resource Sharing", "Client-Origin Request System", "Content-Origin Response Schema", "Cross-Object Request Syntax"], "ans": 0},
        {"q": "What is the purpose of Redux?", "opts": ["Routing", "Centralized state management", "UI animations", "API calls"], "ans": 1},
        {"q": "What is tree shaking?", "opts": ["CSS animation", "Removing unused code from bundles", "DOM manipulation", "Error handling"], "ans": 1},
        {"q": "Which tag makes text bold in HTML?", "opts": ["<i>", "<em>", "<strong>", "<b>"], "ans": 2},
        {"q": "What is a media query?", "opts": ["API call", "CSS technique to apply styles for specific screen sizes", "JavaScript event", "HTML attribute"], "ans": 1},
        {"q": "What is the box model in CSS?", "opts": ["3D layout system", "Model describing margin, border, padding, content", "Flexbox variant", "CSS animation model"], "ans": 1},
        {"q": "What is code splitting?", "opts": ["Breaking CSS into files", "Splitting JS into smaller chunks loaded on demand", "Dividing a team", "Separating HTML and CSS"], "ans": 1},
    ],
    "Backend Developer": [
        {"q": "What is a RESTful API?", "opts": ["A database", "API following REST architectural constraints", "A Python library", "A frontend framework"], "ans": 1},
        {"q": "Which is an ORM?", "opts": ["Redis", "SQLAlchemy", "Docker", "Nginx"], "ans": 1},
        {"q": "What does CRUD stand for?", "opts": ["Create, Read, Update, Delete", "Clone, Run, Upload, Deploy", "Connect, Retrieve, Update, Delete", "Create, Run, Undo, Deploy"], "ans": 0},
        {"q": "What is JWT?", "opts": ["JavaScript Web Tool", "JSON Web Token for authentication", "Java Web Technology", "JSON Wrapper Type"], "ans": 1},
        {"q": "Which is a NoSQL database?", "opts": ["PostgreSQL", "MySQL", "MongoDB", "SQLite"], "ans": 2},
        {"q": "What is caching?", "opts": ["Deleting old data", "Storing frequently accessed data for fast retrieval", "Compressing files", "Encrypting data"], "ans": 1},
        {"q": "What does HTTP status 404 mean?", "opts": ["Server error", "Resource not found", "Unauthorized", "Request timeout"], "ans": 1},
        {"q": "What is middleware?", "opts": ["A database layer", "Software between request and response processing", "Frontend component", "API endpoint"], "ans": 1},
        {"q": "What is connection pooling?", "opts": ["Grouping servers", "Reusing database connections for efficiency", "Load balancing", "Data backup"], "ans": 1},
        {"q": "What is SQL injection?", "opts": ["Adding SQL libraries", "Security vulnerability via malicious SQL input", "Database optimization", "Data migration"], "ans": 1},
        {"q": "Which HTTP method is used to update a resource?", "opts": ["GET", "POST", "PUT", "DELETE"], "ans": 2},
        {"q": "What is a microservice?", "opts": ["Small database", "Small independent service for a specific function", "Micro-frontend", "Tiny API call"], "ans": 1},
        {"q": "What is OAuth?", "opts": ["A database", "Authorization framework", "A REST alternative", "A Python library"], "ans": 1},
        {"q": "What does a reverse proxy do?", "opts": ["Forwards client requests to servers", "Blocks requests", "Caches client data", "Encrypts databases"], "ans": 0},
        {"q": "What is eventual consistency?", "opts": ["Immediate data sync", "Data becomes consistent over time in distributed systems", "Database transaction", "Cache invalidation"], "ans": 1},
        {"q": "What is a message queue?", "opts": ["Email system", "Asynchronous communication between services", "Database queue", "API rate limiter"], "ans": 1},
        {"q": "What is an index in a database?", "opts": ["Primary key", "Data structure to speed up queries", "Table column", "Foreign key"], "ans": 1},
        {"q": "What does ACID stand for in databases?", "opts": ["Atomicity, Consistency, Isolation, Durability", "Async, Computed, Indexed, Durable", "Atomic, Cached, Indexed, Distributed", "Atomicity, Consistency, Integration, Deployment"], "ans": 0},
        {"q": "What is rate limiting?", "opts": ["CPU throttling", "Controlling how many requests a client can make", "Database connection limit", "Memory management"], "ans": 1},
        {"q": "What is gRPC?", "opts": ["A database protocol", "High-performance RPC framework by Google", "A REST alternative library", "A Python framework"], "ans": 1},
        {"q": "What is horizontal scaling?", "opts": ["Adding more RAM", "Adding more servers to handle load", "Upgrading CPU", "Increasing disk space"], "ans": 1},
        {"q": "What is a deadlock?", "opts": ["Server crash", "Two processes waiting on each other indefinitely", "Memory leak", "Infinite loop"], "ans": 1},
        {"q": "What is an API gateway?", "opts": ["Database gateway", "Entry point that routes API requests to services", "Frontend server", "Authentication server"], "ans": 1},
        {"q": "What does TLS do?", "opts": ["Speeds up requests", "Encrypts data in transit", "Compresses responses", "Authenticates users"], "ans": 1},
        {"q": "What is database sharding?", "opts": ["Backing up data", "Splitting database across multiple servers", "Indexing strategy", "Query optimization"], "ans": 1},
    ],
    "UI UX Designer": [
        {"q": "What is a wireframe?", "opts": ["Final design", "Low-fidelity skeletal layout of a screen", "Color palette", "Prototype"], "ans": 1},
        {"q": "What does UX stand for?", "opts": ["User Examination", "User Experience", "UI Extension", "Unified Experience"], "ans": 1},
        {"q": "What is a design system?", "opts": ["An operating system", "Collection of reusable components and guidelines", "A prototyping tool", "A color theory"], "ans": 1},
        {"q": "What is the purpose of user research?", "opts": ["Build prototypes", "Understand user needs and behaviors", "Create color schemes", "Write code"], "ans": 1},
        {"q": "What is a persona in UX?", "opts": ["A user account", "A fictional representation of a target user", "A wireframe component", "A design pattern"], "ans": 1},
        {"q": "What is visual hierarchy?", "opts": ["Color theory", "Arrangement of elements to guide attention", "Grid system", "Typography rules"], "ans": 1},
        {"q": "What does WCAG stand for?", "opts": ["Web Content Accessibility Guidelines", "Web CSS Accessibility Group", "World Content and Graphics", "Web Component Architecture Guide"], "ans": 0},
        {"q": "What is a prototype?", "opts": ["Final product", "Interactive simulation of a design", "Wireframe", "Style guide"], "ans": 1},
        {"q": "What is 'affordance' in design?", "opts": ["Budget allocation", "Visual cue that suggests how to interact with an element", "Animation speed", "Color contrast"], "ans": 1},
        {"q": "What is the 'F-pattern' in UX?", "opts": ["Font selection pattern", "How users scan web pages in an F shape", "Form design pattern", "Feature flag pattern"], "ans": 1},
        {"q": "What is usability testing?", "opts": ["Testing code", "Observing users interacting with a product", "A/B testing", "Performance testing"], "ans": 1},
        {"q": "What is a style guide?", "opts": ["Writing grammar rules", "Document defining visual design standards", "Code standards", "API documentation"], "ans": 1},
        {"q": "What is contrast in design?", "opts": ["Animation speed", "Difference between elements to create visual interest", "Grid spacing", "Font weight"], "ans": 1},
        {"q": "What is 'white space' in design?", "opts": ["White background", "Empty space between elements that aids readability", "Blank page", "Unused canvas area"], "ans": 1},
        {"q": "What is information architecture?", "opts": ["Building design", "Organizing and structuring content for usability", "Database schema", "API design"], "ans": 1},
        {"q": "What is card sorting?", "opts": ["Sorting data tables", "UX method to understand how users categorize content", "Design card components", "Kanban method"], "ans": 1},
        {"q": "What is a high-fidelity prototype?", "opts": ["Sketch on paper", "Detailed interactive prototype close to final product", "Low-detail wireframe", "Style guide"], "ans": 1},
        {"q": "What does CTA stand for?", "opts": ["Content Transfer Action", "Call To Action", "Color Theme Attribute", "Component Target Area"], "ans": 1},
        {"q": "What is Gestalt principle?", "opts": ["German coding standard", "Psychological principles of how people perceive visuals", "Grid system", "Color model"], "ans": 1},
        {"q": "What is 'Hick's Law'?", "opts": ["More speed = more errors", "More choices = more decision time", "Bigger buttons = more clicks", "More contrast = better UX"], "ans": 1},
        {"q": "What is a user journey map?", "opts": ["App sitemap", "Visualization of user's experience across touchpoints", "Navigation menu", "User flow diagram"], "ans": 1},
        {"q": "What is 'Fitts' Law'?", "opts": ["Faster = better UX", "Time to reach target depends on size and distance", "More features = better product", "Simple > complex"], "ans": 1},
        {"q": "What is interaction design?", "opts": ["Backend logic", "Designing how users interact with digital products", "Print design", "Motion graphics"], "ans": 1},
        {"q": "What is empathy mapping?", "opts": ["Map of emotions in code", "Tool to visualize user thoughts, feelings and behaviors", "Color emotion guide", "User persona variant"], "ans": 1},
        {"q": "What is 'progressive disclosure'?", "opts": ["Loading screens", "Showing information gradually to avoid overwhelming users", "Lazy loading images", "Animation technique"], "ans": 1},
    ],
    "Cybersecurity Analyst": [
        {"q": "What is a firewall?", "opts": ["Antivirus software", "Network security system that monitors traffic", "Encryption tool", "VPN service"], "ans": 1},
        {"q": "What does CIA triad stand for?", "opts": ["Central Intelligence Agency", "Confidentiality, Integrity, Availability", "Cyber Incident Analysis", "Certified Information Auditor"], "ans": 1},
        {"q": "What is phishing?", "opts": ["Network scanning", "Fraudulent attempt to steal sensitive information", "Port scanning", "SQL injection"], "ans": 1},
        {"q": "What is a VPN?", "opts": ["Virtual Private Network", "Verified Proxy Node", "Virtual Protocol Network", "Verified Private Node"], "ans": 0},
        {"q": "What is penetration testing?", "opts": ["Testing app performance", "Authorized simulated cyberattack to find vulnerabilities", "Checking network speed", "Code review"], "ans": 1},
        {"q": "What is encryption?", "opts": ["Compressing data", "Converting data into unreadable format without a key", "Backing up data", "Deleting sensitive data"], "ans": 1},
        {"q": "What does DDoS stand for?", "opts": ["Distributed Denial of Service", "Dynamic Data over Systems", "Dual-layer Defense of Servers", "Distributed Data of Systems"], "ans": 0},
        {"q": "What is multi-factor authentication?", "opts": ["Multiple passwords", "Using 2+ verification methods to authenticate", "Admin access levels", "Biometric only"], "ans": 1},
        {"q": "What is a zero-day vulnerability?", "opts": ["Bug with no impact", "Unknown vulnerability with no patch available", "Old unpatched bug", "Low severity issue"], "ans": 1},
        {"q": "What is social engineering?", "opts": ["Building social networks", "Manipulating people to reveal sensitive information", "Social media hacking", "Group programming"], "ans": 1},
        {"q": "What is a SIEM?", "opts": ["Security Information and Event Management", "System for Internet Event Monitoring", "Secure Infrastructure Email Manager", "System Integrity and Encryption Module"], "ans": 0},
        {"q": "What is SQL injection?", "opts": ["Inserting SQL libraries", "Injecting malicious SQL to manipulate databases", "SQL performance tuning", "Database migration"], "ans": 1},
        {"q": "What is the purpose of hashing?", "opts": ["Encrypting data for transmission", "Creating fixed-size output from data (one-way)", "Compressing files", "Generating encryption keys"], "ans": 1},
        {"q": "What is a botnet?", "opts": ["Network of bots for automation", "Group of compromised computers controlled remotely", "Robot testing network", "Bot detection system"], "ans": 1},
        {"q": "What does XSS stand for?", "opts": ["Extended Security System", "Cross-Site Scripting", "XML Security Schema", "Cross-Server Syntax"], "ans": 1},
        {"q": "What is a honeypot?", "opts": ["Sweet data storage", "Decoy system to attract and study attackers", "Firewall type", "Malware tool"], "ans": 1},
        {"q": "What is privilege escalation?", "opts": ["User promotion", "Gaining higher access rights than intended", "Admin login", "Role assignment"], "ans": 1},
        {"q": "What is a CVE?", "opts": ["Cyber Vulnerability Entry", "Common Vulnerabilities and Exposures database entry", "Certificate Verification Entry", "Core Virus Encyclopedia"], "ans": 1},
        {"q": "What is network segmentation?", "opts": ["Splitting internet bandwidth", "Dividing network into isolated zones for security", "DNS splitting", "Load balancing"], "ans": 1},
        {"q": "What is the purpose of a DMZ in networking?", "opts": ["Demarcation zone for ISP", "Buffer zone between internet and internal network", "DNS management zone", "Data migration zone"], "ans": 1},
        {"q": "What is HTTPS?", "opts": ["HTTP with speed boost", "HTTP secured with TLS/SSL encryption", "Hypertext Transfer Protocol Secure System", "HTTP Server"], "ans": 1},
        {"q": "What is a Man-in-the-Middle attack?", "opts": ["Server impersonation", "Attacker secretly intercepts communication between two parties", "Brute force attack", "Phishing variant"], "ans": 1},
        {"q": "What is threat modeling?", "opts": ["Predicting market threats", "Identifying and prioritizing potential security threats", "Building threat databases", "Malware analysis"], "ans": 1},
        {"q": "What is an intrusion detection system?", "opts": ["Antivirus software", "System that monitors network for suspicious activity", "Firewall type", "VPN service"], "ans": 1},
        {"q": "What is the principle of least privilege?", "opts": ["Give all users admin access", "Grant only minimum access rights needed", "Restrict internet access", "Encrypt all communications"], "ans": 1},
    ],
    "Software Engineer": [
        {"q": "What is Big O notation?", "opts": ["Code formatting style", "Describes algorithm time/space complexity", "A Python library", "Object notation format"], "ans": 1},
        {"q": "What is a stack data structure?", "opts": ["FIFO structure", "LIFO structure (Last In First Out)", "Sorted array", "Hash map"], "ans": 1},
        {"q": "What is Git used for?", "opts": ["Database management", "Version control and code collaboration", "Project management", "Code compilation"], "ans": 1},
        {"q": "What is object-oriented programming?", "opts": ["Procedural coding style", "Paradigm using objects with attributes and methods", "Functional programming", "Event-driven programming"], "ans": 1},
        {"q": "What is a binary search?", "opts": ["Searching by value", "Efficient search on sorted data by halving search space", "Linear search variant", "Searching binary files"], "ans": 1},
        {"q": "What is a design pattern?", "opts": ["UI layout", "Reusable solution to a common software problem", "Coding style guide", "Database schema"], "ans": 1},
        {"q": "What is the Singleton pattern?", "opts": ["Single responsibility", "Ensures only one instance of a class exists", "One-to-one database relation", "Single thread execution"], "ans": 1},
        {"q": "What does SOLID stand for?", "opts": ["5 principles of good OOP design", "Software Object Language Integration Design", "Scalable Object Logic Integration Design", "System Object Language Interface Design"], "ans": 0},
        {"q": "What is a linked list?", "opts": ["Array with links", "Linear structure of nodes pointing to next node", "Sorted list", "Doubly indexed array"], "ans": 1},
        {"q": "What is a hash table?", "opts": ["Encrypted table", "Key-value data structure with O(1) average lookup", "Sorted dictionary", "Database table type"], "ans": 1},
        {"q": "What is recursion?", "opts": ["Looping with for loops", "Function that calls itself", "Repeated array operations", "Nested classes"], "ans": 1},
        {"q": "What is the difference between a process and a thread?", "opts": ["No difference", "Process is independent; threads share process memory", "Thread is heavier than process", "Processes run faster"], "ans": 1},
        {"q": "What is a deadlock?", "opts": ["Server timeout", "Two processes waiting on each other indefinitely", "Memory leak", "Stack overflow"], "ans": 1},
        {"q": "What is test-driven development (TDD)?", "opts": ["Writing tests after code", "Writing tests before implementing code", "Testing in production", "Manual testing approach"], "ans": 1},
        {"q": "What is continuous integration?", "opts": ["Daily meetings", "Automatically building and testing code on every commit", "Merging branches weekly", "Manual deployment"], "ans": 1},
        {"q": "What is a queue data structure?", "opts": ["LIFO structure", "FIFO structure (First In First Out)", "Sorted stack", "Priority array"], "ans": 1},
        {"q": "What is an API?", "opts": ["Application Programming Interface", "Automated Process Integration", "Advanced Python Interface", "Application Process Index"], "ans": 0},
        {"q": "What is refactoring?", "opts": ["Rewriting from scratch", "Improving code structure without changing behavior", "Adding new features", "Fixing bugs"], "ans": 1},
        {"q": "What is polymorphism in OOP?", "opts": ["Multiple inheritance", "Objects of different types responding to same interface", "Multiple constructors", "Type casting"], "ans": 1},
        {"q": "What is the Observer pattern?", "opts": ["Code monitoring", "One-to-many dependency where observers get notified of changes", "Logging pattern", "Testing pattern"], "ans": 1},
        {"q": "What is a binary tree?", "opts": ["Tree with 2 levels", "Tree where each node has at most 2 children", "Balanced search tree", "B-tree variant"], "ans": 1},
        {"q": "What is memoization?", "opts": ["Writing documentation", "Caching function results to avoid recomputation", "Memory allocation", "Code comments"], "ans": 1},
        {"q": "What is dynamic programming?", "opts": ["Programming with dynamic typing", "Solving problems by breaking into overlapping subproblems", "Runtime code generation", "UI programming"], "ans": 1},
        {"q": "What is the Factory design pattern?", "opts": ["Building physical factories", "Creates objects without specifying exact class", "Singleton variant", "Observer pattern type"], "ans": 1},
        {"q": "What is coupling in software design?", "opts": ["Database relationships", "Degree of interdependence between modules", "API connections", "Test coverage"], "ans": 1},
    ],
    "Cloud Engineer": [
        {"q": "What does IaaS stand for?", "opts": ["Internet as a Service", "Infrastructure as a Service", "Integration as a Service", "Interface as a Service"], "ans": 1},
        {"q": "What is an S3 bucket?", "opts": ["A database", "Object storage service in AWS", "A server type", "A network protocol"], "ans": 1},
        {"q": "What is auto-scaling?", "opts": ["Automatic code scaling", "Automatically adjusting compute resources based on demand", "Auto database backup", "Automatic deployment"], "ans": 1},
        {"q": "What is a VPC?", "opts": ["Virtual Private Cloud", "Virtual Protocol Connection", "Verified Private Container", "Virtual Proxy Connection"], "ans": 0},
        {"q": "What is Terraform?", "opts": ["A cloud provider", "Infrastructure as Code tool", "Container orchestration", "Monitoring tool"], "ans": 1},
        {"q": "What does CDN stand for?", "opts": ["Central Data Node", "Content Delivery Network", "Cloud Data Network", "Central Deployment Node"], "ans": 1},
        {"q": "What is a container?", "opts": ["Virtual machine", "Lightweight isolated environment for running applications", "Cloud storage unit", "Database cluster"], "ans": 1},
        {"q": "What is Kubernetes?", "opts": ["A cloud provider", "Container orchestration platform", "Infrastructure as code tool", "Monitoring solution"], "ans": 1},
        {"q": "What is serverless computing?", "opts": ["Computing without electricity", "Running code without managing servers", "Offline computing", "Edge computing"], "ans": 1},
        {"q": "What is a load balancer?", "opts": ["CPU manager", "Distributes network traffic across servers", "Storage optimizer", "Database replicator"], "ans": 1},
        {"q": "What is object storage?", "opts": ["OOP storage pattern", "Flat storage for unstructured data (files, images, backups)", "Database type", "Container storage"], "ans": 1},
        {"q": "What is a cloud region?", "opts": ["Geographic area with cloud data centers", "Cloud pricing zone", "Network subnet", "Availability zone"], "ans": 0},
        {"q": "What is IAM in AWS?", "opts": ["Image and Media service", "Identity and Access Management", "Infrastructure and Management", "Internet Access Module"], "ans": 1},
        {"q": "What is CloudFormation?", "opts": ["Weather API service", "AWS Infrastructure as Code service", "Cloud monitoring tool", "Container service"], "ans": 1},
        {"q": "What is a subnet?", "opts": ["Sub-database", "Subdivision of an IP network", "Subcontainer", "Sub-region"], "ans": 1},
        {"q": "What is high availability?", "opts": ["Fast CPU speed", "System designed to minimize downtime", "High bandwidth", "Premium cloud tier"], "ans": 1},
        {"q": "What is GitOps?", "opts": ["Git operations team", "Using Git as source of truth for infrastructure", "GitHub operations", "Git CI/CD pipeline"], "ans": 1},
        {"q": "What is a service mesh?", "opts": ["Network firewall", "Infrastructure layer for service-to-service communication", "Container network", "API gateway type"], "ans": 1},
        {"q": "What is disaster recovery?", "opts": ["Deleting bad data", "Strategy to restore systems after catastrophic failure", "Backup storage", "Monitoring alerting"], "ans": 1},
        {"q": "What is multi-cloud?", "opts": ["Multiple accounts on one provider", "Using services from multiple cloud providers", "Cloud redundancy", "Multi-region deployment"], "ans": 1},
        {"q": "What does SLA stand for?", "opts": ["Server Level Agreement", "Service Level Agreement", "System Load Alert", "Scalable Layer Architecture"], "ans": 1},
        {"q": "What is edge computing?", "opts": ["Extreme computing", "Processing data closer to where it is generated", "GPU computing", "Distributed databases"], "ans": 1},
        {"q": "What is Helm in Kubernetes?", "opts": ["Navigation tool", "Package manager for Kubernetes applications", "Container runtime", "Network plugin"], "ans": 1},
        {"q": "What is a security group in AWS?", "opts": ["IAM user group", "Virtual firewall controlling instance traffic", "Team of security engineers", "Encryption key group"], "ans": 1},
        {"q": "What is blue-green deployment?", "opts": ["Color-coded servers", "Running two identical environments to switch traffic with zero downtime", "Dev/prod environments", "Canary deployment variant"], "ans": 1},
    ],
    "DevOps Engineer": [
        {"q": "What is CI/CD?", "opts": ["Code Inspection/Code Deployment", "Continuous Integration/Continuous Delivery", "Cloud Infrastructure/Cloud Deployment", "Code Integration/Code Distribution"], "ans": 1},
        {"q": "What is Infrastructure as Code?", "opts": ["Writing infrastructure documentation", "Managing infrastructure using code/config files", "Code running on infrastructure", "Cloud billing code"], "ans": 1},
        {"q": "What is Ansible?", "opts": ["A cloud provider", "Configuration management and automation tool", "Container orchestration", "CI/CD pipeline tool"], "ans": 1},
        {"q": "What is a Dockerfile?", "opts": ["Documentation file", "Script of instructions to build a Docker image", "Docker configuration", "Container log file"], "ans": 1},
        {"q": "What is a Jenkins pipeline?", "opts": ["Water pipe monitoring", "Automated workflow for CI/CD in Jenkins", "Network pipeline", "Data pipeline"], "ans": 1},
        {"q": "What does SRE stand for?", "opts": ["Software Reliability Engineering", "Site Reliability Engineering", "System Resource Engineering", "Server Reliability Environment"], "ans": 1},
        {"q": "What is a rolling deployment?", "opts": ["Deploying on Saturdays", "Gradually replacing old instances with new ones", "Rolling back a deployment", "Full restart deployment"], "ans": 1},
        {"q": "What is Prometheus?", "opts": ["A cloud provider", "Open-source monitoring and alerting system", "Container runtime", "CI/CD tool"], "ans": 1},
        {"q": "What is a canary deployment?", "opts": ["Testing in bird-themed environments", "Releasing to small percentage of users before full rollout", "Blue-green deployment variant", "Hotfix deployment"], "ans": 1},
        {"q": "What is the purpose of a Makefile?", "opts": ["Documentation tool", "Automates build and task commands", "Docker file variant", "Dependency manager"], "ans": 1},
        {"q": "What is log aggregation?", "opts": ["Counting log files", "Collecting logs from multiple sources into central location", "Log compression", "Log deletion"], "ans": 1},
        {"q": "What is an SLO?", "opts": ["Service Level Objective", "Server Load Output", "System Log Overview", "Service Launch Order"], "ans": 0},
        {"q": "What is GitLab CI?", "opts": ["A Git hosting alternative", "CI/CD platform integrated with GitLab", "Code review tool", "Container registry"], "ans": 1},
        {"q": "What is Grafana used for?", "opts": ["Code deployment", "Visualizing metrics and monitoring dashboards", "Container management", "Log storage"], "ans": 1},
        {"q": "What is chaos engineering?", "opts": ["Disorganized coding", "Intentionally injecting failures to test system resilience", "Agile methodology", "Random testing"], "ans": 1},
        {"q": "What is a container registry?", "opts": ["Container inventory list", "Storage for Docker images", "Container monitoring", "Container orchestration"], "ans": 1},
        {"q": "What does MTTR stand for?", "opts": ["Mean Time To Resolve", "Mean Time To Recover", "Maximum Time To Respond", "Mean Test Time Rate"], "ans": 1},
        {"q": "What is infrastructure drift?", "opts": ["Cloud migration", "When actual infrastructure differs from its code definition", "Configuration backup", "Deployment failure"], "ans": 1},
        {"q": "What is a health check in DevOps?", "opts": ["Team wellness", "Automated check to verify service is running correctly", "Performance benchmark", "Security audit"], "ans": 1},
        {"q": "What is shift-left testing?", "opts": ["Testing from left side of screen", "Moving testing earlier in development lifecycle", "Shifting test environments", "Left-side code review"], "ans": 1},
        {"q": "What is a feature flag?", "opts": ["Version control flag", "Toggle to enable/disable features without redeploying", "Git branch marker", "CI/CD step flag"], "ans": 1},
        {"q": "What is artifact management?", "opts": ["Museum management", "Storing and versioning build outputs (jars, images, etc.)", "Code documentation", "Project management"], "ans": 1},
        {"q": "What is observability?", "opts": ["Monitoring uptime only", "Ability to understand system state from its outputs (logs, metrics, traces)", "Security monitoring", "Performance profiling"], "ans": 1},
        {"q": "What is a golden image?", "opts": ["Premium cloud tier", "Pre-configured, tested VM image used as base for deployments", "Docker image with GPU", "Production database snapshot"], "ans": 1},
        {"q": "What is runbook automation?", "opts": ["Automated code running", "Automating manual operational procedures", "CI/CD automation", "Test automation"], "ans": 1},
    ],
}

# Hardcoded task durations (hours) for Smart Scheduler
TASK_DURATIONS = {
    "Learn Python Basics & OOP": 8,
    "Master Pandas & NumPy": 6,
    "Learn SQL & Database Querying": 5,
    "Study Data Visualization (Matplotlib / Seaborn / Plotly)": 5,
    "Understand Statistics & Probability": 7,
    "Study Supervised Machine Learning": 8,
    "Study Unsupervised Machine Learning": 6,
    "Learn Model Evaluation & Tuning": 5,
    "Build End-to-End ML Projects": 10,
    "Deploy Models with Streamlit / FastAPI": 6,
    "Learn Python & Software Engineering Best Practices": 6,
    "Study Linear Algebra & Calculus for ML": 8,
    "Master Machine Learning Fundamentals": 8,
    "Learn Deep Learning (Neural Networks, CNNs, RNNs)": 10,
    "Study TensorFlow & PyTorch": 8,
    "Learn MLOps Fundamentals (MLflow, DVC)": 6,
    "Practice Model Deployment (Docker, FastAPI)": 6,
    "Study Cloud ML Services (AWS SageMaker / GCP Vertex AI)": 7,
    "Build Production ML Pipelines": 8,
    "Contribute to Open-Source ML Projects": 5,
    "Learn HTML5 Semantic Markup": 3,
    "Master CSS3 & Flexbox / Grid": 5,
    "Learn JavaScript (ES6+)": 8,
    "Study React & Component Architecture": 8,
    "Learn State Management (Redux / Zustand)": 5,
    "Study TypeScript Basics": 4,
    "Learn Responsive & Accessible Design": 4,
    "Practice Testing (Jest, Cypress)": 4,
    "Build Responsive Websites & Deploy to Vercel": 6,
    "Contribute to Open-Source Frontend Projects": 5,
    "Learn Python or Node.js Fundamentals": 7,
    "Study RESTful API Design": 5,
    "Learn Database Design (SQL & NoSQL)": 6,
    "Study Authentication & Authorization (JWT, OAuth)": 5,
    "Learn Caching (Redis)": 4,
    "Study Message Queues (Kafka / RabbitMQ)": 5,
    "Learn Docker & Containerization": 5,
    "Study CI/CD Pipelines": 5,
    "Build Scalable Backend Services": 8,
    "Deploy Backend Systems to Cloud": 6,
    "Learn Design Principles & Visual Hierarchy": 4,
    "Study Color Theory & Typography": 3,
    "Master Figma for UI Design": 6,
    "Practice Wireframing & Prototyping": 5,
    "Learn User Research & Usability Testing": 5,
    "Study Interaction Design Patterns": 4,
    "Build a Design System": 6,
    "Create End-to-End UX Case Studies": 8,
    "Learn Motion Design Basics": 4,
    "Build a Strong Portfolio": 7,
    "Learn Networking Fundamentals (TCP/IP, DNS, HTTP)": 6,
    "Study Linux & Command Line": 5,
    "Understand Security Fundamentals (CIA Triad)": 4,
    "Learn Ethical Hacking Basics": 6,
    "Practice Penetration Testing (Metasploit, Burp Suite)": 7,
    "Study Cryptography Basics": 4,
    "Learn SIEM Tools (Splunk)": 5,
    "Practice CTF Challenges": 6,
    "Study Incident Response & Forensics": 5,
    "Get CompTIA Security+ Certification": 8,
    "Master Programming Fundamentals": 7,
    "Study Data Structures & Algorithms": 10,
    "Learn Git & Version Control": 3,
    "Study System Design Principles": 7,
    "Learn Object-Oriented & Functional Design": 5,
    "Practice Code Reviews & Clean Code": 4,
    "Study Databases (SQL & NoSQL)": 6,
    "Learn API Design & Microservices": 6,
    "Build and Deploy Full-Stack Projects": 10,
    "Contribute to Open-Source & Build Portfolio": 5,
    "Learn Linux & Bash Scripting": 5,
    "Study Networking (VPC, Subnets, Load Balancers)": 5,
    "Learn AWS / GCP / Azure Fundamentals": 7,
    "Master Docker & Kubernetes": 8,
    "Study Infrastructure as Code (Terraform)": 6,
    "Learn CI/CD for Cloud (GitHub Actions)": 5,
    "Study Cloud Security Best Practices": 5,
    "Learn Monitoring & Observability (Prometheus, Grafana)": 5,
    "Build Cloud-Native Applications": 7,
    "Get AWS Solutions Architect Certification": 10,
    "Learn Linux Administration": 5,
    "Master Git & Branching Strategies": 3,
    "Study CI/CD Pipelines (Jenkins, GitHub Actions)": 6,
    "Learn Docker & Container Orchestration": 6,
    "Master Kubernetes": 8,
    "Study Infrastructure as Code (Terraform, Ansible)": 7,
    "Learn Cloud Platforms (AWS / GCP / Azure)": 7,
    "Study Monitoring (Prometheus, Grafana, ELK Stack)": 6,
    "Practice Incident Management & SRE Principles": 5,
    "Build DevOps Portfolio Projects": 8,
}

# ──────────────────────────────────────────────────────────────
# ROADMAPS
# ──────────────────────────────────────────────────────────────
ROADMAPS = {
    "Data Scientist": [
        "Learn Python Basics & OOP",
        "Master Pandas & NumPy",
        "Learn SQL & Database Querying",
        "Study Data Visualization (Matplotlib / Seaborn / Plotly)",
        "Understand Statistics & Probability",
        "Study Supervised Machine Learning",
        "Study Unsupervised Machine Learning",
        "Learn Model Evaluation & Tuning",
        "Build End-to-End ML Projects",
        "Deploy Models with Streamlit / FastAPI",
    ],
    "ML Engineer": [
        "Learn Python & Software Engineering Best Practices",
        "Study Linear Algebra & Calculus for ML",
        "Master Machine Learning Fundamentals",
        "Learn Deep Learning (Neural Networks, CNNs, RNNs)",
        "Study TensorFlow & PyTorch",
        "Learn MLOps Fundamentals (MLflow, DVC)",
        "Practice Model Deployment (Docker, FastAPI)",
        "Study Cloud ML Services (AWS SageMaker / GCP Vertex AI)",
        "Build Production ML Pipelines",
        "Contribute to Open-Source ML Projects",
    ],
    "Frontend Developer": [
        "Learn HTML5 Semantic Markup",
        "Master CSS3 & Flexbox / Grid",
        "Learn JavaScript (ES6+)",
        "Study React & Component Architecture",
        "Learn State Management (Redux / Zustand)",
        "Study TypeScript Basics",
        "Learn Responsive & Accessible Design",
        "Practice Testing (Jest, Cypress)",
        "Build Responsive Websites & Deploy to Vercel",
        "Contribute to Open-Source Frontend Projects",
    ],
    "Backend Developer": [
        "Learn Python or Node.js Fundamentals",
        "Study RESTful API Design",
        "Learn Database Design (SQL & NoSQL)",
        "Study Authentication & Authorization (JWT, OAuth)",
        "Learn Caching (Redis)",
        "Study Message Queues (Kafka / RabbitMQ)",
        "Learn Docker & Containerization",
        "Study CI/CD Pipelines",
        "Build Scalable Backend Services",
        "Deploy Backend Systems to Cloud",
    ],
    "UI UX Designer": [
        "Learn Design Principles & Visual Hierarchy",
        "Study Color Theory & Typography",
        "Master Figma for UI Design",
        "Practice Wireframing & Prototyping",
        "Learn User Research & Usability Testing",
        "Study Interaction Design Patterns",
        "Build a Design System",
        "Create End-to-End UX Case Studies",
        "Learn Motion Design Basics",
        "Build a Strong Portfolio",
    ],
    "Cybersecurity Analyst": [
        "Learn Networking Fundamentals (TCP/IP, DNS, HTTP)",
        "Study Linux & Command Line",
        "Understand Security Fundamentals (CIA Triad)",
        "Learn Ethical Hacking Basics",
        "Practice Penetration Testing (Metasploit, Burp Suite)",
        "Study Cryptography Basics",
        "Learn SIEM Tools (Splunk)",
        "Practice CTF Challenges",
        "Study Incident Response & Forensics",
        "Get CompTIA Security+ Certification",
    ],
    "Software Engineer": [
        "Master Programming Fundamentals",
        "Study Data Structures & Algorithms",
        "Learn Git & Version Control",
        "Study System Design Principles",
        "Learn Object-Oriented & Functional Design",
        "Practice Code Reviews & Clean Code",
        "Study Databases (SQL & NoSQL)",
        "Learn API Design & Microservices",
        "Build and Deploy Full-Stack Projects",
        "Contribute to Open-Source & Build Portfolio",
    ],
    "Cloud Engineer": [
        "Learn Linux & Bash Scripting",
        "Study Networking (VPC, Subnets, Load Balancers)",
        "Learn AWS / GCP / Azure Fundamentals",
        "Master Docker & Kubernetes",
        "Study Infrastructure as Code (Terraform)",
        "Learn CI/CD for Cloud (GitHub Actions)",
        "Study Cloud Security Best Practices",
        "Learn Monitoring & Observability (Prometheus, Grafana)",
        "Build Cloud-Native Applications",
        "Get AWS Solutions Architect Certification",
    ],
    "DevOps Engineer": [
        "Learn Linux Administration",
        "Master Git & Branching Strategies",
        "Study CI/CD Pipelines (Jenkins, GitHub Actions)",
        "Learn Docker & Container Orchestration",
        "Master Kubernetes",
        "Study Infrastructure as Code (Terraform, Ansible)",
        "Learn Cloud Platforms (AWS / GCP / Azure)",
        "Study Monitoring (Prometheus, Grafana, ELK Stack)",
        "Practice Incident Management & SRE Principles",
        "Build DevOps Portfolio Projects",
    ],
}

SKILL_ICONS = {
    "Python": "🐍",
    "SQL": "🗄️",
    "Machine Learning": "🤖",
    "Web Development": "🌐",
    "UI/UX": "🎨",
    "Communication": "💬",
    "Problem Solving": "🧩",
    "Cloud": "☁️",
    "Data Analysis": "📊",
    "Cybersecurity": "🔐",
}

CAREER_ICONS = {
    "Data Scientist": "🔬",
    "ML Engineer": "⚙️",
    "Frontend Developer": "🖥️",
    "Backend Developer": "🛠️",
    "UI UX Designer": "🎨",
    "Cybersecurity Analyst": "🛡️",
    "Software Engineer": "💻",
    "Cloud Engineer": "☁️",
    "DevOps Engineer": "🚀",
}

BADGES = {
    "First Prediction":  {"icon": "🎯", "xp": 0,   "desc": "Made your first career prediction"},
    "100 XP Club":       {"icon": "⭐", "xp": 100,  "desc": "Earned 100 XP"},
    "Skill Starter":     {"icon": "🌱", "xp": 0,   "desc": "Completed first roadmap task"},
    "Halfway There":     {"icon": "🏃", "xp": 0,   "desc": "50%+ roadmap completion"},
    "Roadmap Complete":  {"icon": "🏆", "xp": 0,   "desc": "Completed the full roadmap"},
    "XP Master":         {"icon": "💎", "xp": 200,  "desc": "Earned 200 XP"},
}

# ──────────────────────────────────────────────────────────────
# DATABASE
# ──────────────────────────────────────────────────────────────
DB_PATH = "skillforge.db"

@st.cache_resource
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=30)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    # Create tables using individual execute (avoids executescript lock issues)
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    # Migrate: add password column if missing
    existing_cols = [row[1] for row in c.execute("PRAGMA table_info(users)").fetchall()]
    if "password" not in existing_cols:
        c.execute("ALTER TABLE users ADD COLUMN password TEXT NOT NULL DEFAULT ''")
    c.execute("""CREATE TABLE IF NOT EXISTS user_stats (
        username TEXT PRIMARY KEY,
        career TEXT,
        xp INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        streak INTEGER DEFAULT 0,
        last_login TEXT,
        progress INTEGER DEFAULT 0,
        completed_tasks TEXT DEFAULT '[]',
        achievements TEXT DEFAULT '[]',
        skill_python INTEGER DEFAULT 5,
        skill_sql INTEGER DEFAULT 5,
        skill_ml INTEGER DEFAULT 5,
        skill_web INTEGER DEFAULT 5,
        skill_uiux INTEGER DEFAULT 5,
        skill_comm INTEGER DEFAULT 5,
        skill_prob INTEGER DEFAULT 5,
        skill_cloud INTEGER DEFAULT 5,
        skill_data INTEGER DEFAULT 5,
        skill_cyber INTEGER DEFAULT 5
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS leaderboard (
        username TEXT PRIMARY KEY,
        career TEXT,
        xp INTEGER DEFAULT 0,
        progress INTEGER DEFAULT 0,
        streak INTEGER DEFAULT 0,
        level INTEGER DEFAULT 1,
        updated_at TEXT DEFAULT CURRENT_TIMESTAMP
    )""")
    conn.commit()

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()

def register_user(username: str, password: str) -> bool:
    try:
        conn = get_conn()
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?,?)",
                  (username, hash_password(password)))
        c.execute("INSERT OR IGNORE INTO user_stats (username) VALUES (?)", (username,))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def login_user(username: str, password: str) -> bool:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username=?", (username,))
    row = c.fetchone()
    if row is None:
        return False
    # Legacy users migrated with empty password: set their password on first login
    if row[0] == "":
        conn2 = get_conn()
        c2 = conn2.cursor()
        c2.execute("UPDATE users SET password=? WHERE username=?", (hash_password(password), username))
        conn2.commit()
        return True
    return row[0] == hash_password(password)

def load_stats(username: str) -> dict:
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT * FROM user_stats WHERE username=?", (username,))
    row = c.fetchone()
    if row is None:
        conn2 = get_conn()
        c2 = conn2.cursor()
        c2.execute("INSERT OR IGNORE INTO user_stats (username) VALUES (?)", (username,))
        conn2.commit()
        return load_stats(username)
    cols = [
        "username","career","xp","level","streak","last_login","progress",
        "completed_tasks","achievements",
        "skill_python","skill_sql","skill_ml","skill_web","skill_uiux",
        "skill_comm","skill_prob","skill_cloud","skill_data","skill_cyber"
    ]
    d = dict(zip(cols, row))
    d["completed_tasks"] = json.loads(d["completed_tasks"] or "[]")
    d["achievements"]    = json.loads(d["achievements"]    or "[]")
    # Randomize skill defaults for brand-new users (all skills == 5 means never set)
    skill_keys = ["skill_python","skill_sql","skill_ml","skill_web","skill_uiux",
                  "skill_comm","skill_prob","skill_cloud","skill_data","skill_cyber"]
    if all(d.get(k, 5) == 5 for k in skill_keys):
        for k in skill_keys:
            d[k] = random.randint(0, 10)
    return d

def save_stats(stats: dict):
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_stats
            (username,career,xp,level,streak,last_login,progress,completed_tasks,achievements,
             skill_python,skill_sql,skill_ml,skill_web,skill_uiux,
             skill_comm,skill_prob,skill_cloud,skill_data,skill_cyber)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(username) DO UPDATE SET
            career=excluded.career, xp=excluded.xp, level=excluded.level,
            streak=excluded.streak, last_login=excluded.last_login,
            progress=excluded.progress, completed_tasks=excluded.completed_tasks,
            achievements=excluded.achievements,
            skill_python=excluded.skill_python, skill_sql=excluded.skill_sql,
            skill_ml=excluded.skill_ml, skill_web=excluded.skill_web,
            skill_uiux=excluded.skill_uiux, skill_comm=excluded.skill_comm,
            skill_prob=excluded.skill_prob, skill_cloud=excluded.skill_cloud,
            skill_data=excluded.skill_data, skill_cyber=excluded.skill_cyber
    """, (
        stats["username"], stats.get("career",""), stats.get("xp",0),
        stats.get("level",1), stats.get("streak",0),
        datetime.now().isoformat(),
        stats.get("progress",0),
        json.dumps(stats.get("completed_tasks",[])),
        json.dumps(stats.get("achievements",[])),
        stats.get("skill_python",5), stats.get("skill_sql",5),
        stats.get("skill_ml",5),    stats.get("skill_web",5),
        stats.get("skill_uiux",5),  stats.get("skill_comm",5),
        stats.get("skill_prob",5),  stats.get("skill_cloud",5),
        stats.get("skill_data",5),  stats.get("skill_cyber",5),
    ))
    # leaderboard
    c.execute("""
        INSERT INTO leaderboard (username,career,xp,progress,streak,level,updated_at)
        VALUES (?,?,?,?,?,?,?)
        ON CONFLICT(username) DO UPDATE SET
            career=excluded.career, xp=excluded.xp, progress=excluded.progress,
            streak=excluded.streak, level=excluded.level, updated_at=excluded.updated_at
    """, (
        stats["username"], stats.get("career",""), stats.get("xp",0),
        stats.get("progress",0), stats.get("streak",0), stats.get("level",1),
        datetime.now().isoformat()
    ))
    conn.commit()

def fetch_leaderboard():
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT username,career,xp,progress,streak,level FROM leaderboard ORDER BY xp DESC LIMIT 10")
    rows = c.fetchall()
    return rows

# ──────────────────────────────────────────────────────────────
# MODEL
# ──────────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    model_path = "model.pkl"
    if not os.path.exists(model_path):
        # Train a fresh model from the dataset
        try:
            df = pd.read_csv("dataset.csv")
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split
            X = df.drop("Career", axis=1)
            y = df["Career"]
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            with open(model_path, "wb") as f:
                pickle.dump(model, f)
            return model
        except Exception as e:
            st.error(f"Could not train model: {e}")
            return None
    with open(model_path, "rb") as f:
        return pickle.load(f)

# ──────────────────────────────────────────────────────────────
# XP & LEVEL HELPERS
# ──────────────────────────────────────────────────────────────
def xp_for_level(lvl: int) -> int:
    return lvl * 100

def compute_level(xp: int) -> int:
    lvl = 1
    while xp >= xp_for_level(lvl):
        xp -= xp_for_level(lvl)
        lvl += 1
    return lvl

def check_achievements(stats: dict) -> list:
    earned = list(stats.get("achievements", []))
    xp = stats.get("xp", 0)
    ct = stats.get("completed_tasks", [])
    progress = stats.get("progress", 0)

    if stats.get("career") and "First Prediction" not in earned:
        earned.append("First Prediction")
    if xp >= 100 and "100 XP Club" not in earned:
        earned.append("100 XP Club")
    if len(ct) >= 1 and "Skill Starter" not in earned:
        earned.append("Skill Starter")
    if progress >= 50 and "Halfway There" not in earned:
        earned.append("Halfway There")
    if progress >= 100 and "Roadmap Complete" not in earned:
        earned.append("Roadmap Complete")
    if xp >= 200 and "XP Master" not in earned:
        earned.append("XP Master")
    return earned

def plant_stage(progress: int):
    if progress < 20:   return "🌱", "Seed",          "#4ade80"
    elif progress < 40: return "🌿", "Sprout",         "#22c55e"
    elif progress < 60: return "🪴", "Young Plant",    "#16a34a"
    elif progress < 80: return "🌳", "Mature Tree",    "#15803d"
    else:               return "🌸", "Blooming Flower","#f472b6"

# ──────────────────────────────────────────────────────────────
# CSS
# ──────────────────────────────────────────────────────────────
def inject_css():
    st.markdown("""
<style>
/* ── Google Font ── */
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@400;500;600;700&family=Exo+2:wght@300;400;500;600;700&display=swap');

/* ── Global Reset ── */
*, *::before, *::after { box-sizing: border-box; }

.stApp {
    background: radial-gradient(ellipse at 20% 10%, #0d2137 0%, #071120 50%, #030b17 100%);
    font-family: 'Exo 2', sans-serif;
    color: #e2e8f0;
    min-height: 100vh;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #071120; }
::-webkit-scrollbar-thumb { background: #00BFFF44; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #00BFFF88; }

/* ── Hero title ── */
.hero-title {
    font-family: 'Rajdhani', sans-serif;
    font-size: clamp(2.5rem, 6vw, 5rem);
    font-weight: 700;
    background: linear-gradient(135deg, #00BFFF 0%, #4F9CF9 40%, #7DD3FC 70%, #00BFFF 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 4s ease infinite;
    line-height: 1.1;
    margin-bottom: 0.25rem;
}
.hero-sub {
    font-family: 'Exo 2', sans-serif;
    font-size: 1.1rem;
    color: #7DD3FC88;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 2rem;
}
@keyframes gradientShift {
    0%   { background-position: 0% 50%; }
    50%  { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* ── Glass card ── */
.glass-card {
    background: linear-gradient(135deg, rgba(0,191,255,0.06) 0%, rgba(15,30,55,0.7) 100%);
    border: 1px solid rgba(0,191,255,0.2);
    border-radius: 18px;
    padding: 1.6rem 2rem;
    backdrop-filter: blur(14px);
    box-shadow: 0 0 30px rgba(0,191,255,0.08), 0 8px 32px rgba(0,0,0,0.4);
    margin-bottom: 1.25rem;
    transition: border-color 0.3s, box-shadow 0.3s;
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 2px;
    background: linear-gradient(90deg, transparent, #00BFFF, transparent);
    opacity: 0.5;
}
.glass-card:hover {
    border-color: rgba(0,191,255,0.45);
    box-shadow: 0 0 45px rgba(0,191,255,0.18), 0 8px 32px rgba(0,0,0,0.5);
}

/* ── Section headers ── */
.section-header {
    font-family: 'Rajdhani', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: #00BFFF;
    letter-spacing: 0.05em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0,191,255,0.15);
}

/* ── Career prediction card ── */
.career-card {
    background: linear-gradient(135deg, rgba(0,191,255,0.12) 0%, rgba(79,156,249,0.08) 100%);
    border: 2px solid rgba(0,191,255,0.4);
    border-radius: 20px;
    padding: 2rem;
    text-align: center;
    box-shadow: 0 0 60px rgba(0,191,255,0.2), inset 0 0 30px rgba(0,191,255,0.05);
    animation: pulseGlow 3s ease-in-out infinite;
    position: relative;
    overflow: hidden;
}
.career-card::after {
    content: '';
    position: absolute;
    top: -50%; left: -50%;
    width: 200%; height: 200%;
    background: conic-gradient(from 0deg, transparent 0deg, rgba(0,191,255,0.05) 60deg, transparent 120deg);
    animation: rotateSlow 8s linear infinite;
}
@keyframes pulseGlow {
    0%,100% { box-shadow: 0 0 40px rgba(0,191,255,0.2); }
    50%      { box-shadow: 0 0 80px rgba(0,191,255,0.4); }
}
@keyframes rotateSlow { 100% { transform: rotate(360deg); } }

.career-icon   { font-size: 4rem; display: block; margin-bottom: 0.5rem; }
.career-title  { font-family: 'Rajdhani', sans-serif; font-size: 2rem; font-weight: 700; color: #00BFFF; }
.career-conf   { font-size: 1rem; color: #7DD3FC; margin-top: 0.3rem; letter-spacing: 0.1em; }

/* ── Stat pill ── */
.stat-pill {
    display: inline-flex; align-items: center; gap: 0.4rem;
    background: rgba(0,191,255,0.1);
    border: 1px solid rgba(0,191,255,0.25);
    border-radius: 999px;
    padding: 0.35rem 0.9rem;
    font-size: 0.85rem; font-weight: 600;
    color: #7DD3FC;
    margin: 0.2rem;
}

/* ── Progress bar custom ── */
.prog-wrap { margin: 0.5rem 0; }
.prog-label { font-size: 0.95rem; color: #ffffff; font-weight: 600; margin-bottom: 0.3rem; display: flex; justify-content: space-between; }
.prog-track {
    background: rgba(255,255,255,0.05);
    border-radius: 999px; height: 8px; overflow: hidden;
    border: 1px solid rgba(0,191,255,0.1);
}
.prog-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #00BFFF, #4F9CF9, #7DD3FC);
    box-shadow: 0 0 10px #00BFFF88;
    transition: width 0.8s cubic-bezier(0.34,1.56,0.64,1);
}

/* ── Badge card ── */
.badge-grid { display: flex; flex-wrap: wrap; gap: 0.75rem; margin-top: 0.5rem; }
.badge-card {
    background: rgba(0,191,255,0.08);
    border: 1px solid rgba(0,191,255,0.2);
    border-radius: 14px;
    padding: 0.75rem 1rem;
    text-align: center; min-width: 120px;
    transition: all 0.3s;
}
.badge-card.earned {
    background: linear-gradient(135deg, rgba(0,191,255,0.18), rgba(79,156,249,0.12));
    border-color: rgba(0,191,255,0.5);
    box-shadow: 0 0 20px rgba(0,191,255,0.2);
}
.badge-card.locked { opacity: 0.35; filter: grayscale(0.8); }
.badge-icon { font-size: 1.8rem; display: block; }
.badge-name { font-size: 0.72rem; color: #7DD3FC; font-weight: 600; margin-top: 0.25rem; letter-spacing: 0.05em; }

/* ── Plant showcase ── */
.plant-showcase {
    text-align: center;
    padding: 2rem;
    background: radial-gradient(ellipse at center, rgba(0,191,255,0.08) 0%, transparent 70%);
    border-radius: 20px;
}
.plant-emoji { font-size: 6rem; display: block; animation: floatPlant 4s ease-in-out infinite; }
.plant-name  { font-family: 'Rajdhani', sans-serif; font-size: 1.7rem; font-weight: 700; margin-top: 0.5rem; color: #ffffff; }
@keyframes floatPlant {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-12px); }
}

/* ── XP bar ── */
.xp-bar-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 999px; height: 12px;
    border: 1px solid rgba(0,191,255,0.15); overflow: hidden; margin-top: 0.3rem;
}
.xp-bar-fill {
    height: 100%; border-radius: 999px;
    background: linear-gradient(90deg, #f59e0b, #fbbf24, #fcd34d);
    box-shadow: 0 0 12px #f59e0baa;
    transition: width 1s ease;
}

/* ── Sidebar styling ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #051018 0%, #071120 100%) !important;
    border-right: 1px solid rgba(0,191,255,0.12) !important;
}
[data-testid="stSidebar"] .stSlider { margin-bottom: 0.25rem; }

/* ── Streamlit overrides ── */
div.stButton > button {
    background: linear-gradient(135deg, #00BFFF, #4F9CF9) !important;
    color: #071120 !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 700 !important; font-size: 1rem !important;
    letter-spacing: 0.08em !important;
    border: none !important; border-radius: 12px !important;
    padding: 0.6rem 1.8rem !important;
    box-shadow: 0 4px 24px rgba(0,191,255,0.35) !important;
    transition: all 0.25s !important;
}
div.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 32px rgba(0,191,255,0.55) !important;
    background: linear-gradient(135deg, #22d3ee, #60a5fa) !important;
}
.stTextInput > div > div > input, .stTextInput > div > div > input:focus {
    background: rgba(240,248,255,0.92) !important;
    border: 1px solid rgba(0,191,255,0.4) !important;
    border-radius: 10px !important;
    color: #000000 !important;
    caret-color: #000000 !important;
}
.stTextInput label, .stTextInput > label { color: #7DD3FC !important; }
.stCheckbox > label { color: #ffffff !important; font-size: 1.05rem !important; font-weight: 500 !important; }
.stCheckbox label p { color: #ffffff !important; font-size: 1.05rem !important; font-weight: 500 !important; }
.stCheckbox span { color: #ffffff !important; font-size: 1.05rem !important; font-weight: 500 !important; }
[data-testid="stCheckbox"] label { color: #ffffff !important; font-size: 1.05rem !important; font-weight: 500 !important; }
[data-testid="stCheckbox"] p { color: #ffffff !important; font-size: 1.05rem !important; font-weight: 500 !important; }
[data-testid="stCheckbox"] span[data-testid="stMarkdownContainer"] p { color: #ffffff !important; font-size: 1.05rem !important; }
.stTabs [data-baseweb="tab-list"] { gap: 0.5rem; background: transparent !important; }
.stTabs [data-baseweb="tab"] {
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important; font-size: 0.95rem !important;
    color: #7DD3FC88 !important;
    background: rgba(0,191,255,0.06) !important;
    border-radius: 10px 10px 0 0 !important;
    border: 1px solid rgba(0,191,255,0.1) !important;
    padding: 0.5rem 1.2rem !important;
    transition: all 0.25s !important;
}
.stTabs [aria-selected="true"] {
    color: #00BFFF !important;
    background: rgba(0,191,255,0.14) !important;
    border-color: rgba(0,191,255,0.35) !important;
}
h1, h2, h3 { font-family: 'Rajdhani', sans-serif !important; color: #4F9CF9 !important; }
.stSuccess { background: rgba(0,191,255,0.12) !important; border: 1px solid rgba(0,191,255,0.3) !important; border-radius: 10px !important; }
.stInfo    { background: rgba(79,156,249,0.10) !important; border: 1px solid rgba(79,156,249,0.3) !important; border-radius: 10px !important; }
.stWarning { background: rgba(251,191,36,0.10) !important; border: 1px solid rgba(251,191,36,0.3) !important; border-radius: 10px !important; }
div[data-testid="stMetric"] {
    background: rgba(0,191,255,0.06) !important;
    border: 1px solid rgba(0,191,255,0.2) !important;
    border-radius: 14px !important; padding: 0.75rem !important;
}
div[data-testid="stMetric"] label { color: #7DD3FC88 !important; font-size: 0.8rem !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color: #00BFFF !important; font-family: 'Rajdhani', sans-serif !important; font-size: 1.8rem !important; font-weight: 700 !important; }
.stDataFrame { border-radius: 12px !important; overflow: hidden !important; }
footer { visibility: hidden; }
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# HELPER WIDGETS
# ──────────────────────────────────────────────────────────────
def glass_card(content_fn, **kwargs):
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    content_fn(**kwargs)
    st.markdown('</div>', unsafe_allow_html=True)

def section_header(icon: str, title: str):
    st.markdown(f'<div class="section-header">{icon} {title}</div>', unsafe_allow_html=True)

def progress_bar(label: str, value: int, color: str = "#00BFFF"):
    st.markdown(f"""
    <div class="prog-wrap">
        <div class="prog-label"><span>{label}</span><span>{value}%</span></div>
        <div class="prog-track">
            <div class="prog-fill" style="width:{value}%; background: linear-gradient(90deg, {color}, {color}cc);"></div>
        </div>
    </div>""", unsafe_allow_html=True)

def render_badges(earned: list):
    html = '<div class="badge-grid">'
    for name, info in BADGES.items():
        cls = "earned" if name in earned else "locked"
        html += f"""
        <div class="badge-card {cls}" title="{info['desc']}">
            <span class="badge-icon">{info['icon']}</span>
            <div class="badge-name">{name}</div>
        </div>"""
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def xp_progress_bar(xp: int, level: int, progress_pct: int = None):
    # XP is driven by roadmap progress (0-200 XP for 0-100% tasks)
    MAX_XP = 200
    # If roadmap progress known, derive XP from it; else use stored xp capped at 200
    if progress_pct is not None:
        display_xp = int((progress_pct / 100) * MAX_XP)
    else:
        display_xp = min(xp, MAX_XP)
    pct = int((display_xp / MAX_XP) * 100)
    st.markdown(f"""
    <div style="font-size:1rem; color:#ffffff; font-weight:600; margin-bottom:0.3rem; display:flex; justify-content:space-between;">
        <span>⭐ XP Progress</span><span style="color:#f59e0b;">{display_xp} / {MAX_XP} XP</span>
    </div>
    <div class="xp-bar-wrap">
        <div class="xp-bar-fill" style="width:{pct}%"></div>
    </div>""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# RADAR CHART
# ──────────────────────────────────────────────────────────────
def make_radar(skills: dict) -> go.Figure:
    cats = list(skills.keys())
    vals = list(skills.values())
    cats_closed = cats + [cats[0]]
    vals_closed  = vals + [vals[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals_closed, theta=cats_closed,
        fill='toself',
        fillcolor='rgba(0,191,255,0.12)',
        line=dict(color='#00BFFF', width=2.5),
        name='Skills',
    ))
    fig.update_layout(
        polar=dict(
            bgcolor='rgba(7,17,32,0.6)',
            radialaxis=dict(
                visible=True, range=[0,10],
                tickfont=dict(size=9, color='rgba(125,211,252,0.33)'),
                gridcolor='rgba(0,191,255,0.1)',
                linecolor='rgba(0,191,255,0.15)',
            ),
            angularaxis=dict(
                tickfont=dict(size=10, color='#7DD3FC'),
                gridcolor='rgba(0,191,255,0.1)',
                linecolor='rgba(0,191,255,0.15)',
            ),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(t=30, b=30, l=40, r=40),
    )
    return fig

# ──────────────────────────────────────────────────────────────
# PDF EXPORT
# ──────────────────────────────────────────────────────────────
def generate_pdf_report(stats: dict, skills: dict) -> bytes:
    try:
        from fpdf import FPDF
    except ImportError:
        return b""

    # Sanitize: replace unicode chars unsupported by Helvetica with ASCII equivalents
    def s(text: str) -> str:
        text = str(text)
        replacements = {
            "–": "-",   # en dash
            "—": "--",  # em dash
            "‘": "'",   # left single quote
            "’": "'",   # right single quote
            "“": '"',   # left double quote
            "”": '"',   # right double quote
            "…": "...", # ellipsis
            "•": "*",   # bullet
            " ": " ",   # non-breaking space
            "✓": "[DONE]",  # checkmark
            "○": "[ ]",    # circle
            "→": "->",  # arrow
        }
        for uni, asc in replacements.items():
            text = text.replace(uni, asc)
        # Strip any remaining non-latin-1 chars (emojis etc)
        return text.encode("latin-1", errors="ignore").decode("latin-1")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Header
    pdf.set_font("Helvetica", "B", 24)
    pdf.set_text_color(0, 100, 180)
    pdf.cell(0, 14, s("SkillForge AI - Career Report"), ln=True, align="C")
    pdf.set_font("Helvetica", size=10)
    pdf.set_text_color(100, 100, 100)
    pdf.cell(0, 8, s(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}"), ln=True, align="C")
    pdf.ln(6)

    def section(title):
        pdf.set_font("Helvetica", "B", 14)
        pdf.set_text_color(0, 100, 180)
        pdf.cell(0, 10, s(title), ln=True)
        pdf.set_draw_color(0, 100, 180)
        pdf.set_line_width(0.4)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(3)

    def row(label, value):
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_text_color(60, 60, 60)
        pdf.cell(60, 7, s(label), ln=False)
        pdf.set_font("Helvetica", size=10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, s(str(value)), ln=True)

    # User info
    section("User Profile")
    row("Username:",    stats.get("username", ""))
    row("Career Path:", stats.get("career", "N/A"))
    row("Level:",       stats.get("level", 1))
    row("Total XP:",    min(stats.get("xp", 0), 200))
    row("Streak:",      f"{stats.get('streak', 0)} days")
    row("Progress:",    f"{stats.get('progress', 0)}%")
    pdf.ln(4)

    # Skills
    section("Skill Assessment")
    for name, val in skills.items():
        row(f"  {name}:", f"{val} / 10")
    pdf.ln(4)

    # Roadmap
    career = stats.get("career", "")
    tasks  = ROADMAPS.get(career, [])
    done   = stats.get("completed_tasks", [])
    section("Roadmap Progress")
    for t in tasks:
        status = "[DONE]" if t in done else "[    ]"
        pdf.set_font("Helvetica", size=10)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 7, s(f"  {status} {t}"), ln=True)

    # Footer
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(140, 140, 140)
    pdf.cell(0, 6, s("SkillForge AI -- Cultivate Skills. Grow Your Future."), ln=True, align="C")

    result = pdf.output(dest="S")
    return bytes(result) if isinstance(result, bytearray) else result

# ──────────────────────────────────────────────────────────────
# AUTH PAGE
# ──────────────────────────────────────────────────────────────
def render_auth():
    # Animated particle header
    st.markdown("""
    <div style="text-align:center; padding: 3rem 0 1rem;">
        <div class="hero-title">SkillForge AI</div>
        <div class="hero-sub">Cultivate Skills. Grow Your Future.</div>
    </div>
    """, unsafe_allow_html=True)

    col_gap1, col_main, col_gap2 = st.columns([1.2, 1, 1.2])
    with col_main:
        st.markdown('<div class="glass-card" style="padding:2.2rem 2.5rem;">', unsafe_allow_html=True)
        tab_login, tab_reg = st.tabs(["🔑 Sign In", "✨ Create Account"])

        with tab_login:
            st.markdown("#### Welcome back")
            l_user = st.text_input("Username", key="l_user", placeholder="your_username")
            l_pass = st.text_input("Password", type="password", key="l_pass", placeholder="••••••••")
            if st.button("Sign In →", key="btn_login", use_container_width=True):
                if login_user(l_user, l_pass):
                    st.session_state["logged_in"] = True
                    st.session_state["username"] = l_user
                    st.rerun()
                else:
                    st.error("Invalid credentials — please try again.")

        with tab_reg:
            st.markdown("#### Join the forge")
            r_user = st.text_input("Choose Username", key="r_user", placeholder="forge_hero")
            r_pass = st.text_input("Password", type="password", key="r_pass", placeholder="strong password")
            r_pass2= st.text_input("Confirm Password", type="password", key="r_pass2", placeholder="repeat password")
            if st.button("Create Account →", key="btn_reg", use_container_width=True):
                if r_pass != r_pass2:
                    st.error("Passwords do not match.")
                elif len(r_user) < 3 or len(r_pass) < 4:
                    st.warning("Username ≥ 3 chars, password ≥ 4 chars.")
                elif register_user(r_user, r_pass):
                    st.success("Account created! Please sign in.")
                else:
                    st.error("Username already taken — try another.")

        st.markdown('</div>', unsafe_allow_html=True)

    # Feature pills below
    st.markdown("""
    <div style="text-align:center; margin-top:2rem; opacity:0.6; font-size:0.82rem; letter-spacing:0.1em; color:#7DD3FC;">
        🤖 AI CAREER PREDICTION &nbsp;|&nbsp; 🌱 DIGITAL GARDEN &nbsp;|&nbsp;
        🏆 GAMIFICATION &nbsp;|&nbsp; 📊 SKILL ANALYTICS &nbsp;|&nbsp; 📄 PDF EXPORT
    </div>
    """, unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────
def render_sidebar(stats: dict) -> dict:
    with st.sidebar:
        # User profile block
        st.markdown(f"""
        <div style="text-align:center; padding:1rem 0 0.5rem;">
            <div style="font-size:2.5rem;">👾</div>
            <div style="font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700; color:#00BFFF;">
                {stats['username']}
            </div>
            <div style="font-size:0.88rem; color:#ffffff; font-weight:600; letter-spacing:0.1em;">LEVEL {stats['level']} FORGER</div>
        </div>
        """, unsafe_allow_html=True)
        xp_progress_bar(stats["xp"], stats["level"], progress_pct=stats.get("progress", 0))
        st.markdown(f"""
        <div style="display:flex; justify-content:center; gap:0.5rem; margin:0.75rem 0;">
            <span class="stat-pill">⭐ {min(stats['xp'], 200)} XP</span>
            <span class="stat-pill">🔥 {stats['streak']}d streak</span>
        </div>
        """, unsafe_allow_html=True)
        st.divider()

        # Skill sliders
        st.markdown('<div style="font-family:\'Rajdhani\',sans-serif; font-size:1.1rem; font-weight:700; color:#00BFFF; letter-spacing:0.05em; margin-bottom:0.5rem;">⚡ SKILL ASSESSMENT</div>', unsafe_allow_html=True)

        skill_keys = [
            ("Python",          "skill_python", "🐍"),
            ("SQL",             "skill_sql",    "🗄️"),
            ("Machine Learning","skill_ml",     "🤖"),
            ("Web Development", "skill_web",    "🌐"),
            ("UI/UX",           "skill_uiux",   "🎨"),
            ("Communication",   "skill_comm",   "💬"),
            ("Problem Solving", "skill_prob",   "🧩"),
            ("Cloud",           "skill_cloud",  "☁️"),
            ("Data Analysis",   "skill_data",   "📊"),
            ("Cybersecurity",   "skill_cyber",  "🔐"),
        ]
        skills = {}
        for label, key, icon in skill_keys:
            default_val = stats.get(key) if stats.get(key, -1) != -1 else random.randint(0, 10)
            val = st.slider(f"{icon} {label}", 0, 10, default_val, key=f"sl_{key}")
            skills[label] = val

        st.divider()
        st.markdown('<div style="font-family:\'Rajdhani\',sans-serif; font-size:1rem; font-weight:700; color:#00BFFF; margin-bottom:0.5rem;">🔑 AI API KEY</div>', unsafe_allow_html=True)
        api_key_input = st.text_input(
            "Gemini / Any AI API Key",
            type="password",
            placeholder="AIza... (Gemini) or any key",
            key="ai_api_key_input",
            label_visibility="collapsed",
            help="Enter Gemini API key (or any compatible key) to unlock AI Mentor, Study Plan & Resume features"
        )
        if api_key_input:
            st.session_state["ai_api_key"] = api_key_input
            st.success("✅ API key saved", icon="🔑")
        elif "ai_api_key" not in st.session_state:
            st.caption("⚠️ Enter key to unlock AI features")
        st.divider()
        if st.button("🚪 Logout", use_container_width=True, key="btn_logout"):
            for k in ["logged_in","username","stats"]:
                st.session_state.pop(k, None)
            st.rerun()

    return skills

# ──────────────────────────────────────────────────────────────
# MAIN APP
# ──────────────────────────────────────────────────────────────
def render_app(stats: dict):
    skills = render_sidebar(stats)

    # ── CHATBASE WIDGET (bottom-right, shown after login) ──────
    components.html("""
    <script>
    (function(){
      if(!window.parent.chatbase || window.parent.chatbase("getState") !== "initialized"){
        window.parent.chatbase = (...args) => {
          if(!window.parent.chatbase.q){ window.parent.chatbase.q = [] }
          window.parent.chatbase.q.push(args)
        };
        window.parent.chatbase = new Proxy(window.parent.chatbase, {
          get(target, prop){
            if(prop === "q"){ return target.q }
            return (...args) => target(prop, ...args)
          }
        })
      }
      const onLoad = function(){
        const script = document.createElement("script");
        script.src = "https://www.chatbase.co/embed.min.js";
        script.id = "Sl0q4y9ILFqIdK8szW1Gv";
        script.setAttribute("domain", "www.chatbase.co");
        window.parent.document.body.appendChild(script);
      };
      if(window.parent.document.readyState === "complete"){ onLoad(); }
      else { window.parent.addEventListener("load", onLoad); }
    })();
    </script>
    """, height=0, scrolling=False)


    # Sync sliders into stats
    skill_map = {
        "Python": "skill_python", "SQL": "skill_sql",
        "Machine Learning": "skill_ml", "Web Development": "skill_web",
        "UI/UX": "skill_uiux", "Communication": "skill_comm",
        "Problem Solving": "skill_prob", "Cloud": "skill_cloud",
        "Data Analysis": "skill_data", "Cybersecurity": "skill_cyber",
    }
    for label, key in skill_map.items():
        stats[key] = skills[label]

    # ── Hero ──────────────────────────────────────────────────
    if True:  # full width hero
        st.markdown(f"""
        <div class="hero-title">SkillForge AI</div>
        <div class="hero-sub">Cultivate Skills. Grow Your Future.</div>
        """, unsafe_allow_html=True)


    st.divider()

    # ── TABS ──────────────────────────────────────────────────
    tabs = st.tabs([
        "🎯 Prediction",
        "🎮 Skill Challenge",
        "📅 Smart Scheduler",
        "🗺️ Roadmap",
        "🏆 Leaderboard",
        "📄 Export",
    ])

    # ── TAB 1: PREDICTION ─────────────────────────────────────
    with tabs[0]:
        section_header("🎯", "AI Career Prediction")
        model = load_model()

        col_pred, col_radar = st.columns([1, 1])
        with col_pred:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("##### Your current skill profile")
            for label, val in skills.items():
                progress_bar(label, val * 10)
            st.markdown('</div>', unsafe_allow_html=True)

            if st.button("⚡ Predict My Career Path", key="btn_predict", use_container_width=True):
                if model is None:
                    st.error("Model not loaded. Please ensure model.pkl exists.")
                else:
                    input_arr = [[
                        skills["Python"], skills["SQL"], skills["Machine Learning"],
                        skills["Web Development"], skills["UI/UX"], skills["Communication"],
                        skills["Problem Solving"], skills["Cloud"], skills["Data Analysis"],
                        skills["Cybersecurity"],
                    ]]
                    prediction  = model.predict(input_arr)[0]
                    probability = max(model.predict_proba(input_arr)[0]) * 100

                    # Save to stats
                    stats["career"] = prediction
                    stats["xp"]    = stats.get("xp", 0) + 25
                    stats["level"] = compute_level(stats["xp"])
                    stats["achievements"] = check_achievements(stats)
                    save_stats(stats)
                    st.session_state["stats"] = stats
                    st.session_state["last_prediction"] = (prediction, probability)
                    st.balloons()

            # Show last prediction if exists
            if "last_prediction" in st.session_state:
                pred, prob = st.session_state["last_prediction"]
                icon = CAREER_ICONS.get(pred, "💼")
                st.markdown(f"""
                <div class="career-card" style="margin-top:1rem;">
                    <span class="career-icon">{icon}</span>
                    <div class="career-title">{pred}</div>
                </div>
                """, unsafe_allow_html=True)

                # Career Readiness Analysis (no gap skills shown)
                st.markdown('<div class="glass-card" style="margin-top:1rem;">', unsafe_allow_html=True)
                st.markdown("##### 🔍 Career Readiness Analysis")
                career_skill_targets = {
                    "Data Scientist":       [8,8,9,3,2,7,9,5,9,2],
                    "ML Engineer":          [8,7,8,4,2,6,8,5,8,2],
                    "Frontend Developer":   [5,3,2,9,8,8,6,2,3,1],
                    "Backend Developer":    [7,6,4,8,2,6,8,5,4,3],
                    "UI UX Designer":       [3,2,1,7,10,9,5,1,2,1],
                    "Cybersecurity Analyst":[5,4,3,5,2,7,9,6,4,10],
                    "Software Engineer":    [7,6,6,8,3,7,8,6,5,3],
                    "Cloud Engineer":       [7,7,5,6,2,6,8,10,6,4],
                    "DevOps Engineer":      [6,6,5,7,2,6,8,9,5,4],
                }
                labels = list(skills.keys())
                targets = career_skill_targets.get(pred, [7]*10)
                vals = list(skills.values())
                readiness = sum(min(v, t) for v, t in zip(vals, targets)) / sum(targets) * 100
                progress_bar(f"Overall Readiness for {pred}", int(readiness), "#4F9CF9")
                st.markdown('</div>', unsafe_allow_html=True)

        with col_radar:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            section_header("📡", "Skill Radar")
            fig = make_radar(skills)
            st.plotly_chart(fig, use_container_width=True, key="radar_main")
            st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 2: ANALYTICS ──────────────────────────────────────
    # ── TAB 2: SKILL CHALLENGE ────────────────────────────────
    with tabs[1]:
        section_header("🎮", "Skill Challenge Mode")
        career = stats.get("career", "")
        questions = QUIZ_DATA.get(career, [])

        if not career or not questions:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:2.5rem;">
                <div style="font-size:3rem;">🎯</div>
                <div style="font-size:1.2rem; color:#00BFFF; font-weight:700; margin-top:1rem;">Run a Career Prediction First</div>
                <div style="color:#7DD3FC; margin-top:0.5rem;">Complete the prediction to unlock career-specific quiz questions.</div>
            </div>""", unsafe_allow_html=True)
        else:
            # Init quiz state
            if "quiz_idx" not in st.session_state:
                st.session_state["quiz_idx"]      = 0
                st.session_state["quiz_score"]    = 0
                st.session_state["quiz_answered"] = False
                st.session_state["quiz_selected"] = None
                st.session_state["quiz_complete"] = False
                import random as _random
                st.session_state["quiz_order"]    = _random.sample(range(len(questions)), len(questions))

            q_order   = st.session_state["quiz_order"]
            q_idx     = st.session_state["quiz_idx"]
            score     = st.session_state["quiz_score"]
            total_q   = len(q_order)
            answered  = st.session_state["quiz_answered"]
            complete  = st.session_state["quiz_complete"]

            # ── Score bar at top ──
            col_sc1, col_sc2, col_sc3 = st.columns(3)
            col_sc1.markdown(
                f'<div class="glass-card" style="text-align:center;">'
                f'<div style="font-size:0.8rem; color:#7DD3FC88;">Question</div>'
                f'<div style="font-family:\'Rajdhani\',sans-serif; font-size:1.8rem; font-weight:700; color:#00BFFF;">'
                f'{min(q_idx+1, total_q)} / {total_q}</div></div>', unsafe_allow_html=True)
            col_sc2.markdown(
                f'<div class="glass-card" style="text-align:center;">'
                f'<div style="font-size:0.8rem; color:#7DD3FC88;">Score</div>'
                f'<div style="font-family:\'Rajdhani\',sans-serif; font-size:1.8rem; font-weight:700; color:#4ade80;">'
                f'⭐ {score * 5} XP</div></div>', unsafe_allow_html=True)
            col_sc3.markdown(
                f'<div class="glass-card" style="text-align:center;">'
                f'<div style="font-size:0.8rem; color:#7DD3FC88;">Accuracy</div>'
                f'<div style="font-family:\'Rajdhani\',sans-serif; font-size:1.8rem; font-weight:700; color:#f59e0b;">'
                f'{int(score/max(q_idx,1)*100) if q_idx > 0 else 0}%</div></div>', unsafe_allow_html=True)

            if complete:
                # ── Results screen ──
                final_pct = int(score / total_q * 100)
                grade = "🏆 Excellent!" if final_pct >= 80 else "👍 Good Job!" if final_pct >= 60 else "📚 Keep Learning!"
                st.markdown(f"""
                <div class="glass-card" style="text-align:center; padding:2rem;">
                    <div style="font-size:4rem;">{grade.split()[0]}</div>
                    <div style="font-family:'Rajdhani',sans-serif; font-size:2rem; font-weight:700; color:#00BFFF; margin-top:0.5rem;">{grade}</div>
                    <div style="font-size:1.1rem; color:#e2e8f0; margin-top:0.5rem;">
                        You scored <span style="color:#4ade80; font-weight:700;">{score}/{total_q}</span> ({final_pct}%)
                        and earned <span style="color:#f59e0b; font-weight:700;">⭐ {score*5} XP</span>
                    </div>
                </div>""", unsafe_allow_html=True)
                # Award XP
                bonus_xp = score * 5
                if bonus_xp > 0 and not st.session_state.get("quiz_xp_awarded"):
                    stats["xp"] = min(stats.get("xp", 0) + bonus_xp, 200)
                    save_stats(stats)
                    st.session_state["stats"] = stats
                    st.session_state["quiz_xp_awarded"] = True
                    st.success(f"🎉 +{bonus_xp} XP awarded to your profile!")
                if st.button("🔄 Restart Quiz", key="btn_restart_quiz", use_container_width=True):
                    import random as _r
                    st.session_state.update({
                        "quiz_idx": 0, "quiz_score": 0, "quiz_answered": False,
                        "quiz_selected": None, "quiz_complete": False, "quiz_xp_awarded": False,
                        "quiz_order": _r.sample(range(len(questions)), len(questions))
                    })
                    st.rerun()
            else:
                # ── Active question ──
                real_idx = q_order[q_idx]
                q_data   = questions[real_idx]

                st.markdown(f"""
                <div class="glass-card">
                    <div style="font-size:0.8rem; color:#7DD3FC88; margin-bottom:0.75rem;">
                        {career} · Question {q_idx+1}
                    </div>
                    <div style="font-size:1.15rem; color:#ffffff; font-weight:600; line-height:1.5;">
                        {q_data["q"]}
                    </div>
                </div>""", unsafe_allow_html=True)

                opts = q_data["opts"]
                correct_idx = q_data["ans"]

                btn_cols = st.columns(2)
                for i, opt in enumerate(opts):
                    col = btn_cols[i % 2]
                    if answered:
                        if i == correct_idx:
                            col.markdown(
                                f'<div style="background:rgba(74,222,128,0.15); border:2px solid #4ade80;'
                                f'border-radius:10px; padding:0.75rem 1rem; margin:0.3rem 0; color:#4ade80; font-weight:600;">✅ {opt}</div>',
                                unsafe_allow_html=True)
                        elif i == st.session_state["quiz_selected"]:
                            col.markdown(
                                f'<div style="background:rgba(248,113,113,0.15); border:2px solid #f87171;'
                                f'border-radius:10px; padding:0.75rem 1rem; margin:0.3rem 0; color:#f87171; font-weight:600;">❌ {opt}</div>',
                                unsafe_allow_html=True)
                        else:
                            col.markdown(
                                f'<div style="background:rgba(0,191,255,0.04); border:1px solid rgba(0,191,255,0.15);'
                                f'border-radius:10px; padding:0.75rem 1rem; margin:0.3rem 0; color:#7DD3FC;">◦ {opt}</div>',
                                unsafe_allow_html=True)
                    else:
                        if col.button(f"{['A','B','C','D'][i]}. {opt}", key=f"opt_{q_idx}_{i}", use_container_width=True):
                            st.session_state["quiz_selected"] = i
                            st.session_state["quiz_answered"] = True
                            if i == correct_idx:
                                st.session_state["quiz_score"] += 1
                            st.rerun()

                if answered:
                    result_txt = "✅ Correct! +5 XP" if st.session_state["quiz_selected"] == correct_idx else f"❌ Correct answer: {opts[correct_idx]}"
                    result_col = "#4ade80" if st.session_state["quiz_selected"] == correct_idx else "#f87171"
                    st.markdown(
                        f'<div style="color:{result_col}; font-weight:700; font-size:1rem; margin:0.75rem 0;">{result_txt}</div>',
                        unsafe_allow_html=True)

                    next_label = "Next Question ▶" if q_idx < total_q - 1 else "🏁 Finish Quiz"
                    if st.button(next_label, key="btn_next_q", use_container_width=True):
                        if q_idx >= total_q - 1:
                            st.session_state["quiz_complete"] = True
                        else:
                            st.session_state["quiz_idx"]     += 1
                            st.session_state["quiz_answered"] = False
                            st.session_state["quiz_selected"] = None
                        st.rerun()

    # ── TAB 3: SMART SCHEDULER ────────────────────────────────
    with tabs[2]:
        section_header("📅", "Smart Scheduler")
        career     = stats.get("career", "")
        all_tasks  = ROADMAPS.get(career, [])
        done_tasks = stats.get("completed_tasks", [])
        pending    = [t for t in all_tasks if t not in done_tasks]

        if not career:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:2.5rem;">
                <div style="font-size:3rem;">📅</div>
                <div style="font-size:1.2rem; color:#00BFFF; font-weight:700; margin-top:1rem;">Run a Career Prediction First</div>
                <div style="color:#7DD3FC; margin-top:0.5rem;">Complete the prediction to generate your smart schedule.</div>
            </div>""", unsafe_allow_html=True)
        elif not pending:
            st.markdown("""
            <div class="glass-card" style="text-align:center; padding:2.5rem;">
                <div style="font-size:3rem;">🎉</div>
                <div style="font-size:1.2rem; color:#4ade80; font-weight:700; margin-top:1rem;">All Tasks Complete!</div>
                <div style="color:#7DD3FC; margin-top:0.5rem;">You've finished your entire roadmap. Congratulations!</div>
            </div>""", unsafe_allow_html=True)
        else:
            col_cfg, col_cal = st.columns([1, 2])

            with col_cfg:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("##### ⚙️ Schedule Settings")
                hours_pw   = st.slider("Hours available per week", 2, 40, 10, key="sched_hours")
                start_week = st.number_input("Starting week number", 1, 52, 1, key="sched_start")
                show_all   = st.checkbox("Show all pending tasks", value=False, key="sched_showall")
                generate   = st.button("📅 Generate Schedule", key="btn_gen_sched", use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

                st.markdown('<div class="glass-card" style="margin-top:1rem;">', unsafe_allow_html=True)
                st.markdown("##### 📊 Stats")
                total_hours = sum(TASK_DURATIONS.get(t, 5) for t in pending)
                weeks_needed = max(1, -(-total_hours // hours_pw))
                st.markdown(
                    f'<div style="color:#ffffff; font-size:0.95rem; margin:0.4rem 0;">Pending tasks: <b style="color:#00BFFF;">{len(pending)}</b></div>'
                    f'<div style="color:#ffffff; font-size:0.95rem; margin:0.4rem 0;">Est. total hours: <b style="color:#f59e0b;">{total_hours}h</b></div>'
                    f'<div style="color:#ffffff; font-size:0.95rem; margin:0.4rem 0;">Weeks to complete: <b style="color:#4ade80;">{weeks_needed} weeks</b></div>',
                    unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col_cal:
                if generate or "schedule_data" in st.session_state:
                    if generate:
                        # Build schedule: pack tasks into weeks
                        schedule = []
                        current_week = int(start_week)
                        week_hours   = 0
                        week_tasks   = []

                        for task in pending:
                            duration = TASK_DURATIONS.get(task, 5)
                            if week_hours + duration > hours_pw and week_tasks:
                                schedule.append({"week": current_week, "tasks": week_tasks, "hours": week_hours})
                                current_week += 1
                                week_hours    = 0
                                week_tasks    = []
                            week_tasks.append({"task": task, "hours": duration})
                            week_hours += duration

                        if week_tasks:
                            schedule.append({"week": current_week, "tasks": week_tasks, "hours": week_hours})

                        st.session_state["schedule_data"] = schedule

                    schedule = st.session_state.get("schedule_data", [])
                    display  = schedule if show_all else schedule[:6]

                    for week_data in display:
                        wn    = week_data["week"]
                        tasks = week_data["tasks"]
                        wh    = week_data["hours"]
                        fill  = min(int(wh / hours_pw * 100), 100)
                        bar_color = "#4ade80" if fill <= 80 else "#f59e0b" if fill <= 100 else "#f87171"

                        st.markdown(
                            f'<div class="glass-card" style="margin-bottom:0.75rem;">'
                            f'<div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:0.5rem;">'
                            f'<span style="font-family:\'Rajdhani\',sans-serif; font-size:1.1rem; font-weight:700; color:#00BFFF;">📅 Week {wn}</span>'
                            f'<span style="font-size:0.82rem; color:#7DD3FC88;">{wh}h / {hours_pw}h</span></div>'
                            f'<div style="background:rgba(0,191,255,0.08); border-radius:6px; height:6px; margin-bottom:0.75rem;">'
                            f'<div style="width:{fill}%; background:{bar_color}; height:6px; border-radius:6px;"></div></div>',
                            unsafe_allow_html=True)

                        for item in tasks:
                            t  = item["task"]
                            h  = item["hours"]
                            yt = YOUTUBE_RESOURCES.get(t, ("",  ""))
                            done_mark = "✅" if t in done_tasks else "📌"
                            st.markdown(
                                f'<div style="display:flex; justify-content:space-between; align-items:flex-start;'
                                f'padding:0.4rem 0; border-bottom:1px solid rgba(0,191,255,0.08);">'
                                f'<div><span style="color:#ffffff; font-size:0.92rem;">{done_mark} {t}</span>'
                                + (f'<br><a href="{yt[1]}" target="_blank" style="font-size:0.75rem; color:#FF4444; text-decoration:none;">▶ {yt[0]}</a>' if yt[0] else "")
                                + f'</div><span style="font-size:0.8rem; color:#f59e0b; white-space:nowrap; margin-left:0.5rem;">~{h}h</span></div>',
                                unsafe_allow_html=True)

                        st.markdown('</div>', unsafe_allow_html=True)

                    if not show_all and len(schedule) > 6:
                        st.info(f"Showing 6 of {len(schedule)} weeks. Check 'Show all' to see full schedule.")

                    st.download_button(
                        "⬇️ Download Schedule",
                        data="\n\n".join([
                            f"WEEK {w['week']} ({w['hours']}h)\n" + "\n".join([f"  - {t['task']} (~{t['hours']}h)" for t in w['tasks']])
                            for w in st.session_state.get("schedule_data", [])
                        ]),
                        file_name=f"schedule_{stats.get('username','user')}.txt",
                        mime="text/plain", use_container_width=True
                    )
                else:
                    st.markdown("""
                    <div class="glass-card" style="text-align:center; padding:2.5rem;">
                        <div style="font-size:3rem;">🗓️</div>
                        <div style="font-size:1.1rem; color:#00BFFF; font-weight:700; margin-top:1rem;">Ready to Schedule</div>
                        <div style="color:#7DD3FC; margin-top:0.5rem;">Set your weekly hours and click Generate to get a week-by-week task calendar.</div>
                    </div>""", unsafe_allow_html=True)

    with tabs[3]:
        section_header("🗺️", "Personalized Career Roadmap")
        career = stats.get("career", "")

        if not career:
            st.info("Run a career prediction first to unlock your personalized roadmap.")
        else:
            tasks = ROADMAPS.get(career, [])
            done  = stats.get("completed_tasks", [])

            col_rmap, col_plant_mini = st.columns([2, 1])
            with col_rmap:
                st.markdown(f'<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(f"##### 🛣️ Roadmap: **{career}**")
                newly_done = []
                for i, task in enumerate(tasks):
                    is_checked = task in done
                    checked = st.checkbox(
                        f"{i+1}. {task}",
                        value=is_checked,
                        key=f"task_{i}_{task[:20]}"
                    )
                    if checked and task not in done:
                        newly_done.append(task)
                    elif not checked and task in done:
                        done.remove(task)
                    # YouTube resource link under each task
                    if task in YOUTUBE_RESOURCES:
                        yt_title, yt_url = YOUTUBE_RESOURCES[task]
                        st.markdown(
                            f'''<div style="margin:-0.4rem 0 0.6rem 1.8rem;">
                            <a href="{yt_url}" target="_blank"
                               style="font-size:0.78rem; color:#FF4444; text-decoration:none;
                                      display:inline-flex; align-items:center; gap:0.35rem;
                                      background:rgba(255,68,68,0.08); border:1px solid rgba(255,68,68,0.25);
                                      border-radius:20px; padding:0.2rem 0.7rem;">
                                ▶ {yt_title}
                            </a></div>''',
                            unsafe_allow_html=True
                        )

                for t in newly_done:
                    done.append(t)

                total   = len(tasks)
                n_done  = len([t for t in tasks if t in done])
                prog_pct = 100 if (total > 0 and n_done >= total) else (int((n_done / total) * 100) if total > 0 else 0)

                st.markdown(f"""
                <div style="margin-top:1rem;">
                    <div class="prog-label"><span>Overall Progress</span><span>{n_done}/{total} tasks</span></div>
                    <div class="prog-track">
                        <div class="prog-fill" style="width:{prog_pct}%"></div>
                    </div>
                </div>""", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # Save progress — XP = roadmap % × 200 (max 200)
                stats["completed_tasks"] = done
                stats["progress"]        = prog_pct
                stats["xp"]              = int((prog_pct / 100) * 200)
                stats["level"]           = compute_level(stats["xp"])
                stats["achievements"]    = check_achievements(stats)
                save_stats(stats)
                st.session_state["stats"] = stats

            with col_plant_mini:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                plant_emoji, plant_name, plant_color = plant_stage(prog_pct)
                st.markdown(f"""
                <div class="plant-showcase">
                    <span class="plant-emoji">{plant_emoji}</span>
                    <div class="plant-name" style="color:{plant_color};">{plant_name}</div>
                    <div style="font-size:1rem; color:#ffffff; font-weight:600; margin-top:0.4rem;">{prog_pct}% complete</div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

                # XP display — driven by roadmap progress
                roadmap_xp = int((prog_pct / 100) * 200)
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("##### ⭐ XP Progress")
                xp_progress_bar(roadmap_xp, stats["level"], progress_pct=prog_pct)
                st.markdown(f'''
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:0.8rem;">
                    <span style="font-size:1rem; color:#ffffff; font-weight:600;">Earned XP</span>
                    <span style="font-family:\'Rajdhani\',sans-serif; font-size:1.4rem; font-weight:700; color:#f59e0b;">⭐ {roadmap_xp}</span>
                </div>
                <div style="font-size:0.88rem; color:#7DD3FC; margin-top:0.3rem; text-align:right;">{prog_pct}% roadmap → {roadmap_xp}/200 XP</div>
                ''', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

    # ── TAB 4: GARDEN ─────────────────────────────────────────

    with tabs[4]:
        section_header("🏆", "Community Leaderboard")
        rows = fetch_leaderboard()
        if not rows:
            st.info("No community data yet — be the first on the leaderboard!")
        else:
            rank_emojis = ["🥇","🥈","🥉"] + ["🎖️"] * 20
            for i, (uname, career, xp, progress, streak, level) in enumerate(rows):
                is_me = uname == stats["username"]
                bg = "rgba(0,191,255,0.15)" if is_me else "rgba(255,255,255,0.03)"
                border = "rgba(0,191,255,0.5)" if is_me else "rgba(255,255,255,0.08)"
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:1rem; padding:0.9rem 1.2rem;
                     background:{bg}; border:1px solid {border}; border-radius:14px; margin-bottom:0.5rem;">
                    <span style="font-size:1.5rem; min-width:2rem;">{rank_emojis[i]}</span>
                    <div style="flex:1;">
                        <div style="font-weight:700; color:{'#00BFFF' if is_me else '#e2e8f0'};">
                            {uname} {"(you)" if is_me else ""}
                        </div>
                        <div style="font-size:0.78rem; color:#7DD3FC88;">{career or "No career yet"} · Level {level}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-family:'Rajdhani',sans-serif; font-size:1.2rem; font-weight:700; color:#f59e0b;">⭐ {min(xp, 200)}</div>
                        <div style="font-size:0.75rem; color:#7DD3FC88;">{progress}% · 🔥{streak}d</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)


    # ── TAB 6: AI MENTOR CHAT ─────────────────────────────────
    with tabs[5]:
        section_header("📄", "Export Career Report")
        col_ex1, col_ex2 = st.columns(2)

        with col_ex1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("##### 📋 Report Preview")
            st.markdown(f"""
            <table style="width:100%; border-collapse:collapse; font-size:0.9rem; color:#e2e8f0;">
                <tr><td style="padding:6px 8px; color:#7DD3FC88;">Username</td><td style="padding:6px 8px;">{stats['username']}</td></tr>
                <tr><td style="padding:6px 8px; color:#7DD3FC88;">Career Path</td><td style="padding:6px 8px;">{stats.get('career','N/A')}</td></tr>
                <tr><td style="padding:6px 8px; color:#7DD3FC88;">Level</td><td style="padding:6px 8px;">{stats['level']}</td></tr>
                <tr><td style="padding:6px 8px; color:#7DD3FC88;">Total XP</td><td style="padding:6px 8px;">{stats['xp']}</td></tr>
                <tr><td style="padding:6px 8px; color:#7DD3FC88;">Progress</td><td style="padding:6px 8px;">{stats.get('progress',0)}%</td></tr>
                <tr><td style="padding:6px 8px; color:#7DD3FC88;">Streak</td><td style="padding:6px 8px;">{stats.get('streak',0)} days</td></tr>

            </table>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col_ex2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("##### 📥 Download PDF Report")
            st.markdown("Generate a professional PDF containing your career prediction, skill analysis, roadmap progress, and XP.")
            if st.button("📄 Generate & Download PDF", key="btn_pdf", use_container_width=True):
                pdf_bytes = generate_pdf_report(stats, skills)
                if pdf_bytes:
                    st.download_button(
                        "⬇️ Download Report",
                        data=pdf_bytes,
                        file_name=f"skillforge_{stats['username']}_report.pdf",
                        mime="application/pdf",
                        use_container_width=True,
                    )
                    st.success("PDF generated successfully!")
                else:
                    st.warning("Install `fpdf2` to enable PDF export: `pip install fpdf2`")

            # CSV export
            st.markdown("---")
            st.markdown("##### 📊 Download Skill Data (CSV)")
            df_export = pd.DataFrame([{
                **{f"skill_{k.lower().replace(' ','_')}": v for k, v in skills.items()},
                "career": stats.get("career",""),
                "xp": stats["xp"],
                "level": stats["level"],
                "progress": stats.get("progress",0),
            }])
            csv_data = df_export.to_csv(index=False)
            st.download_button(
                "⬇️ Download Skill CSV",
                data=csv_data,
                file_name=f"skillforge_{stats['username']}_skills.csv",
                mime="text/csv",
                use_container_width=True,
            )
            st.markdown('</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────
# ENTRY POINT
# ──────────────────────────────────────────────────────────────
def main():
    init_db()
    inject_css()

    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    if not st.session_state["logged_in"]:
        render_auth()
        return

    username = st.session_state["username"]

    # Load or refresh stats
    if "stats" not in st.session_state:
        st.session_state["stats"] = load_stats(username)

    # Streak logic: increment if new day
    stats = st.session_state["stats"]
    today_str = date.today().isoformat()
    last_login = stats.get("last_login", "")[:10] if stats.get("last_login") else ""
    if last_login != today_str:
        if last_login == (date.today().replace(day=date.today().day - 1)).isoformat():
            stats["streak"] = stats.get("streak", 0) + 1
        elif last_login == "":
            stats["streak"] = 1
        # else streak broken - reset
        elif last_login < (date.today().replace(day=date.today().day - 1)).isoformat():
            stats["streak"] = 1
        stats["last_login"] = datetime.now().isoformat()
        save_stats(stats)
        st.session_state["stats"] = stats

    render_app(stats)


if __name__ == "__main__":
    main()