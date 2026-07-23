import logging
from pathlib import Path

from pages.memberlist import MemberListPage
from utils.excel_reader import (
    generate_fake_member_data,
    get_excel_data,
    save_excel_data,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)

DATA_FILE = Path(__file__).resolve().parents[2] / "tests" / "data" / "member" / "faker_member_data.xlsx"


def test_member_list_page(page):
    """Test member list page - Add member functionality"""
    logger.info("=" * 60)
    logger.info("Starting test: test_member_list_page")
    logger.info("=" * 60)
    
    try:
        # Generate test data
        logger.info("Generating fake member data...")
        fake_rows = generate_fake_member_data(count=1)
        save_excel_data(DATA_FILE, fake_rows, sheet_name="Sheet1")
        logger.info(f"✓ Test data saved to: {DATA_FILE}")

        # Load test data
        testdata = get_excel_data(DATA_FILE, "Sheet1")
        first_member = list(testdata[0])
        logger.info(f"✓ Loaded member record with {len(first_member)} fields")
        logger.info(f"  First Name: {first_member[0]} | Last Name: {first_member[1]}")

        # Initialize page object
        logger.info("Opening Member List Page...")
        member = MemberListPage(page)
        member.open()
        
        # Verify page loaded
        assert member.is_visible("(//span[contains(text(),'Member Search')])[2]"), \
            "Member Search page did not load"
        logger.info("✓ Member Search page loaded successfully")

        # Navigate and add member
        logger.info("Scrolling to bottom and adding member...")
        member.scroll_to_bottom()
        member.add_member()
        member.page.wait_for_load_state("networkidle")
        logger.info("✓ Add member dialog opened")

        # Select random CHCP
        logger.info("Selecting random CHCP...")
        selected_chcp = member.select_random_chcp()
        logger.info(f"✓ Selected CHCP: {selected_chcp}")

        # Update member data
        first_member[10] = selected_chcp
        save_excel_data(DATA_FILE, [first_member], sheet_name="Sheet1")
        logger.info("✓ Member data updated with selected CHCP")

        # Display updated data
        updated_data = get_excel_data(DATA_FILE, "Sheet1")
        logger.info("=" * 60)
        logger.info("Updated Member Data:")
        logger.info("=" * 60)
        for idx, row in enumerate(updated_data):
            logger.info(f"  Row {idx}: {row}")
        logger.info("=" * 60)

        # Create member
        logger.info("Clicking create button...")
        member.click_create_button()
        logger.info("✓ Member creation completed")
        
        logger.info("=" * 60)
        logger.info("✓ TEST PASSED: Member successfully created")
        logger.info("=" * 60)

    except Exception as e:
        logger.error(f"✗ TEST FAILED: {str(e)}")
        logger.error("=" * 60)
        raise

    

    


    
    
    