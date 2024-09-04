# Quick Level Selector Plugin

A simple **Python tool for Unreal Engine** that provides a quick level selection feature directly integrated into the editor's toolbar. This tool automatically lists available levels in your project, organizes them by their directory, and allows you to open any level with just a click.

![Quick Level Selector](path/to/your/gif/file.gif)

## Features
- **Automatic Level Detection:** The tool scans your project for available levels and organizes them into sections based on their directory structure.
- **Quick Access:** All levels are listed in a dropdown menu within the editor's toolbar for easy access.
- **Manual Refresh:** If you add or remove levels, use the **Refresh** button to update the list.

## How to Install

1. **Download the Plugin:**
    - Clone the repository or download the plugin as a ZIP file:
    ```bash
    git clone https://github.com/yourusername/QuickLevelSelector.git
    ```
    - If you download the ZIP file, extract it into your desired location.

2. **Add the Plugin to Your Project:**
    - Navigate to your Unreal Engine project's `Plugins` folder. If it doesn't exist, create it.
    - Copy the `QuickLevelSelector` folder from the repository into your project's `Plugins` directory.

3. **Enable the Plugin:**
    - Open your project in Unreal Engine.
    - Go to `Edit > Plugins` and find the `Quick Level Selector` plugin in the list.
    - Enable the plugin and restart the editor if prompted.

## How to Use

- Once the plugin is installed and enabled, you will see a new dropdown menu in the editor's toolbar.
- Click on the dropdown to see a list of available levels organized by their directory. Click on any level to open it.
- If you make changes to your levels (add or remove levels), click the **Refresh** button to update the list.

## Known Issues
- **Large Maps at Startup:** If the editor is still processing larger maps when first opened, some levels may be missed by the plugin. This is a known issue and a work in progress (WIP) for a future update.
- **Manual Refresh Required:** The plugin currently requires manual refreshing to detect changes in the level list. Automatic detection is also a WIP.

## Notes
- This tool is written in Python and is designed specifically for Unreal Engine users.
- If you encounter any issues, feel free to open an issue on the GitHub repository.

---

Feel free to contribute to this plugin by forking the repository and submitting a pull request!

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

