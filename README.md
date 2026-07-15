# Library Management System

A web-based **Library Management System** developed using **Python, Flask, SQLite, HTML, CSS, Bootstrap, and JavaScript**. The application simplifies library operations by enabling book management, issue and return processing, fine calculation, and report generation through a centralized role-based system.

## Project Overview

The Library Management System is designed to automate the daily activities of a library. It provides separate dashboards for **Librarians**, **Students**, and **Faculty members**, enabling efficient book management, issue and return processing, fine calculation, and report generation. The system reduces manual work while maintaining accurate library records.

## Features

### User Authentication

- Secure login system
- Role-based access
- Separate dashboards for Librarian, Student, and Faculty

### Book Management

- Add new books
- View available books
- Delete books
- Manage book details (Title, Author, ISBN, Category, Quantity)

### Book Issue

- Issue books to students and faculty
- Automatic issue date generation
- Automatic due date calculation
- Track issued books

### Book Return

- Return issued books
- Automatic return date update
- Automatic fine calculation
- Automatic status update

### Fine Management

- Calculate overdue fines
- View pending fines
- Mark fines as paid
- Generate fine reports

### Reports

- Total Books Report
- Issued Books Report
- Returned Books Report
- Fine Collection Report
- Dashboard Summary

## Technology Stack

- Python
- Flask
- SQLite
- HTML5
- CSS3
- Bootstrap 5
- JavaScript

## User Roles

### Librarian

- Manage books
- Issue books
- Return books
- Calculate fines
- View reports
- Maintain library records

### Student

- Login to the system
- View available books
- View issued books
- Check fine status

### Faculty

- Login to the system
- View available books
- View issued books
- Check fine details

## Project Workflow

```text
           User Login
                │
                ▼
      Role Authentication
                │
                ▼
      Librarian Dashboard
                │
      ┌─────────┼──────────┐
      ▼         ▼          ▼
 Book      Issue Books   Return Books
Management      │             │
      │         ▼             ▼
 Add/Delete  Update Issue   Fine
   Books       Records   Calculation
      │                       │
      └───────────┬───────────┘
                  ▼
          Reports Dashboard
                  │
                  ▼
Books • Issued • Returned • Fine Reports
```

## Future Enhancements

- Barcode & QR Code Integration
- Book Reservation System
- Email Notifications
- SMS Notifications
- PDF Report Export
- Password Encryption
- Online Fine Payment
- Cloud Database Integration
- Advanced Book Search

## Author

**G O Chandana**

Department of Computer Science and Engineering

SJB Institute of Technology, Bengaluru
