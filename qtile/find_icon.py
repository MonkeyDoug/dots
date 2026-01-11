import os
from xdg import DesktopEntry
from xdg import IconTheme
from xdg import BaseDirectory

def find_app_icon(app_name):
    icon_path = None

    # 1. Find the .desktop file
    # We search standard paths like /usr/share/applications and ~/.local/share/applications
    desktop_file = None
    for data_dir in BaseDirectory.xdg_data_dirs:
        possible_path = os.path.join(data_dir, "applications", f"{app_name}.desktop")
        if os.path.exists(possible_path):
            desktop_file = possible_path
            break
            
    if not desktop_file:
        print(f"Error: Could not find '{app_name}.desktop'")
        return None

    # 2. Extract the Icon name from the .desktop file
    entry = DesktopEntry.DesktopEntry(desktop_file)
    icon_name = entry.getIcon()
    
    if not icon_name:
        print("Error: No 'Icon' entry found in desktop file.")
        return None

    # 3. If the icon path is absolute (e.g. /opt/app/icon.png), return it immediately
    if os.path.isabs(icon_name):
        if os.path.exists(icon_name):
            return icon_name
        print("Error: Icon path in desktop file does not exist.")
        return None

    # 4. Resolve the icon name using the current theme
    # 'hicolor' is the default fallback theme mandated by freedesktop.org
    icon_path = IconTheme.getIconPath(icon_name, size=64, theme="hicolor")
    
    if not icon_path:
        print(f"Error: Could not find icon '{icon_name}' in system themes.")
    return icon_path

def main():
    name = input("Enter application name (app_id): ")
    icon = find_app_icon(name)
    print(icon)
    return

if __name__ == "__main__":
    main()
