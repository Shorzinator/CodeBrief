"""Tests for the Bundle Generator tool."""

from unittest.mock import patch

from contextcraft.tools import bundler


class TestBundlerHelperFunctions:
    """Test cases for the bundler helper functions."""

    @patch("contextcraft.tools.bundler.tree_generator")
    def test_generate_tree_content_success(self, mock_tree_generator, tmp_path):
        """Test successful tree content generation."""
        # Mock the tree generation function to return expected content
        mock_tree_generator.generate_and_output_tree.return_value = (
            "ContextCraft/\n├── file1.py\n└── file2.py"
        )

        result = bundler.generate_tree_content(tmp_path, [])

        assert "# Directory Tree" in result
        assert "ContextCraft/" in result
        assert "├── file1.py" in result
        assert "└── file2.py" in result

    @patch("contextcraft.tools.bundler.tree_generator")
    def test_generate_tree_content_error(self, mock_tree_generator, tmp_path):
        """Test tree content generation with error."""
        mock_tree_generator.generate_and_output_tree.side_effect = Exception(
            "Tree generation failed"
        )

        result = bundler.generate_tree_content(tmp_path, [])

        assert "# Directory Tree" in result
        assert "Error generating directory tree" in result
        assert "Tree generation failed" in result

    @patch("contextcraft.tools.bundler.git_provider")
    def test_generate_git_content_success(self, mock_git_provider, tmp_path):
        """Test successful Git content generation."""
        mock_git_provider.get_git_context.return_value = (
            "# Git Context\n\nMock git output"
        )

        result = bundler.generate_git_content(tmp_path)

        assert "# Git Context" in result
        assert "Mock git output" in result
        mock_git_provider.get_git_context.assert_called_once_with(
            project_root=tmp_path,
            diff_options=None,
            log_count=5,
            full_diff=False,
        )

    @patch("contextcraft.tools.bundler.git_provider")
    def test_generate_git_content_error(self, mock_git_provider, tmp_path):
        """Test Git content generation with error."""
        mock_git_provider.get_git_context.side_effect = Exception("Git error")

        result = bundler.generate_git_content(tmp_path)

        assert "# Git Context" in result
        assert "Error generating Git context" in result
        assert "Git error" in result

    @patch("contextcraft.tools.bundler.dependency_lister")
    def test_generate_deps_content_success(self, mock_dependency_lister, tmp_path):
        """Test successful dependency content generation."""
        # Mock the list_dependencies function to return expected content
        mock_dependency_lister.list_dependencies.return_value = (
            "# Project Dependencies\n\nMock dependencies"
        )

        result = bundler.generate_deps_content(tmp_path)

        assert "# Project Dependencies" in result
        assert "Mock dependencies" in result

    @patch("contextcraft.tools.bundler.dependency_lister")
    def test_generate_deps_content_error(self, mock_dependency_lister, tmp_path):
        """Test dependency content generation with error."""
        mock_dependency_lister.list_dependencies.side_effect = Exception("Deps error")

        result = bundler.generate_deps_content(tmp_path)

        assert "# Project Dependencies" in result
        assert "Error generating dependency list" in result
        assert "Deps error" in result


class TestCreateBundle:
    """Test cases for the create_bundle function."""

    @patch("contextcraft.tools.bundler.generate_tree_content")
    @patch("contextcraft.tools.bundler.generate_git_content")
    @patch("contextcraft.tools.bundler.generate_deps_content")
    @patch("contextcraft.tools.bundler.generate_flatten_content")
    @patch("contextcraft.tools.bundler.config_manager")
    def test_create_bundle_file_output(
        self,
        mock_config_manager,
        mock_flatten,
        mock_deps,
        mock_git,
        mock_tree,
        tmp_path,
    ):
        """Test bundle creation with file output."""
        # Mock config
        mock_config_manager.load_config.return_value = {}

        # Mock content generation
        mock_tree.return_value = "Mock tree content"
        mock_git.return_value = "# Git Context\n\nMock git content"
        mock_deps.return_value = "# Project Dependencies\n\nMock deps content"
        mock_flatten.return_value = "# Files: Project Root\n\nMock flatten content"

        output_file = tmp_path / "bundle.md"

        with patch("contextcraft.tools.bundler.console"):
            bundler.create_bundle(
                project_root=tmp_path,
                output_file_path=output_file,
                flatten_paths=[tmp_path],  # Explicitly provide flatten paths
            )

            # Verify file was created
            assert output_file.exists()
            content = output_file.read_text()

            # Verify content structure
            assert "# ContextCraft Bundle" in content
            assert "## Table of Contents" in content
            assert "## Directory Tree" in content
            assert "## Git Context" in content
            assert "## Project Dependencies" in content
            assert "Mock tree content" in content
            assert "Mock git content" in content
            assert "Mock deps content" in content
            assert "Mock flatten content" in content
