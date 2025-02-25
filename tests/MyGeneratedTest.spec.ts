import { test, expect } from '@playwright/test';
import { HeaderComponent, LeftNavigationPanel, AccountPage } from '@POM';

test('Update user profile name', async ({ page }) => {
  
  await test.step('Navigate to the Roommate app', async () => {
    await page.goto(`${process.env.BASE_URL}/`, { waitUntil: 'networkidle' });
  });

  await test.step('Open the select-room page', async () => {
    await page.goto(`${process.env.BASE_URL}/select-room`, { waitUntil: 'networkidle' });
  });

  await test.step('Navigate to the Account page via navigation panel', async () => {
    await LeftNavigationPanel.leftNavPanel.account_link(page).click();
    await expect(page.url()).toContain('/settings/account');
  });

  await test.step('Initiate edit of personal information', async () => {
    await AccountPage.editPersonalInfoComponent.edit_button(page).click();
  });

  await test.step('Input new profile name "New Name" and save changes', async () => {
    await AccountPage.editPersonalInfoComponent.edit_name_field(page).fill('New Name');
    await AccountPage.editPersonalInfoComponent.save_button(page).click();
  });

  await test.step('Validate that the new name is reflected on the account page', async () => {
    const nameInfo = AccountPage.personalInfoComponent.name_info(page);
    await expect(nameInfo).toContainText('New Name');
  });

  await test.step('Verify if confirmation message is shown', async () => {
    const confirmationMessage = page.locator('text=Name updated successfully');
    await expect(confirmationMessage).toBeVisible();
  });

  await test.step('Ensure new name appears in header', async () => {
    const userName = HeaderComponent.header.user_name(page);
    await expect(userName).toContainText('New Name');
  });

});