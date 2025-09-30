#!/bin/bash

# Quick test script for the backend API

echo "🧪 Testing Research Intelligence Platform Backend API"
echo ""

BASE_URL="http://localhost:8000"

# Test 1: Health Check
echo "1️⃣ Testing health check..."
curl -s "$BASE_URL/health" | python -m json.tool
echo ""

# Test 2: Fetch Bios
echo "2️⃣ Testing bios endpoint..."
curl -s -X POST "$BASE_URL/bios" \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Harvard University",
    "role_title": "Chief Financial Officer"
  }' | python -m json.tool | head -n 30
echo "... (truncated)"
echo ""

# Test 3: Fetch Jobs
echo "3️⃣ Testing jobs endpoint..."
curl -s -X POST "$BASE_URL/jobs" \
  -H "Content-Type: application/json" \
  -d '{
    "role_title": "Chief Financial Officer",
    "search_type": "Executive"
  }' | python -m json.tool | head -n 30
echo "... (truncated)"
echo ""

# Test 4: Fetch News
echo "4️⃣ Testing news endpoint..."
curl -s -X POST "$BASE_URL/news" \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Harvard University"
  }' | python -m json.tool | head -n 30
echo "... (truncated)"
echo ""

# Test 5: Trigger Workflow
echo "5️⃣ Testing workflow trigger..."
TRIGGER_RESPONSE=$(curl -s -X POST "$BASE_URL/trigger" \
  -H "Content-Type: application/json" \
  -d '{
    "org_name": "Harvard University",
    "role_title": "Chief Financial Officer",
    "search_type": "Executive"
  }')
echo "$TRIGGER_RESPONSE" | python -m json.tool
RUN_ID=$(echo "$TRIGGER_RESPONSE" | python -c "import sys, json; print(json.load(sys.stdin)['run_id'])")
echo ""

# Test 6: Check Status
echo "6️⃣ Testing status endpoint (waiting 5 seconds)..."
sleep 5
curl -s "$BASE_URL/status/$RUN_ID" | python -m json.tool
echo ""

echo "✅ All tests completed!"
echo ""
echo "📖 For full API documentation, visit: $BASE_URL/docs"
