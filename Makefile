# Makefile

.PHONY: all frontend backend stop

all: frontend backend

frontend:
	@echo Starting frontend...
	powershell -Command "Start-Process cmd -ArgumentList '/k cd frontend && npm run dev'"

backend:
	@echo Starting backend...
	powershell -Command "Start-Process cmd -ArgumentList '/k cd backend && uvicorn app.main:app --reload --port 8000'"

stop:
	@echo Stopping all processes...
	taskkill /IM cmd.exe /F