from playwright.sync_api import sync_playwright
import time
import sys

def run():
    print("Starting Playwright verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        try:
            # 1. Navigate to Home
            print("Navigating to home...")
            page.goto("http://127.0.0.1:5000")

            # 2. Add a Job
            print("Adding a job...")
            page.fill("#url", "http://test-delete.com")
            page.fill("#selector", "h1")
            page.fill("#interval", "10")
            page.click("button:has-text('Add Job')")

            # Wait for reload
            page.wait_for_load_state("networkidle")

            # 3. Verify Job in List
            print("Verifying job in list...")
            if not page.is_visible("text=http://test-delete.com"):
                print("Job URL not found in list")
                sys.exit(1)

            # Take screenshot of index page with job
            page.screenshot(path="frontend_verification/index_page.png")
            print("Screenshot saved to frontend_verification/index_page.png")

            # 6. Delete Job (handle confirm dialog)
            print("Deleting job...")
            # We need to set up the dialog handler BEFORE the action that triggers it
            page.once("dialog", lambda dialog: dialog.accept())

            # We need to make sure we are clicking the delete button for the specific job we just added
            # Finding the row that contains the text, then the delete button within it
            # Using xpath or just assuming it's the last one if we just added it?
            # Safer to find the row.

            # This selector finds the row (tr) containing the text, then finds the button with text "Delete" inside it.
            page.locator("tr:has-text('http://test-delete.com')").locator("button:has-text('Delete')").click()

            page.wait_for_load_state("networkidle")

            # 7. Verify Job Deleted
            print("Verifying deletion...")
            if page.is_visible("text=http://test-delete.com"):
                print("Job still visible after deletion")
                page.screenshot(path="frontend_verification/failed_delete.png")
                sys.exit(1)

            print("Verification successful!")

        except Exception as e:
            print(f"Error during verification: {e}")
            page.screenshot(path="frontend_verification/error_state.png")
            raise
        finally:
            browser.close()

if __name__ == "__main__":
    run()
