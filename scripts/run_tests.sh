#!/bin/bash
set -e

KEEP_HISTORY=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --keep-history)
            KEEP_HISTORY=true
            shift
            ;;
        *)
            shift
            ;;
    esac
done

rm -rf allure-results/
mkdir -p allure-results

if [ "$KEEP_HISTORY" = true ] && [ -d "allure-report/history" ]; then
    echo "📚 Preserving history..."
    cp -r allure-report/history allure-results/
fi

echo "🚀 Running tests..."
uv run pytest --alluredir=allure-results -v

echo ""
echo "📁 Results: $(ls allure-results/*.json 2>/dev/null | wc -l) test result files"

echo ""
echo "✅ Done! Choose how to view:"
echo ""
echo "   Quick view (temporary server):"
echo "      uv run allure serve allure-results"
echo ""
echo "   Generate static HTML report:"
echo "      uv run allure generate allure-results -o allure-report --clean"
echo "      Then open: allure-report/index.html"
echo "      Or serve:  uv run allure serve allure-report"
