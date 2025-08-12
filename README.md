🌍 **Earthquake Notification & SOS Alert System**
Author: Adarsha Aryal
AWS Serverless Project – Real-time earthquake monitoring & automated outbound voice alerts.

**Overview**
This project monitors real-time earthquake data from the European Seismological Agency API and automatically alerts registered users via Amazon Connect outbound voice calls if an earthquake occurs within their defined radius.

Users can register their details (name, email, next-of-kin phone number, location, radius) via a Leaflet-powered web frontend, which stores their information in Amazon DynamoDB.
An EC2 instance runs a WebSocket client that listens for earthquake events and triggers alerts through AWS Connect.

**Tech Stack**
Frontend:

HTML, CSS, JavaScript
Leaflet.js for interactive location selection
Hosted on AWS S3 (Static Website Hosting)

Backend Services:

AWS Lambda (user registration endpoint)
AWS API Gateway (exposes Lambda to frontend)
Amazon DynamoDB (stores subscriber info)
Amazon Connect (outbound voice calls)
AWS EC2 (WebSocket client for earthquake feed)

Data Source:
European Seismological Agency Standing Order WebSocket API

**Features**
User-defined radius: Alerts are triggered only if the earthquake falls within the chosen range.
Automated outbound voice calls using Amazon Connect.
Interactive map for location selection via Leaflet.
Serverless subscriber storage in DynamoDB.
Real-time monitoring via persistent WebSocket connection.
