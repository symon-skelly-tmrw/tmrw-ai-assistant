import type { Page } from '@playwright/test';

export class LoginPage {

  static room_logo(page: Page) {
    return page.locator('i').getByRole('img')
  }

  static sign_in_button(page: Page) {
    return page.getByRole('link', { name: 'Sign In' })
  }
  
  static log_in_to_room_header(page: Page) {
    return page.getByRole('heading', { name: 'Log in to Room' })
  }

  static email_field_header(page: Page) {
    return page.getByText('Email')
  }

  static email_field(page: Page) {
    return page.getByRole('textbox', { name: 'Enter your email...' })
  }

  static password_header(page: Page) {
    return page.getByText('Password', { exact: true })
  }

  static password_field(page: Page) {
    return page.getByRole('textbox', { name: 'Enter password...' })
  }

  static password_visibility_toggle(page: Page) {
    return page.locator('form').getByRole('img')
  }

  static forgot_my_password_link(page: Page) {
    return page.getByRole('link', { name: 'Forgot my password' })
  }

  static login_button(page: Page) {
    return page.getByRole('button', { name: 'Login' })
  }

  static login_container(page: Page) {
    return page.getByText('Log in to RoomLog in to your personal ROOMEmailPassword Forgot my password Login');
  }

  static error_text(page: Page) {
    return page.locator('.loginV3_formhasErrorSpan__u_V0i')
  }
}

export class ForgotPasswordPage {
  static header(page: Page) {
    return page.getByRole('heading', { name: 'Forgot password?' })
  }

  static sub_text(page: Page) {
    return page.locator('[class="forgotPasswordV3_subText__nJmh2"]');
  }

  static email_input(page: Page) {
    return page.getByRole('textbox', { name: 'Email address' })
  }

  static resend_email_button(page: Page) {
    return page.getByRole('button', { name: 'Resend email' })
  }

  static send_button(page: Page) {
    return page.getByRole('button', { name: 'Send', exact: true })
  }
}

export class LeftNavigationPanel {
    static leftNavPanel = {
        account_link(page: Page) {
          return page.locator('a[href="/settings/account"]');
        },
    
        rooms_link(page: Page) {
          return page.locator('a[href="/select-room"]');  
        },
    
        meet_link(page: Page) {
          return page.locator('a[href="/meet"]');  
        },
      };
}

export class HeaderComponent {
    static logo(page: Page) {
          return page.getByRole('navigation').getByRole('link');
      }

    static menu_button(page: Page) {
          return page.locator('button[aria-haspopup="menu"]');
      }

    static user_name(page: Page) {
          return page.locator('button[aria-haspopup="menu"] span.sc-c8c622f7-0');
      }
};


export class AccountPage {
    static account_header(page: Page) {
      return page.getByRole('heading', { name: 'Account' });
    }

    // These are the read-only locators that should be used to verify the user's personal information
    static personalInfoComponent = {
      personal_info_header(page: Page) {
        return page.getByRole('heading', { name: 'Personal information' }).first();
      },
  
      edit_personal_info_utton(page: Page) {
        return page.locator('form').filter({ hasText: 'Personal informationEdit your' }).getByRole('button');
      },
  
      profile_picture_label(page: Page) {
        return page.locator('form').filter({ hasText: 'Personal informationEdit your' }).locator('rect').first();
      },

      name_info(page: Page) {
        return page.locator('[class="infoBlock_blockItem__PdnC0 PersonalInfoTextBlock_InfoBlock__PkcHV"]', { hasText: 'Name'});
      },

      email_info(page: Page) {
        return page.locator('[class="infoBlock_blockItem__PdnC0 PersonalInfoTextBlock_InfoBlock__PkcHV"]', { hasText: 'Email'});
      }
    };

    // these are locators that are used to edit the user's personal information
    static editPersonalInfoComponent = {
        edit_button(page: Page) {
            return page.locator('form').filter({ hasText: 'Personal informationEdit your' }).getByRole('button')
        },

        edit_name_field(page: Page) {
            return page.getByRole('textbox', { name: 'Name' });
        },

        edit_email_field(page: Page) {
            return page.getByRole('textbox', { name: 'Email' });
        },

        save_button(page: Page) {
            return page.getByRole('button', { name: 'Save' })
        },

        cancel_button(page: Page) {
            return page.getByRole('button', { name: 'Cancel' })
        },
    }

    static editPasswordComponent = {
        edit_button(page: Page) {
            return page.locator('form').filter({ hasText: 'PasswordEditCurrent password' }).getByRole('button')
        },

        save_button(page: Page) {
            return page.getByRole('button', { name: 'Save' })
        },

        current_password_field(page: Page) {
            return page.getByRole('textbox', { name: 'Current password' });
        },

        current_password_visibility_toggle(page: Page) {
            return page.locator('form').filter({ hasText: 'PasswordCancelSaveCurrent' }).getByRole('img').first()
        },

        new_password_field(page: Page) {
            return page.getByRole('textbox', { name: 'New password', exact: true });
        },

        new_password_visibility_toggle(page: Page) {
            return page.locator('form').filter({ hasText: 'PasswordCancelSaveCurrent' }).getByRole('img').nth(1)
        },

        confirm_password_field(page: Page) {
            return page.getByRole('textbox', { name: 'Confirm new password' })
        },

        confirm_password_visibility_toggle(page: Page) {
            return page.locator('form').filter({ hasText: 'PasswordCancelSaveCurrent' }).getByRole('img').nth(2)
        }
    }

    static deleteAccountComponent = {
        delete_account_button(page: Page) {
            return page.getByRole('button', { name: 'Delete account' });
        },

        confirm_delete_button(page: Page) {
            return page.getByRole('button', { name: 'Continue' });
        },

        cancel_delete_button(page: Page) {
            return page.getByRole('button', { name: 'Cancel' });
        },

        delete_account_modal(page: Page) {
            return page.locator('.delete-account-modal');
        },

        reason_radio_button(page: Page, reason: string) {
            return page.locator(`input[value="${reason}"]`);
        },

        reason_label(page: Page, reason: string) {
            return page.locator(`label[for="${reason}"]`);
        }
    };
  }

