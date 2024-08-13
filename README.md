# ATS-app (Applicant Tracking System)
This is a Flask-based tool for evaluating resumes against job descriptions. It uses Groq LLM to extract and analyze relevant information from both PDFs, calculates match percentages based on cosine similarity, and displays detailed results. The app also features a dynamic waiting time display that shows real-time elapsed time from processing initiation to result display. Users can upload multiple resumes and a job description, which are processed to identify the best-fit candidates.

![ATS-Image](https://private-user-images.githubusercontent.com/123545481/357391663-103f008b-4693-4a01-9393-9179acac1353.png?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MjM1NDkyMTUsIm5iZiI6MTcyMzU0ODkxNSwicGF0aCI6Ii8xMjM1NDU0ODEvMzU3MzkxNjYzLTEwM2YwMDhiLTQ2OTMtNGEwMS05MzkzLTkxNzlhY2FjMTM1My5wbmc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQwODEzJTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MDgxM1QxMTM1MTVaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT1mMThmNmEyMDQ2ZTdmNWI1YTRjMmE3Nzc4YjJjODc0NTc4MjgwMTk3OWIxZGViMjk4MWQyZDI2NDMzNmFlZGVkJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZhY3Rvcl9pZD0wJmtleV9pZD0wJnJlcG9faWQ9MCJ9.IePHbonSBu5dszR6tkEkx_4St1vvPDVa-4g2ZrKv830)

## Docker 
This app can be used by leveraging docker. 

See overview of this repository for further details.

[Docker-ats-app](https://hub.docker.com/r/aryan018/ats-app)

