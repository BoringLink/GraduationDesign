#!/bin/bash
# Run literature-search skill evals with proper environment setup

set -e

# Get the directory this script is in
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SKILL_DIR="$SCRIPT_DIR"

echo "=========================================="
echo "Literature Search Skill - Evaluation Suite"
echo "=========================================="
echo ""
echo "Skill Location: $SKILL_DIR"
echo ""

# Set up Python path
export PYTHONPATH="$SKILL_DIR/scripts:$PYTHONPATH"

# Set Semantic Scholar API key if provided
if [ -z "$SEMANTIC_SCHOLAR_KEY" ]; then
    echo "⚠️  SEMANTIC_SCHOLAR_KEY not set"
    echo "   Set it with: export SEMANTIC_SCHOLAR_KEY='your-key-here'"
    echo "   For now, using arXiv-only searches"
    echo ""
else
    echo "✓ SEMANTIC_SCHOLAR_KEY is set"
    echo ""
fi

# Create outputs directory
mkdir -p "$SKILL_DIR/outputs"

# Run tests
echo "Running evaluation tests..."
echo ""

cd "$SKILL_DIR/scripts"
python3 test_skill.py

echo ""
echo "✓ Evaluation complete!"
echo ""
echo "Results saved to: $SKILL_DIR/outputs/"
