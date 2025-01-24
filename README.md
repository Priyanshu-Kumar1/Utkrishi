# **Utkrishi: Revolutionizing Agricultural Commerce**  
![Utkrishi](https://img.shields.io/badge/version-0.1-blue) ![Django](https://img.shields.io/badge/server-Django-green) ![Kivy](https://img.shields.io/badge/frontend-Kivy-orange) ![License](https://img.shields.io/badge/license-MIT-purple)

Utkrishi is a platform designed to empower farmers and connect them directly with consumers by eliminating intermediaries. This ensures better profits for farmers and affordable prices for consumers. The project leverages **Django**, **Firebase**, and **Kivy** to deliver a scalable, secure, and user-friendly application.

---

## **Table of Contents**
1. [Screenshorts](#screenshorts)  
2. [About the Project](#about-the-project)  
3. [Key Features](#key-features)  
4. [Technologies Used](#technologies-used)  
5. [System Architecture](#system-architecture)  
6. [Installation](#installation)  
7. [Usage](#usage)  
8. [Contributing](#contributing)  
9. [License](#license)  
10. [Contact](#contact)

---

## **Screenshorts**
<img src="https://github.com/user-attachments/assets/d723ffd0-b421-4b75-922c-9b099e546bee" alt="Presplash" width="100" height="222.29">
<img src="https://github.com/user-attachments/assets/356e1a62-d08f-4399-a9e3-8858ff01182d" alt="Language Selection" width="100" height="222.29">
<img src="https://github.com/user-attachments/assets/1e36498b-be33-4ba3-87c9-1613f070dcfc" alt="Home" width="100" height="222.29">
<img src="https://github.com/user-attachments/assets/b83c469e-0b8b-46a5-878e-b6e737126078" alt="Search" width="100" height="222.29">
<img src="https://github.com/user-attachments/assets/3e605e30-abeb-46bf-8fb6-9c62a46a7e78" alt="Account" width="100" height="222.29">

## **About the Project**

Utkrishi aims to bridge the gap between farmers and consumers through a digital marketplace, enabling direct transactions without the need for middlemen.  
The project focuses on:
- Providing farmers with tools to list products easily using **voice-to-text** in their native language.
- Offering consumers access to fresh produce at competitive prices.
- Building a centralized server for data management and secure operations using **Django**.
- Real-time synchronization of data and notifications through **Firebase**.

---

## **Key Features**
- **Direct Farmer-to-Consumer Sales**: Eliminates intermediaries, improving profits for farmers.  
- **Multi-Language Support**: Farmers and consumers can interact with the platform in their preferred language.  
- **Voice-to-Text Functionality for Product Listing**: Simplifies product listing for farmers with limited literacy or typing skills.  
- **AI-Driven Recommendations**: Personalized product suggestions for consumers based on their behavior.  
- **Real-Time Notifications for Transactions**: Updates for buyers and sellers using Firebase Cloud Messaging (FCM).  
- **User-Friendly Interface on Mobile and Web**: Optimized design for ease of use.

---

## **Technologies Used**
| **Technology**      | **Purpose**                       |
|----------------------|-----------------------------------|
| **Kivy/KivyMD**      | Frontend for Mobile App           |
| **Django**           | Backend for Web and APIs         |
| **Firebase**         | Realtime Database & Notifications|
| **SQLite**           | Local database for offline mode  |
| **AI/NLP**           | Recommendations and Voice Input  |

---

## **System Architecture**
The **Utkrishi** platform has a modular architecture that supports scalability and real-time updates.  

- **Frontend**: Built using Kivy/KivyMD for the mobile application.  
- **Backend**: Django server manages business logic, authentication, and APIs.  
- **Database**: Firebase for real-time data, Firestore for storing user and product information.  
- **AI/NLP**: NLP processes voice commands, and AI provides product recommendations.

```
[USER INTERFACE] <--> [DJANGO SERVER] <--> [FIREBASE/AI MODULES]
```


---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/utkrishi.git
cd utkrishi
```

### **2. Backend Setup (Django)**
1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up Firebase credentials:
   - Download Firebase Admin SDK JSON and place it in the project directory.
   - Add the file path in Django settings.

3. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### **3. Mobile App Setup (Kivy)**
1. Install Kivy and KivyMD:
   ```bash
   pip install kivy kivymd
   ```
2. Run the mobile app:
   ```bash
   python main.py
   ```

---

## **Usage**

- **Farmers**:  
  - List products using voice-to-text functionality or manual input.  
  - Manage inventory and track sales.  
  - Get real-time notifications for purchases.  

- **Consumers**:  
  - Browse fresh produce, view personalized recommendations, and make purchases.  

- **Admin**:  
  - Manage user accounts and transactions via the centralized Django server.  

---

## **Contributing**
We welcome contributions from the community! 🚀  

### **Steps to Contribute:**
1. **Fork the Repository**  
2. **Create a New Branch**  
   ```bash
   git checkout -b feature-name
   ```
3. **Make Changes and Commit**  
   ```bash
   git commit -m "Add your message here"
   ```
4. **Push to Your Branch**  
   ```bash
   git push origin feature-name
   ```
5. **Create a Pull Request**

---

## **License**
This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## **Contact**

**Priyanshu Kumar**   
📧 [rprem058@gmail.com]  
🌐 [GitHub Profile](https://github.com/Priyanshu-Kumar1)
