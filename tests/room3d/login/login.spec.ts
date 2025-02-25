import { test, expect } from '@playwright/test';
import { LoginPage, LeftNavigationPanel, AccountPage, HeaderComponent } from '@POM';

test('User should be able to log in, update profile name, and save changes', async ({ page }) => {
  
  await test.step('Navigate to login page', async () => {
    await page.goto(`${process.env.BASE_URL}/login`, { waitUntil: 'networkidle' });
  });

  await test.step('Log in with valid credentials', async () => {
    const email = process.env.EMAIL;
    const password = process.env.PASSWORD;

    // Filling in the login form
    await LoginPage.email_field(page).fill(email);
    await LoginPage.password_field(page).fill(password);

    // Clicking the login button
    await LoginPage.login_button(page).click();
  });

  await test.step('Verify redirection to select-room page', async () => {
    // Since we don't have explicit visual checks in history.json,
    // we assume redirection is verified by checking the URL.
    await expect(page).toHaveURL(/\/select-room$/, { timeout: 5000 });
  });

  await test.step('Navigate to Account page', async () => {
    // Clicking on the account link in the left navigation panel
    await LeftNavigationPanel.leftNavPanel.account_link(page).click();
  });

  await test.step('Edit and save personal information', async () => {
    const newName = 'Playwright1234567';
    
    // Click edit button to enable editing personal information
    await AccountPage.editPersonalInfoComponent.edit_button(page).click();
    
    // Fill the name field with new name
    await AccountPage.editPersonalInfoComponent.edit_name_field(page).fill(newName);

    // Save the changes
    await AccountPage.editPersonalInfoComponent.save_button(page).click();

    await test.step('Ensure new name appears in header', async () => {
      const userName = HeaderComponent.user_name(page);
      await expect(userName).toContainText(newName);
    });
  });

});