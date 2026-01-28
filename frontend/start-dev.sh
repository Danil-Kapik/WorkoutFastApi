#!/bin/bash

# Quick start script for the frontend

cd "$(dirname "$0")"

echo "Starting Workout Tracker Frontend..."
echo ""
echo "Available commands:"
echo "  npm run dev      - Start development server (http://localhost:5173)"
echo "  npm run build    - Build for production"
echo "  npm run preview  - Preview production build"
echo ""
echo "Ensure backend is running on http://localhost:8000"
echo ""

npm run dev
