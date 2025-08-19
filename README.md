# 🌍 Earthquake Notification & SOS Alert System

<img width="5142" height="2813" alt="Blank diagram (1)" src="https://github.com/user-attachments/assets/1c66f37f-4fd3-430a-a77a-7a7e14ef545d" />

This is a serverless project that provides real-time earthquake monitoring and automated voice alerts using AWS services.

## Overview

The **Earthquake Notification & SOS Alert System** monitors real-time earthquake data from the European Seismological Agency API. If an earthquake occurs within a user's defined radius, the system automatically triggers an outbound voice call to alert their nominated contact.

Users can register their details—including their name, location, and the desired alert radius—through a web frontend powered by **Leaflet.js**. This information is securely stored in an **Amazon DynamoDB** database. A dedicated **AWS EC2** instance runs a WebSocket client that listens for earthquake events and initiates alerts via **Amazon Connect** or **Twilio**.

## Key Features

* **User-Defined Radius**: Alerts are triggered only when an earthquake falls within a user's specified range.
* **Automated Voice Calls**: Uses Amazon Connect or Twilio for automated, outbound voice notifications.
* **Interactive Map**: An intuitive, interactive map built with Leaflet.js simplifies location selection.
* **Serverless Subscriber Storage**: User data is stored efficiently and scalably in DynamoDB.
* **Real-Time Monitoring**: A persistent WebSocket connection ensures the system is always monitoring for the latest earthquake events.

## Tech Stack

### Frontend
* **HTML, CSS, JavaScript**
* **Leaflet.js** for interactive map functionality
* Hosted on **AWS S3** for static website hosting

### Backend
* **AWS Lambda**: Handles the user registration endpoint.
* **AWS API Gateway**: Exposes the Lambda function to the web frontend.
* **Amazon DynamoDB**: Stores all subscriber information.
* **Amazon Connect / Twilio**: Used for sending automated outbound voice calls.
* **AWS EC2**: Hosts the WebSocket client that processes the earthquake feed.

### Data Source
* European Seismological Agency Standing Order WebSocket API



