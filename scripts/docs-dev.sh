#!/bin/bash
# scripts/docs-dev.sh
# Helper script for local documentation development

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Poetry is installed
check_poetry() {
    if ! command -v poetry &> /dev/null; then
        print_error "Poetry is not installed. Please install Poetry first."
        exit 1
    fi
}

# Function to install documentation dependencies
install_deps() {
    print_status "Installing documentation dependencies..."
    poetry install --with docs
    print_success "Dependencies installed successfully"
}

# Function to validate configuration
validate_config() {
    print_status "Validating MkDocs configuration..."
    # Test build without publishing to validate configuration
    poetry run mkdocs build --clean --strict --quiet
    print_success "Configuration is valid"
}

# Function to build documentation
build_docs() {
    print_status "Building documentation..."
    poetry run mkdocs build --clean --strict --verbose

    if [ -d "site" ] && [ -f "site/index.html" ]; then
        print_success "Documentation built successfully"
        print_status "Site size: $(du -sh site | cut -f1)"
        print_status "Total files: $(find site -type f | wc -l)"
    else
        print_error "Build failed - site directory or index.html not found"
        exit 1
    fi
}

# Function to serve documentation locally
serve_docs() {
    print_status "Starting local documentation server..."
    print_status "Documentation will be available at: http://127.0.0.1:8000"
    print_warning "Press Ctrl+C to stop the server"
    poetry run mkdocs serve
}

# Function to clean build artifacts
clean() {
    print_status "Cleaning build artifacts..."
    rm -rf site/
    rm -rf .mkdocs_cache/
    print_success "Cleaned build artifacts"
}

# Function to run full test
test_docs() {
    print_status "Running full documentation test..."

    validate_config
    build_docs

    # Check for LED effects
    if grep -q "led-text" site/stylesheets/extra.css; then
        print_success "LED effects CSS found"
    else
        print_warning "LED effects CSS not found"
    fi

    if grep -q "initLEDEffects" site/javascripts/extra.js; then
        print_success "LED effects JavaScript found"
    else
        print_warning "LED effects JavaScript not found"
    fi

    # Check critical pages
    critical_pages=(
        "site/index.html"
        "site/getting-started/installation/index.html"
        "site/user-guide/cli-commands/index.html"
        "site/reference/main/index.html"
    )

    for page in "${critical_pages[@]}"; do
        if [ -f "$page" ]; then
            print_success "Found: $page"
        else
            print_error "Missing: $page"
            exit 1
        fi
    done

    print_success "All documentation tests passed!"
}

# Function to show help
show_help() {
    echo "ContextCraft Documentation Development Helper"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  install     Install documentation dependencies"
    echo "  validate    Validate MkDocs configuration"
    echo "  build       Build documentation"
    echo "  serve       Start local development server"
    echo "  test        Run full documentation test"
    echo "  clean       Clean build artifacts"
    echo "  help        Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 serve    # Start development server"
    echo "  $0 test     # Run full test suite"
    echo "  $0 build    # Build documentation"
}

# Main script logic
main() {
    # Check if Poetry is available
    check_poetry

    # Parse command line arguments
    case "${1:-help}" in
        "install")
            install_deps
            ;;
        "validate")
            validate_config
            ;;
        "build")
            build_docs
            ;;
        "serve")
            serve_docs
            ;;
        "test")
            test_docs
            ;;
        "clean")
            clean
            ;;
        "help"|"--help"|"-h")
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
