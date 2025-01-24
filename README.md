# **Utkrishi: Revolutionizing Agricultural Commerce**  
![Utkrishi](https://img.shields.io/badge/version-0.1-blue) ![Django](https://img.shields.io/badge/server-Django-green) ![Kivy](https://img.shields.io/badge/frontend-Kivy-orange) ![License](https://img.shields.io/badge/license-MIT-purple)

Utkrishi is a platform designed to empower farmers and connect them directly with consumers by eliminating intermediaries. This ensures better profits for farmers and affordable prices for consumers. The project leverages **Django**, **Firebase**, and **Kivy** to deliver a scalable, secure, and user-friendly application.

---

## **Table of Contents**
1. [Screenshorts](#screenshorts)  
1. [About the Project](#about-the-project)  
2. [Key Features](#key-features)  
3. [Technologies Used](#technologies-used)  
4. [System Architecture](#system-architecture)  
5. [Installation](#installation)  
6. [Usage](#usage)  
7. [Contributing](#contributing)  
8. [License](#license)  
9. [Contact](#contact)

---

## **Screenshorts**
![Presplash Screen](screenshots/Presplash.jpg)

![Language Selection Screen](screenshots/Lang.jpg)

![Home Screen](screenshots/Presplash.jpg)

![Search Screen](screenshots/Search.jpg)

![Account Screen](screenshots/Account.jpg)

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
