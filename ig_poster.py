#
# IG_POSTER.PY
#



###########################################
# n the assignment of the next_button2_region variable, the tuple (800, 800, 300, 200) defines the region in which pyautogui will search for the next_button2 image. The arguments in the tuple are responsible for the following points:
#
# Left (x-coordinate): The first value (800) represents the x-coordinate of the top-left corner of the region.
# Top (y-coordinate): The second value (800) represents the y-coordinate of the top-left corner of the region.
# Width: The third value (300) represents the width of the region, extending to the right from the left x-coordinate.
# Height: The fourth value (200) represents the height of the region, extending downwards from the top y-coordinate.
# So, the region is defined by starting at the point (800, 800) and extending 300 pixels to the right and 200 pixels downward.
#
###########################################



import pyautogui
import time
import os
from ai_news_config import UPCOMING_POSTS_PATH_LONG

def auto_post(folder):
    image_path = os.path.join(folder, "picture_0.png")
    caption_path = os.path.join(folder, "caption_0.txt")

    # Check if image and caption files exist
    if not os.path.exists(image_path):
        print(f"Image not found: {image_path}")
        return
    if not os.path.exists(caption_path):
        print(f"Caption not found: {caption_path}")
        return

    with open(caption_path, 'r') as file:
        caption = file.read()

    # Open Chrome and navigate to Instagram
    os.system("google-chrome https://www.instagram.com")
    time.sleep(7)  # Increased sleep time to ensure the page loads completely

    # Locate the create post button
    create_button_path = 'pyautogui_images/create_ig_post.png'
    print(f"Looking for create post button image at: {create_button_path}")
    create_button = pyautogui.locateOnScreen(create_button_path, confidence=0.8)
    if create_button is None:
        print(f"Create post button image not found: {create_button_path}")
        return
    pyautogui.click(create_button)
    time.sleep(4)  # Increased sleep time

    # Locate the add photo button
    add_photo_button_path = 'pyautogui_images/add_photo.png'
    print(f"Looking for add photo button image at: {add_photo_button_path}")
    add_photo = pyautogui.locateOnScreen(add_photo_button_path, confidence=0.8)
    if add_photo is None:
        print(f"Add photo button image not found: {add_photo_button_path}")
        return
    pyautogui.click(add_photo)
    time.sleep(4)  # Increased sleep time

    # Click on "Desktop"
    desktop_button_path = 'pyautogui_images/desktop_button.png'
    print(f"Looking for Desktop button image at: {desktop_button_path}")
    desktop_button = pyautogui.locateOnScreen(desktop_button_path, confidence=0.8)
    if desktop_button is None:
        print(f"Desktop button image not found: {desktop_button_path}")
        return
    pyautogui.click(desktop_button)
    time.sleep(2)  # Increased sleep time

    # Click on "daily_scripts"
    daily_scripts_button_path = 'pyautogui_images/daily_scripts_button.png'
    print(f"Looking for daily_scripts button image at: {daily_scripts_button_path}")
    daily_scripts_button = pyautogui.locateOnScreen(daily_scripts_button_path, confidence=0.8)
    if daily_scripts_button is None:
        print(f"daily_scripts button image not found: {daily_scripts_button_path}")
        return
    pyautogui.click(daily_scripts_button)
    time.sleep(2)  # Increased sleep time

    # Click on "open"
    open_button_path = 'pyautogui_images/open_button.png'
    print(f"Looking for open button image at: {open_button_path}")
    open_button = pyautogui.locateOnScreen(open_button_path, confidence=0.8)
    if open_button is None:
        print(f"Open button image not found: {open_button_path}")
        return
    pyautogui.click(open_button)
    time.sleep(2)  # Increased sleep time

    # Click on "youtube_video_insights"
    youtube_video_insights_button_path = 'pyautogui_images/youtube_video_insights_button.png'
    print(f"Looking for youtube_video_insights button image at: {youtube_video_insights_button_path}")
    youtube_video_insights_button = pyautogui.locateOnScreen(youtube_video_insights_button_path, confidence=0.8)
    if youtube_video_insights_button is None:
        print(f"youtube_video_insights button image not found: {youtube_video_insights_button_path}")
        return
    pyautogui.click(youtube_video_insights_button)
    time.sleep(2)  # Increased sleep time

    # Click on "open"
    open_button_path = 'pyautogui_images/open_button.png'
    print(f"Looking for open button image at: {open_button_path}")
    open_button = pyautogui.locateOnScreen(open_button_path, confidence=0.8)
    if open_button is None:
        print(f"Open button image not found: {open_button_path}")
        return
    pyautogui.click(open_button)
    time.sleep(2)  # Increased sleep time

    # Click on "instagram_creatives"
    instagram_creatives_button_path = 'pyautogui_images/instagram_creatives_button.png'
    print(f"Looking for instagram_creatives button image at: {instagram_creatives_button_path}")
    instagram_creatives_button = pyautogui.locateOnScreen(instagram_creatives_button_path, confidence=0.8)
    if instagram_creatives_button is None:
        print(f"instagram_creatives button image not found: {instagram_creatives_button_path}")
        return
    pyautogui.click(instagram_creatives_button)
    time.sleep(2)  # Increased sleep time

    # Click on "open"
    open_button_path = 'pyautogui_images/open_button.png'
    print(f"Looking for open button image at: {open_button_path}")
    open_button = pyautogui.locateOnScreen(open_button_path, confidence=0.8)
    if open_button is None:
        print(f"Open button image not found: {open_button_path}")
        return
    pyautogui.click(open_button)
    time.sleep(2)  # Increased sleep time

    # Click on "upcoming_posts"
    upcoming_posts_button_path = 'pyautogui_images/upcoming_posts_button.png'
    print(f"Looking for upcoming_posts button image at: {upcoming_posts_button_path}")
    upcoming_posts_button = pyautogui.locateOnScreen(upcoming_posts_button_path, confidence=0.8)
    if upcoming_posts_button is None:
        print(f"upcoming_posts button image not found: {upcoming_posts_button_path}")
        return
    pyautogui.click(upcoming_posts_button)
    time.sleep(2)  # Increased sleep time

    # Click on "open"
    open_button_path = 'pyautogui_images/open_button.png'
    print(f"Looking for open button image at: {open_button_path}")
    open_button = pyautogui.locateOnScreen(open_button_path, confidence=0.8)
    if open_button is None:
        print(f"Open button image not found: {open_button_path}")
        return
    pyautogui.click(open_button)
    time.sleep(2)  # Increased sleep time

    # Click on "picture_0.png"
    picture_0_button_path = 'pyautogui_images/picture_0_button.png'
    print(f"Looking for picture_0_button.png image at: {picture_0_button_path}")
    picture_0_button = pyautogui.locateOnScreen(picture_0_button_path, confidence=0.8)
    if picture_0_button is None:
        print(f"picture_0_button image not found: {picture_0_button}")
        return
    pyautogui.click(picture_0_button)
    time.sleep(2)  # Increased sleep time

    # Click on "open"
    open_button_path = 'pyautogui_images/open_button.png'
    print(f"Looking for open button image at: {open_button_path}")
    open_button = pyautogui.locateOnScreen(open_button_path, confidence=0.8)
    if open_button is None:
        print(f"Open button image not found: {open_button_path}")
        return
    pyautogui.click(open_button)
    time.sleep(2)  # Increased sleep time

    # Proceed with the next steps
    next_button2_path = 'pyautogui_images/next_button2.png'
    print(f"Looking for next button 2 image at: {next_button2_path}")
    next_button2 = pyautogui.locateOnScreen(next_button2_path, confidence=0.8)
    if next_button2 is None:
        print(f"Next button image not found: {next_button2_path}")
        return
    pyautogui.click(next_button2)
    time.sleep(2)  # Increased sleep time
    
    # Proceed with the next steps
    next_button2_path = 'pyautogui_images/next_button2.png'
    print(f"Looking for next button 2 image at: {next_button2_path}")
    next_button2 = pyautogui.locateOnScreen(next_button2_path, confidence=0.8)
    if next_button2 is None:
        print(f"Next button image not found: {next_button2_path}")
        return
    pyautogui.click(next_button2)
    time.sleep(2)  # Increased sleep time

    # Paste the caption
    caption_space_path = 'pyautogui_images/caption_space.png'
    print(f"Looking for caption space image at: {caption_space_path}")
    caption_space = pyautogui.locateOnScreen(caption_space_path, confidence=0.8)
    if caption_space is None:
        print(f"Caption space image not found: {caption_space_path}")
        return
    pyautogui.click(caption_space)
    pyautogui.write(caption)
    time.sleep(3)  # Increased sleep time

    # Share the post
    share_button_path = 'pyautogui_images/share_button.png'
    print(f"Looking for share button image at: {share_button_path}")
    share_button = pyautogui.locateOnScreen(share_button_path, confidence=0.8)
    if share_button is None:
        print(f"Share button image not found: {share_button_path}")
        return
    pyautogui.click(share_button)
    time.sleep(4)  # Increased sleep time

    # Minimize Chrome
    pyautogui.hotkey('ctrl', 'super', 'down')

# Example usage:
def main():
    # Replace with actual folder paths generated by your previous script
    folders = [
        UPCOMING_POSTS_PATH_LONG
    ]

    for folder in folders:
        auto_post(folder)

if __name__ == "__main__":
    main()