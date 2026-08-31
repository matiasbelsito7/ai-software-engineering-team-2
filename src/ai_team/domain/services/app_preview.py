"""
App preview service.

Generates a preview HTML from the output files of a generated application.
"""

from __future__ import annotations


class AppPreview:
    """
    Generates a single-file HTML preview from generated application files.
    """

    @staticmethod
    def generate(
        files: dict[str, str],
        app_name: str = "Generated App",
    ) -> str:
        """
        Combine output files into a single preview HTML.

        Args:
            files: Mapping of file paths to their content.
            app_name: Name of the application for the preview title.

        Returns:
            A complete HTML string that displays the app preview.
        """

        html_content = files.get("index.html", "")
        css_content = files.get("styles.css", "")
        js_content = files.get("app.js", "")

        if not html_content:
            html_content = AppPreview._build_default_html(files, app_name)

        if css_content and "<style>" not in html_content:
            html_content = html_content.replace(
                "</head>",
                f"<style>{css_content}</style>\n</head>",
            )

        if js_content and "<script>" not in html_content:
            html_content = html_content.replace(
                "</body>",
                f"<script>{js_content}</script>\n</body>",
            )

        return html_content

    @staticmethod
    def _build_default_html(
        files: dict[str, str],
        app_name: str,
    ) -> str:
        """
        Build a default HTML preview when no index.html exists.
        """

        file_list_items = "\n".join(
            f"<li><code>{path}</code> ({len(content)} bytes)</li>"
            for path, content in sorted(files.items())
        )

        return (
            "<!DOCTYPE html>\n"
            "<html lang='en'>\n"
            "<head>\n"
            f"<title>{app_name} - Preview</title>\n"
            "<meta charset='UTF-8'>\n"
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n"
            "<style>\n"
            "  body { font-family: system-ui, sans-serif; max-width: 800px;\n"
            "         margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }\n"
            "  h1 { border-bottom: 2px solid #e5e7eb; padding-bottom: 0.5rem; }\n"
            "  ul { line-height: 1.8; }\n"
            "  code { background: #f3f4f6; padding: 2px 6px; border-radius: 4px; }\n"
            "  .note { background: #fef3c7; border: 1px solid #f59e0b;\n"
            "          padding: 1rem; border-radius: 8px; margin-top: 1rem; }\n"
            "</style>\n"
            "</head>\n"
            "<body>\n"
            f"<h1>{app_name}</h1>\n"
            "<p>Generated application preview.</p>\n"
            "<h2>Generated Files</h2>\n"
            f"<ul>\n{file_list_items}\n</ul>\n"
            "<div class='note'>\n"
            "<strong>Note:</strong> This is a static preview. "
            "Download the full project to run it locally.\n"
            "</div>\n"
            "</body>\n"
            "</html>"
        )
