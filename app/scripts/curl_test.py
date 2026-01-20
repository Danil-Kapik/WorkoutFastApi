curl -H "Authorization: Bearer ${ACCESS_TOKEN}" http://localhost:8000/progress/




curl -X POST http://localhost:8000/sessions/create \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI4IiwiaWF0IjoxNzY4ODUyMTE5LCJleHAiOjE3Njg4NTU3MTl9.xwcvQv4k_omkSrlXS9ufgan5IQRpk6MjN2YFVr8zEVg" \
  -d '{
    "exercise_type": "подтягивания",
    "reps": 4
  }'
