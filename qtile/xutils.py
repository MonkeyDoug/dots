from Xlib import X, display, Xatom
from Xlib.protocol import request
from PIL import Image
import numpy as np

import sys

np.set_printoptions(threshold=sys.maxsize)


def find_window_by_name(d, window_name, root=None):
    """Recursively search for a window with the specified name."""
    if root is None:
        root = d.screen().root

    print(f"finding window of name {window_name}")
    children = root.query_tree().children
    for win in children:
        try:
            name = win.get_full_property(
                d.intern_atom("_NET_WM_NAME"), X.AnyPropertyType
            )
            if name and window_name == name.value.decode("utf-8"):
                return win
        except Exception:
            pass
        # Recursively search in child windows
        try:
            found = find_window_by_name(d, window_name, win)
            if found:
                return found
        except Exception:
            continue
    return None


def get_window_icon(d, window):
    """Retrieve the _NET_WM_ICON property and decode it into an image."""
    print("getting window icon")
    atom = d.intern_atom("_NET_WM_ICON")
    prop = window.get_full_property(atom, Xatom.CARDINAL)

    if not prop:
        raise ValueError("No _NET_WM_ICON property found for the window.")

    data = prop.value
    print(len(data))
    print(data[0], data[1])
    # with open("data.txt", "w") as f:
    #     f.write(str(data))

    # Parse the _NET_WM_ICON data
    icons = []
    i = 0
    while i < len(data):
        width = data[i]
        height = data[i + 1]
        if width == 0 or height == 0:
            break
        pixels = data[i + 2 : i + 2 + width * height]
        icons.append((width, height, pixels))
        i += 2 + width * height

    if not icons:
        raise ValueError("No icons found in the _NET_WM_ICON property.")

    # Choose the largest icon (arbitrarily)
    width, height, pixels = max(icons, key=lambda x: x[0] * x[1])

    # Convert to an image
    # print(np.array(pixels).reshape((height, width)))
    argb = np.array(pixels).reshape((height, width))
    image = Image.fromarray(argb, "RGBA")
    return image


def get_icon(window_name):
    d = display.Display()

    try:
        # Find the window by name
        window = find_window_by_name(d, window_name)
        if not window:
            raise ValueError(f"No window found with name containing: '{window_name}'")

        # Get and display the window icon
        icon_image = get_window_icon(d, window)
        return icon_image
    except Exception as e:
        print(f"Error: {e}")


def main():
    # Connect to the X server
    d = display.Display()
    window_name = input("Enter the window name: ")

    try:
        # Find the window by name
        window = find_window_by_name(d, window_name)
        if not window:
            raise ValueError(f"No window found with name containing: '{window_name}'")

        # Get and display the window icon
        icon_image = get_window_icon(d, window)
        icon_image.show()  # Display the icon
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
