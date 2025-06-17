#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Running AI feature tests...${NC}"

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}pytest is not installed. Installing...${NC}"
    pip install pytest pytest-asyncio
fi

# Create test directory if it doesn't exist
TEST_DIR="tests"
if [ ! -d "$TEST_DIR" ]; then
    echo -e "${YELLOW}Creating test directory...${NC}"
    mkdir -p "$TEST_DIR"
fi

# Run tests
echo -e "${YELLOW}Running tests...${NC}"
python -m pytest tests/test_ai_features.py -v

# Check test results
if [ $? -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
else
    echo -e "${RED}Some tests failed. Please check the output above.${NC}"
    exit 1
fi

echo -e "${GREEN}Test run complete!${NC}" 