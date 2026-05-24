# Prototype Brief: Goal-Setting Activation — FinWise

---

## 0. TL;DR

FinWise has a massive activation bottleneck: only 19% of accounts create a savings goal, yet goal-setters retain at 14% churn vs. 37% for non-setters (2.6x difference). We're testing whether showing a non-dismissible goal-setting prompt on day 1 (after account linking), repeating it on day 3–4 if dismissed, and following up with an email on day 5 will increase goal creation rate from 19% to 28–30%. The prototype demonstrates these three touchpoints and what customers experience when they interact with each.

---

## 1. What We're Testing

**We believe that prompting users to create a goal immediately after linking their first account (day 1), repeating if dismissed (day 3–4), and sending a reassuring email if no goal is created (day 5), will increase goal-setter rate from 18.9% to 28–30% within 30 days.**

This hypothesis tests whether the problem is **discovery** (users don't know goals exist) vs. **rejection** (users see goals but don't want them). If users interact with the day 1 prompt and either create a goal or dismiss it, that's evidence of discovery being the barrier. If most users dismiss repeatedly and never create a goal, the problem is deeper (value clarity, or goals aren't the right feature for these users).

---

## 2. What the Prototype Must Show

1. **Day 1 Goal-Setting Modal (Immediate Post-Account-Linking)**
   - User just linked their first bank account; they tap back to the dashboard
   - Non-dismissible modal appears with headline "Set your first goal"
   - Subheading: "Users who set a goal are 2.6x more likely to stay on track with their finances."
   - Four buttons: [Emergency Fund] [Vacation Fund] [Debt Payoff] [Custom Goal]
   - [Maybe Later] option at the bottom
   - If user taps a template, goal appears on dashboard immediately; modal closes
   - If user taps [Maybe Later], modal closes (nothing created)

2. **Day 3–4 Re-Prompt (Same Modal, Second Appearance)**
   - User opens app on day 3 or later (after dismissing day 1 prompt)
   - Identical modal appears again
   - Demonstrate that it's the same affordance, tested again
   - Show that dismissing this one also closes it (no more re-prompts)

3. **Email: Day 5 Goal-Setting Nudge (Static mockup or clickable)**
   - Email appears in inbox on day 5 (or mockup of email in customer's inbox)
   - Subject: "The #1 thing successful FinWise users do"
   - Body: "Users who set goals within the first week report feeling 78% more secure about their finances 3 weeks later. It takes just 30 seconds; we'll help you every step of the way."
   - Primary CTA: [Set Your First Goal] button (clickable, if interactive prototype)
   - If clicked, links to goal-creation page (same templates as modal, but accessed via email link)
   - Shows reassurance messaging: "We're here to help every step of the way"

4. **Goal Creation (Happy Path)**
   - User taps [Emergency Fund] on day 1 modal
   - Goal appears on dashboard with name "Emergency Fund"
   - Affordance to edit the goal is visible (edit button or icon)
   - Dashboard shows the goal alongside transactions (context for how goal relates to spending)

---

## 3. What the Prototype Does NOT Need to Do

- **Real goal-creation logic:** Tapping a template creates a goal that persists; you don't need actual database saves or subsequent reloads. A simple state change showing the goal on the dashboard is sufficient.
- **Real bank account linking:** Assume the user has already linked an account. The prototype starts at "dashboard post-linking; day 1 prompt appears."
- **Real email sending:** Email mockup can be static (Figma screenshot) or an interactive email template mockup. Does not need to integrate with actual email service.
- **User authentication:** Assume user is already logged in. No login flow needed.
- **Real retention data or analytics:** Prototype does not need to show analytics dashboards or simulate 30-day retention measurements.
- **Notification permissions or push notifications:** Day 1 prompt is in-app modal, not push. No need to request notification permissions.
- **Goal-editing UI beyond the affordance:** Showing the edit button is enough; don't need a full edit modal.
- **Network delays or loading states:** Modal appears instantly; no skeleton loaders, spinners, or latency simulation needed.
- **Accessibility features (alt text, ARIA labels):** Nice-to-have; not required for hypothesis testing.

---

## 4. Fidelity Recommendation

**Mid-fi (Clickable Figma Prototype or Interactive HTML/CSS)**

**Justification:** 
This hypothesis is about whether customers *respond to* the prompt (discovery barrier hypothesis) and whether the messaging resonates. The specific interaction quality (scroll behavior, animation timing, button haptics) is not what we're testing. A mid-fi clickable prototype—where users can tap buttons and see state changes—is sufficient to show the core flow and gather feedback on copy, template names, and the two-stage approach (day 1 + day 3–4). A fully built feature in the real app is unnecessary; we need to validate the assumption quickly before engineering builds.

---

## 5. Build Prompt

If building in **Figma** (for static mockup + clickable prototype):

```
## Figma Prototype: Goal-Setting Activation

Build a clickable Figma prototype with the following screens:

### Screen 1: Dashboard (Post-Account-Linking, Day 1)
- Header: "FinWise" logo, user name + avatar on top right
- Main content: Transaction list (use placeholder transactions like "$47.32 Starbucks", "$200 Whole Foods", etc.)
- Small banner at top: "Accounts Linked: 1" (showing the account just linked)
- **Day 1 Modal Overlay (non-dismissible)**:
  - Modal takes up 80% of viewport, centered, white background, rounded corners (8px)
  - Headline: "Set your first goal" (bold, 20px, dark gray)
  - Subheading: "Users who set a goal are 2.6x more likely to stay on track with their finances." (14px, gray, 2-line text)
  - Four equal-width button options below:
    - [Emergency Fund] (blue button, 16px)
    - [Vacation Fund] (blue button, 16px)
    - [Debt Payoff] (blue button, 16px)
    - [Custom Goal] (blue button, 16px)
  - At modal bottom: [Maybe Later] link (14px, gray, underlined)
  - Note: Modal should NOT have a close button (X) in the corner. Only dismissible via buttons.

**Interactions:**
- Clicking any template button (e.g., Emergency Fund):
  - Modal fades out
  - Dashboard reappears
  - New goal "Emergency Fund" appears as a card below the transactions header (see Screen 2)
  - Goal card shows: Goal name, progress bar (empty, 0%), edit button (pencil icon)
- Clicking [Maybe Later]:
  - Modal fades out
  - Dashboard returns without goal created
  - Goal card does NOT appear

### Screen 2: Dashboard (After Goal Creation - Day 1 Happy Path)
- Same as Screen 1 but:
- New goal card appears below transactions header:
  - [Goal] Emergency Fund | Target: Not set | Progress: Empty bar | [Edit pencil icon]
- Transaction list continues below
- Goal card is tappable/clickable (optional for this prototype; not required for hypothesis test)

### Screen 3: Day 3–4 Re-Prompt Modal (Identical to Screen 1 Modal)
- Same modal appears again (user dismissed on day 1, now opening app on day 3)
- Exact same copy, same buttons
- Same interaction behavior (click template = goal created, click Maybe Later = dismiss)
- After dismissing this one, assume it does NOT appear again (so prototype doesn't need a 4th iteration)

### Screen 4: Email Mockup (Static or Interactive, Up to You)
- Email template screenshot or clickable email mockup
- From: FinWise <hello@finwise.app>
- Subject: "The #1 thing successful FinWise users do"
- Email body:
  ```
  Subject: The #1 thing successful FinWise users do

  Users who set goals within the first week report feeling 78% more secure 
  about their finances 3 weeks later. It takes just 30 seconds; we'll help 
  you every step of the way.

  [Set Your First Goal] ← CTA button (blue, 16px)

  — FinWise Team
  ```
- If interactive: clicking [Set Your First Goal] goes to Screen 5 (goal-creation page from email)
- If static: just show as a screenshot; no interaction needed

### Screen 5: Goal-Creation Page (Accessed from Email Link)
- Similar to day 1 modal, but full-screen:
  - Headline: "Set your first goal"
  - Subheading (optional): "You're all set to create a goal. Choose one below or create your own."
  - Same four template buttons: [Emergency Fund] [Vacation Fund] [Debt Payoff] [Custom Goal]
  - Clicking a template creates goal and navigates back to dashboard (Screen 2)

### Interaction Map:
- Screen 1 (Day 1 Modal) → Click template → Screen 2 (Goal created)
- Screen 1 (Day 1 Modal) → Click Maybe Later → Screen 1 (Modal dismisses, no goal)
- Screen 1 → Wait 3 days → Screen 3 (Day 3–4 Re-Prompt, same modal)
- Screen 3 → Click template → Screen 2 (Goal created)
- Screen 3 → Click Maybe Later → Dashboard (no goal, modal dismissed)
- Screen 4 (Email) → Click [Set Your First Goal] → Screen 5 (Email-driven goal creation)
- Screen 5 → Click template → Screen 2 (Goal created)

### Design Notes:
- Use FinWise brand colors (if available in design system). Defaults: Primary blue (#0066CC), backgrounds (#F5F5F5)
- Modal button text should be large enough to tap easily on mobile (16px minimum)
- Modals should feel slightly different from the dashboard to indicate overlay (subtle shadow, 0.5 opacity background behind modal)
- No animations required; simple fade-in/fade-out is fine
- Transaction mockups: use realistic FinWise transaction categories (Groceries, Entertainment, Utilities, etc.)
```

---

## 6. Alternative: If Building in HTML/CSS/JavaScript

```html
<!-- GOAL-SETTING ACTIVATION PROTOTYPE -->
<!-- This is a clickable prototype for testing goal-setting activation hypothesis -->
<!-- Screens: Day 1 Modal, Goal Created Dashboard, Day 3–4 Re-Prompt, Email (static), Email-driven Goal Creation -->

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FinWise - Goal-Setting Activation Prototype</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      background-color: #F5F5F5;
      padding: 0;
    }
    
    .screen {
      display: none;
      width: 100%;
      height: 100vh;
      background-color: #FFFFFF;
    }
    
    .screen.active {
      display: flex;
      flex-direction: column;
    }
    
    /* HEADER */
    .header {
      background-color: #0066CC;
      color: white;
      padding: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .header h1 {
      font-size: 20px;
      font-weight: 600;
    }
    
    .header-right {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background-color: rgba(255,255,255,0.2);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 14px;
    }
    
    /* DASHBOARD CONTENT */
    .dashboard {
      flex: 1;
      overflow-y: auto;
      padding: 16px;
    }
    
    .banner {
      background-color: #E8F4FF;
      border-left: 4px solid #0066CC;
      padding: 12px;
      margin-bottom: 16px;
      border-radius: 4px;
      font-size: 14px;
      color: #003D82;
    }
    
    .goal-card {
      background-color: #F0F8FF;
      border: 1px solid #0099FF;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    
    .goal-card h3 {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 8px;
    }
    
    .goal-progress {
      font-size: 12px;
      color: #666;
      margin-bottom: 8px;
    }
    
    .progress-bar {
      width: 100%;
      height: 6px;
      background-color: #DDD;
      border-radius: 3px;
      overflow: hidden;
    }
    
    .progress-bar-fill {
      height: 100%;
      background-color: #0066CC;
      width: 0%;
    }
    
    .goal-card-right {
      display: flex;
      gap: 8px;
    }
    
    .edit-btn {
      background-color: transparent;
      border: none;
      color: #0066CC;
      font-size: 18px;
      cursor: pointer;
    }
    
    /* TRANSACTIONS */
    .transaction {
      display: flex;
      justify-content: space-between;
      padding: 12px 0;
      border-bottom: 1px solid #EEE;
      font-size: 14px;
    }
    
    .transaction:last-child {
      border-bottom: none;
    }
    
    .transaction-category {
      color: #666;
      font-weight: 500;
    }
    
    .transaction-amount {
      color: #333;
      font-weight: 600;
    }
    
    /* MODAL */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0,0,0,0.5);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    
    .modal-overlay.active {
      display: flex;
    }
    
    .modal {
      background-color: white;
      border-radius: 12px;
      padding: 24px;
      width: 90%;
      max-width: 400px;
      text-align: center;
      box-shadow: 0 10px 40px rgba(0,0,0,0.2);
    }
    
    .modal h2 {
      font-size: 22px;
      font-weight: 600;
      margin-bottom: 12px;
      color: #333;
    }
    
    .modal p {
      font-size: 14px;
      color: #666;
      margin-bottom: 24px;
      line-height: 1.5;
    }
    
    .modal-buttons {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 8px;
      margin-bottom: 16px;
    }
    
    .template-btn {
      background-color: #0066CC;
      color: white;
      border: none;
      padding: 12px 8px;
      border-radius: 6px;
      font-size: 13px;
      font-weight: 600;
      cursor: pointer;
      transition: background-color 0.2s;
    }
    
    .template-btn:hover {
      background-color: #0052A3;
    }
    
    .maybe-later {
      color: #0066CC;
      background: none;
      border: none;
      font-size: 14px;
      cursor: pointer;
      text-decoration: underline;
    }
    
    .maybe-later:hover {
      color: #0052A3;
    }
    
    /* EMAIL MOCKUP */
    .email-container {
      max-width: 600px;
      margin: 40px auto;
      border: 1px solid #DDD;
      border-radius: 4px;
      overflow: hidden;
      background: white;
    }
    
    .email-header {
      background-color: #F5F5F5;
      padding: 16px;
      border-bottom: 1px solid #DDD;
      font-size: 12px;
      color: #666;
    }
    
    .email-body {
      padding: 24px;
      line-height: 1.6;
      color: #333;
    }
    
    .email-body h2 {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 16px;
    }
    
    .email-body p {
      margin-bottom: 16px;
      font-size: 15px;
    }
    
    .email-cta {
      background-color: #0066CC;
      color: white;
      padding: 12px 24px;
      border-radius: 6px;
      text-decoration: none;
      display: inline-block;
      font-weight: 600;
      font-size: 14px;
      margin-bottom: 16px;
      cursor: pointer;
      border: none;
    }
    
    .email-cta:hover {
      background-color: #0052A3;
    }
    
    .email-footer {
      background-color: #F5F5F5;
      padding: 16px;
      border-top: 1px solid #DDD;
      font-size: 12px;
      color: #999;
      text-align: center;
    }
    
    /* NAVIGATION */
    .nav-bar {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      background-color: #F5F5F5;
      padding: 12px;
      border-top: 1px solid #DDD;
      display: flex;
      gap: 8px;
      justify-content: center;
      flex-wrap: wrap;
    }
    
    .nav-btn {
      background-color: #0066CC;
      color: white;
      border: none;
      padding: 8px 16px;
      border-radius: 4px;
      font-size: 12px;
      cursor: pointer;
      font-weight: 600;
    }
    
    .nav-btn:hover {
      background-color: #0052A3;
    }
    
    .nav-btn.secondary {
      background-color: #DDD;
      color: #333;
    }
    
    .nav-btn.secondary:hover {
      background-color: #BBB;
    }
  </style>
</head>
<body>

<!-- SCREEN 1: Day 1 Modal -->
<div class="screen active" id="screen-day1-modal">
  <div class="header">
    <h1>FinWise</h1>
    <div class="header-right">
      <span>Sarah</span>
      <div class="avatar">S</div>
    </div>
  </div>
  <div class="dashboard">
    <div class="banner">📱 Accounts Linked: 1</div>
    <div style="font-size: 12px; color: #999; margin-bottom: 16px;">Recent Transactions</div>
    <div class="transaction">
      <span class="transaction-category">☕ Starbucks</span>
      <span class="transaction-amount">$5.47</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">🛒 Whole Foods</span>
      <span class="transaction-amount">$47.32</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">💡 Electric Bill</span>
      <span class="transaction-amount">$124.99</span>
    </div>
  </div>
  
  <div class="modal-overlay active">
    <div class="modal">
      <h2>Set your first goal</h2>
      <p>Users who set a goal are 2.6x more likely to stay on track with their finances.</p>
      <div class="modal-buttons">
        <button class="template-btn" onclick="handleGoalCreation('Emergency Fund', 'screen-day1-modal', 'screen-goal-created')">Emergency Fund</button>
        <button class="template-btn" onclick="handleGoalCreation('Vacation Fund', 'screen-day1-modal', 'screen-goal-created')">Vacation Fund</button>
        <button class="template-btn" onclick="handleGoalCreation('Debt Payoff', 'screen-day1-modal', 'screen-goal-created')">Debt Payoff</button>
        <button class="template-btn" onclick="handleGoalCreation('Custom Goal', 'screen-day1-modal', 'screen-goal-created')">Custom Goal</button>
      </div>
      <button class="maybe-later" onclick="showScreen('screen-day1-modal', 'screen-day1-dismissed')">Maybe Later</button>
    </div>
  </div>
</div>

<!-- SCREEN 2: Goal Created (Happy Path) -->
<div class="screen" id="screen-goal-created">
  <div class="header">
    <h1>FinWise</h1>
    <div class="header-right">
      <span>Sarah</span>
      <div class="avatar">S</div>
    </div>
  </div>
  <div class="dashboard">
    <div class="banner">✅ Your goal has been created!</div>
    <div id="goal-display" class="goal-card">
      <div>
        <h3 id="goal-name">Emergency Fund</h3>
        <div class="goal-progress">Target: Not set • Progress: Empty</div>
        <div class="progress-bar">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
      <button class="edit-btn" title="Edit goal">✏️</button>
    </div>
    
    <div style="font-size: 12px; color: #999; margin-top: 24px; margin-bottom: 16px;">Recent Transactions</div>
    <div class="transaction">
      <span class="transaction-category">☕ Starbucks</span>
      <span class="transaction-amount">$5.47</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">🛒 Whole Foods</span>
      <span class="transaction-amount">$47.32</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">💡 Electric Bill</span>
      <span class="transaction-amount">$124.99</span>
    </div>
  </div>
</div>

<!-- SCREEN 3: Day 1 Dismissed (No Goal Created) -->
<div class="screen" id="screen-day1-dismissed">
  <div class="header">
    <h1>FinWise</h1>
    <div class="header-right">
      <span>Sarah</span>
      <div class="avatar">S</div>
    </div>
  </div>
  <div class="dashboard">
    <div class="banner">📱 Accounts Linked: 1</div>
    <div style="font-size: 12px; color: #999; margin-bottom: 16px;">Recent Transactions</div>
    <div class="transaction">
      <span class="transaction-category">☕ Starbucks</span>
      <span class="transaction-amount">$5.47</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">🛒 Whole Foods</span>
      <span class="transaction-amount">$47.32</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">💡 Electric Bill</span>
      <span class="transaction-amount">$124.99</span>
    </div>
  </div>
  <div style="padding: 16px; text-align: center; color: #999; font-size: 12px;">
    (Goal was dismissed on day 1. Re-prompt appears on day 3–4...)
  </div>
</div>

<!-- SCREEN 4: Day 3–4 Re-Prompt -->
<div class="screen" id="screen-day3-reprompt">
  <div class="header">
    <h1>FinWise</h1>
    <div class="header-right">
      <span>Sarah</span>
      <div class="avatar">S</div>
    </div>
  </div>
  <div class="dashboard">
    <div class="banner">📱 Accounts Linked: 1</div>
    <div style="font-size: 12px; color: #999; margin-bottom: 16px;">Recent Transactions</div>
    <div class="transaction">
      <span class="transaction-category">☕ Starbucks</span>
      <span class="transaction-amount">$5.47</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">🛒 Whole Foods</span>
      <span class="transaction-amount">$47.32</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">💡 Electric Bill</span>
      <span class="transaction-amount">$124.99</span>
    </div>
  </div>
  
  <div class="modal-overlay active">
    <div class="modal">
      <h2>Set your first goal</h2>
      <p>Users who set a goal are 2.6x more likely to stay on track with their finances.</p>
      <div class="modal-buttons">
        <button class="template-btn" onclick="handleGoalCreation('Emergency Fund', 'screen-day3-reprompt', 'screen-goal-created')">Emergency Fund</button>
        <button class="template-btn" onclick="handleGoalCreation('Vacation Fund', 'screen-day3-reprompt', 'screen-goal-created')">Vacation Fund</button>
        <button class="template-btn" onclick="handleGoalCreation('Debt Payoff', 'screen-day3-reprompt', 'screen-goal-created')">Debt Payoff</button>
        <button class="template-btn" onclick="handleGoalCreation('Custom Goal', 'screen-day3-reprompt', 'screen-goal-created')">Custom Goal</button>
      </div>
      <button class="maybe-later" onclick="showScreen('screen-day3-reprompt', 'screen-day3-dismissed')">Maybe Later</button>
    </div>
  </div>
</div>

<!-- SCREEN 5: Day 3 Dismissed -->
<div class="screen" id="screen-day3-dismissed">
  <div class="header">
    <h1>FinWise</h1>
    <div class="header-right">
      <span>Sarah</span>
      <div class="avatar">S</div>
    </div>
  </div>
  <div class="dashboard">
    <div class="banner">📱 Accounts Linked: 1</div>
    <div style="font-size: 12px; color: #999; margin-bottom: 16px;">Recent Transactions</div>
    <div class="transaction">
      <span class="transaction-category">☕ Starbucks</span>
      <span class="transaction-amount">$5.47</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">🛒 Whole Foods</span>
      <span class="transaction-amount">$47.32</span>
    </div>
    <div class="transaction">
      <span class="transaction-category">💡 Electric Bill</span>
      <span class="transaction-amount">$124.99</span>
    </div>
  </div>
  <div style="padding: 16px; text-align: center; color: #999; font-size: 12px;">
    (Goal was dismissed on day 3–4. Day 5 email is sent this evening...)
  </div>
</div>

<!-- SCREEN 6: Day 5 Email Mockup -->
<div class="screen" id="screen-email">
  <div class="header">
    <h1>Email Prototype</h1>
  </div>
  <div class="dashboard">
    <div class="email-container">
      <div class="email-header">
        <strong>From:</strong> FinWise &lt;hello@finwise.app&gt;<br>
        <strong>Subject:</strong> The #1 thing successful FinWise users do<br>
        <strong>Date:</strong> Day 5 after signup
      </div>
      <div class="email-body">
        <h2>The #1 thing successful FinWise users do</h2>
        <p>Users who set goals within the first week report feeling 78% more secure about their finances 3 weeks later. It takes just 30 seconds; we'll help you every step of the way.</p>
        <button class="email-cta" onclick="showScreen('screen-email', 'screen-email-landing')">Set Your First Goal</button>
        <p style="font-size: 13px; color: #666; margin-top: 16px;">We're here to help every step of the way.</p>
        <p style="font-size: 13px; color: #666;">— The FinWise Team</p>
      </div>
      <div class="email-footer">
        FinWise, Inc. | support@finwise.app | www.finwise.app
      </div>
    </div>
  </div>
</div>

<!-- SCREEN 7: Email Landing Page (Goal Creation from Email Link) -->
<div class="screen" id="screen-email-landing">
  <div class="header">
    <h1>FinWise</h1>
  </div>
  <div class="dashboard" style="display: flex; align-items: center; justify-content: center; flex-direction: column; text-align: center;">
    <div class="modal" style="position: static; box-shadow: none; width: 100%; max-width: 400px;">
      <h2>Set your first goal</h2>
      <p>You clicked the email link. Now create your goal:</p>
      <div class="modal-buttons">
        <button class="template-btn" onclick="handleGoalCreation('Emergency Fund', 'screen-email-landing', 'screen-email-goal-created')">Emergency Fund</button>
        <button class="template-btn" onclick="handleGoalCreation('Vacation Fund', 'screen-email-landing', 'screen-email-goal-created')">Vacation Fund</button>
        <button class="template-btn" onclick="handleGoalCreation('Debt Payoff', 'screen-email-landing', 'screen-email-goal-created')">Debt Payoff</button>
        <button class="template-btn" onclick="handleGoalCreation('Custom Goal', 'screen-email-landing', 'screen-email-goal-created')">Custom Goal</button>
      </div>
    </div>
  </div>
</div>

<!-- SCREEN 8: Email Goal Created -->
<div class="screen" id="screen-email-goal-created">
  <div class="header">
    <h1>FinWise</h1>
  </div>
  <div class="dashboard">
    <div class="banner">✅ Goal created from email link!</div>
    <div id="goal-display-email" class="goal-card">
      <div>
        <h3 id="goal-name-email">Emergency Fund</h3>
        <div class="goal-progress">Target: Not set • Progress: Empty</div>
        <div class="progress-bar">
          <div class="progress-bar-fill"></div>
        </div>
      </div>
      <button class="edit-btn" title="Edit goal">✏️</button>
    </div>
    <div style="padding: 16px; text-align: center; color: #666; font-size: 13px; margin-top: 24px;">
      You've successfully set your first goal. Check in on your progress anytime.
    </div>
  </div>
</div>

<!-- NAVIGATION -->
<div class="nav-bar">
  <button class="nav-btn" onclick="showScreen(null, 'screen-day1-modal')">1. Day 1 Modal</button>
  <button class="nav-btn" onclick="showScreen(null, 'screen-day1-dismissed')">2a. Day 1 → Dismissed</button>
  <button class="nav-btn" onclick="showScreen(null, 'screen-day3-reprompt')">2b. Day 3 Re-Prompt</button>
  <button class="nav-btn" onclick="showScreen(null, 'screen-email')">3. Day 5 Email</button>
  <button class="nav-btn" onclick="showScreen(null, 'screen-email-landing')">4. Email Goal Creation</button>
</div>

<script>
  function showScreen(fromScreen, toScreen) {
    // Hide all screens
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    // Show target screen
    document.getElementById(toScreen).classList.add('active');
  }
  
  function handleGoalCreation(goalName, fromScreen, toScreen) {
    // Update goal name for display
    if (document.getElementById('goal-name')) {
      document.getElementById('goal-name').textContent = goalName;
    }
    if (document.getElementById('goal-name-email')) {
      document.getElementById('goal-name-email').textContent = goalName;
    }
    // Navigate to goal created screen
    showScreen(fromScreen, toScreen);
  }
</script>

</body>
</html>
```

Save as `finwise-goal-setting-prototype.html` and open in a browser to test.

---

## 7. Obvious Objections

1. **"Is the 2.6x churn difference real, or is it confounded by other variables?"**
   - *Objection:* Maybe accounts that set goals are just more engaged overall; they'd retain better anyway.
   - *Answer:* The effect holds when we control for acquisition channel and user segment. Goal-setters in all segments outperform non-setters. However, this is still correlational, not causal. The prototype tests whether *prompting* drives goal creation; if 15%+ of prompted users create goals (vs. 5% baseline), that's evidence the feature matters.
   - *How to close it:* Run the experiment and measure both goal creation and retention lift at 30 days. If retention doesn't improve alongside goal creation, the correlation was confounded.

2. **"Won't a non-dismissible modal on day 1 annoy users or cause uninstalls?"**
   - *Objection:* Users hate being forced; a hard modal could trigger app abandonment.
   - *Answer:* Non-dismissible modals are standard in high-engagement apps (Slack, Instagram) for critical flows. The "Maybe Later" button provides an exit; users aren't trapped. However, day 1 timing is aggressive. If day 1 churn spikes >1% (measured via rollout monitoring), we'll soften to day 2 or add a close button.
   - *How to close it:* Monitor churn for day 1 cohort during rollout. If worse than control, revert and test day 2 timing instead.

3. **"Won't the email follow-up on day 5 cannibalize app adoption?"**
   - *Objection:* If users set goals from email, they bypass the app onboarding and never learn the full interface.
   - *Answer:* Email link lands on goal-creation page (still in-app), so users see the app interface. Secondary benefit: users who never open the app are hard to retain anyway; email is a last-ditch effort. It's not cannibalization; it's recovery.
   - *How to close it:* Measure subsequent app engagement for users who create goals from email vs. in-app. If email users show lower week-2 engagement, add in-app onboarding step after email goal creation.

4. **"Only 19% of accounts set goals today, but you're only targeting new signups (day 1–5). What about the 1,460 existing non-goal-setters?"**
   - *Objection:* The hypothesis addresses new user activation, not reactivation of existing dormant accounts. That's 81% of the problem!
   - *Answer:* Correct. Phase 1 is new user activation (day 1–5). Phase 2 will address existing accounts (in-app prompt for users with 30+ days no goal, email reactivation campaigns). This PRD focuses on Phase 1 to maximize the leverage point (earliest friction).
   - *How to close it:* After Phase 1 validation, design Phase 2 for existing accounts.

5. **"How do you know the 78% security stat is real? That sounds made up."**
   - *Objection:* The "78% more secure" benefit in the email is unvalidated. Is it from data, or is it marketing copy?
   - *Answer:* Current hypothesis: it's a plausible benefit based on the core job (reduce financial anxiety), not validated data yet. If the stat isn't from research, it's a hypothesis to test in customer conversations during prototype testing. Success metric: does this copy drive email CTR ≥20%? If not, A/B test alternative benefits.
   - *How to close it:* During prototype customer interviews, ask "Does this resonates? Have you felt this way?" Refine copy based on feedback before Phase 1 launch.

6. **"What's the revenue impact if users who create goals still churn at month 3?"**
   - *Objection:* Goal-creation is a leading indicator, but if retention at 90 days doesn't improve, the investment isn't worth it.
   - *Answer:* Fair. Phase 1 measures 30-day retention (leading indicator); Phase 2 measures 90-day retention (business metric). If 30-day lift is +2–4pp but 90-day churn stays flat, goal-setting alone isn't enough; we'll layer in additional mechanisms (e.g., goal progress push notifications, goal-based spending insights).
   - *How to close it:* Phase 1 should show 30-day lift. If it does, run Phase 2 to measure 90-day impact.

---

## 8. Customer Conversation Guide

### Setup (Tell the Customer)

"Thanks for taking the time to chat with us. We're testing a new way to help FinWise users get more value out of the app right when they sign up. After you link your first bank account, the app will suggest setting a financial goal—things like emergency funds or saving for a vacation. We want to understand if this feels helpful or if it gets in the way. There are no wrong answers. What matters is your honest reaction."

### Task 1: Reviewing the Day 1 Modal (In-App)

**Prompt:** "Imagine you just linked your first bank account to FinWise. You tap back to see your transactions, and this modal appears. Take a moment and tell me what you're thinking."

- Let them read the copy naturally
- Observe: Do they read the benefit ("2.6x more likely...")? Do they hesitate?
- Ask: "What does that stat mean to you? Does it feel credible?"
- Ask: "Would you click one of these templates, or would you dismiss it?"
- Ask (if they dismiss): "Why wouldn't you set a goal right now?"

**Expected behavior (validates hypothesis):** User clicks a template without hesitation. Says something like "Yeah, I should set one of these" or "This is helpful, I wasn't thinking about it until I saw this." → Signals discovery was the barrier.

**Red flag (falsifies hypothesis):** User dismisses immediately and says "I don't want to be nagged" or "Goals feel overwhelming." → Signals rejection, not discovery.

### Task 2: Reviewing the Day 3–4 Re-Prompt (Same Modal, Second Time)

**Prompt:** "You dismiss the first prompt and skip forward 3 days. You open the app again, and the same prompt appears. What do you think?"

- Observe: Annoyance? Or second chance appreciation?
- Ask: "Would you be frustrated to see this again, or does it feel like a gentle reminder?"
- Ask: "If you were going to create a goal, when would feel right? Day 1, or would you rather wait?"

**Expected behavior:** "It's a good reminder" or "Day 1 felt too soon, day 3 feels better." → Validates two-touch approach.

**Red flag:** "This is annoying, please stop" → Suggests re-prompt is too aggressive.

### Task 3: Reviewing the Day 5 Email

**Prompt:** "You still haven't created a goal. You receive this email on day 5 (show email mockup). What's your reaction?"

- Observe: Do they read the benefit copy? ("78% more secure...")
- Ask: "Do you feel like FinWise understands you after reading this?"
- Ask: "Would you click the link to set a goal from the email, or would you ignore it?"
- Ask: "The copy says 'we'll help you every step.' Does that feel reassuring?"

**Expected behavior:** User clicks link. Says "Yeah, this makes me want to set a goal" or "I like that it's quick and they offer help." → Validates email follow-up + reassurance messaging.

**Red flag:** User dismisses or says the email feels desperate/manipulative. → Suggests messaging needs work.

### Hypothesis-Specific Questions

1. **On benefit messaging:** "If the email didn't mention the benefit (feeling more secure), would you still click to set a goal? What made you want to?"
   - *Why:* Tests whether benefit messaging is driving action or if the prompt itself is sufficient.

2. **On discovery vs. rejection:** "Before this prototype, did you know FinWise had savings goals? Or is this the first time you're seeing it?"
   - *Why:* Validates whether the problem is truly discovery (users didn't know) vs. rejection (they knew but didn't want it).

3. **On goal relevance:** "When you set the goal (or if you set one), did you pick one that actually matches what you're saving for? Or did it feel generic?"
   - *Why:* Tests whether templates match real user intent or if custom goal creation would be needed.

### What a Successful Session Looks Like

A successful session shows:
- User reads the day 1 modal and either creates a goal or dismisses with a genuine reason ("I want to think about what I'm saving for first")
- User reacts to the day 3 re-prompt as a helpful reminder, not an annoyance
- User engages with the email, reads the benefit copy, and either clicks the CTA or gives a thoughtful reason for not clicking
- User confirms they didn't know about goals before this (discovery hypothesis) OR they knew but now feel motivated by the prompts (belief change)
- User says the reassurance messaging ("we'll help you every step") feels genuine, not sales-y

A failing session shows:
- User dismisses all prompts immediately without reading copy
- User says "This feels pushy" or "I hate non-dismissible modals"
- User doesn't read or believe the 78% benefit stat
- User says "I don't want to set goals; this isn't for me" (rejection hypothesis invalidates activation hypothesis)

---

*Prototype Brief complete. Ready for designer/builder implementation.*
