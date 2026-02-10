MediPay Ecosystem 
A full-stack microservices platform for healthcare claim management and financial analytics.
📋 Project Overview
MediPay was developed to solve the complexity of healthcare claim processing by integrating high-performance backend services with a real-time data analytics engine. The system ensures high data integrity through automated auditing and provides stakeholders with actionable financial metrics.
🏗️ Architecture
The system follows a microservices-oriented architecture orchestrated by Docker Compose:
Frontend: Angular 16+ (SPA) with Nginx reverse proxy.
Transactional Service: Java 17 / Spring Boot 3 (Handling claims logic).
Analytics Engine: Python (Pandas/NumPy) for data aggregation and financial metrics.
Database: PostgreSQL (with custom Triggers & PL/pgSQL functions for auditing).
Infrastructure: AWS (EC2 for compute, RDS for managed database).
🚀 Key Technical Features
High-Integrity Auditing: Implemented database-level triggers to monitor the claims table, automatically populating an audit_log for every update/insert to ensure 100% traceability.
Dynamic Proxying: Configured Nginx as a gateway to manage historic proxying, allowing the application to resolve dynamic URLs across local, staging, and AWS environments.
Data Engineering: Developed a Python-based module that aggregates raw claim data to calculate real-time financial metrics, providing a predictive view of patient/provider statements.
Automated CI/CD: Established a GitHub Actions workflow (deploy.yml) that automates testing, containerization, and deployment to an Amazon Linux (t3) instance.
🛠️ Tech Stack
Layer	Technologies
Backend	Java, Spring Boot, Hibernate, JUnit 5
Data Science	Python, Pandas, NumPy, PyTest
Frontend	Angular, TypeScript, Karma/Jasmine, Nginx
Database	PostgreSQL (RDS), Stored Procedures, Triggers
DevOps	Docker, Docker Compose, GitHub Actions, AWS EC2
🧪 Testing Strategy
Backend: 100% service-layer coverage using JUnit 5.
Frontend: Unit testing with Karma/Jasmine, utilizing provideHttpClientTesting for robust API mocking.
Analytics: Integration testing of data frames using PyTest.  

📬 Contact
Brilliant Mashanda - Senior Java Developer
masebenza.bm@gmail.com
