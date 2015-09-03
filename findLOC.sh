echo "Python files: "
find . -name "*.py" -type f -exec cat {} + | wc -l

echo ""

echo "HTML files: "
find . -name "*.html" -type f -exec cat {} + | wc -l

echo ""

echo "CSS files: "
find . -name "*.css" -type f -exec cat {} + | wc -l

echo ""

echo "JS files: "
find . -name "*.js" -type f -exec cat {} + | wc -l

echo ""

echo "Text files: "
find . -name "*.txt" -type f -exec cat {} + | wc -l

echo ""

echo "Markdown files: "
find . -name "*.md" -type f -exec cat {} + | wc -l

echo ""

echo "===TOTAL==="
find . -name "*" -type f -exec cat {} + | wc -l


echo ""
echo ""
echo "******AL HABIBI******"
echo ""
echo ""
