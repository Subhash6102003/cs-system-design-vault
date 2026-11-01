================================================================================
  FILE 065: FRONTEND TESTING
  Section: E - Frontend Development
================================================================================

────────────────────────────────────────────────────────────────────────────────
  1. OVERVIEW
────────────────────────────────────────────────────────────────────────────────

  Frontend Testing: Unit, Component, and End-to-End

  Testing frontend code used to be notoriously difficult, resulting in flaky tests and frustrated developers. Today, modern tooling makes testing robust and confidence-inspiring. This module covers the testing pyramid specifically for the frontend. You will learn Unit Testing with Jest, Component Testing with React Testing Library (focusing on accessible querying), and End-to-End (E2E) testing with Cypress/Playwright. Mastering these tools ensures that your refactors don't break production and that your UI remains accessible.

  Prerequisites: JavaScript ES6+, React Fundamentals, and a basic understanding of DOM nodes.

────────────────────────────────────────────────────────────────────────────────
  2. KEY TERMINOLOGY
────────────────────────────────────────────────────────────────────────────────

  The Testing Pyramid
    1. Unit Tests (Many, Fast): Testing isolated pure functions (e.g., helpers, reducers).
    2. Integration/Component Tests (Medium): Testing components rendering and interacting with each other.
    3. E2E Tests (Few, Slow, High Confidence): Spinning up a real browser to simulate user journeys from login to checkout.

  Jest
    A popular JavaScript testing framework. Provides the test runner, assertion library (expect), and mocking capabilities (jest.fn()).

  React Testing Library (RTL)
    A library for testing React components. Its core philosophy: The more your tests resemble the way your software is used, the more confidence they can give you. (Avoid testing internal state; test the DOM output).

  Accessible Queries
    RTL encourages querying the DOM exactly how a user/screen reader finds elements: getByRole, getByLabelText, getByText.

  Mocking
    Replacing real dependencies (like an API call fetch or a heavy child component) with controlled fake versions to isolate the test.

  Snapshot Testing
    Capturing a serialized version of the UI and comparing it in future test runs to detect unexpected UI changes. (Use sparingly, often leads to fatigue).

  Cypress / Playwright
    Modern E2E testing tools. They control an actual Chromium/Firefox/Webkit browser, intercept network requests, and execute real clicks and typing.

  Test-Driven Development (TDD)
    Writing the test before writing the implementation code.

  Code Coverage
    A metric showing the percentage of source code executed during the test suite (Lines, Functions, Branches).

────────────────────────────────────────────────────────────────────────────────
  3. DIAGRAMS & VISUAL MODELS
────────────────────────────────────────────────────────────────────────────────

  The RTL Query Priority
  RTL provides many ways to find an element, but you should prioritize them in this order to ensure accessibility:

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    1. Accessibility Queries (BEST)                                      │
  │       - getByRole('button', { name: /submit/i })                        │
  │       - getByLabelText('Username')                                      │
  │                                                                         │
  │    2. Semantic Queries                                                  │
  │       - getByPlaceholderText('Search...')                               │
  │       - getByText('Welcome back')                                       │
  │                                                                         │
  │    3. Test ID (WORST, fallback only)                                    │
  │       - getByTestId('custom-div')                                       │
  └─────────────────────────────────────────────────────────────────────────┘

  The Component Testing Flow

  ┌─────────────────────────────────────────────────────────────────────────┐
  │    [ Arrange ]                                                          │
  │    Render Component with specific Props/Mock Providers                  │
  │         |                                                               │
  │    [ Act ]                                                              │
  │    Find Element (getByRole) -> Simulate Event (userEvent.click)         │
  │         |                                                               │
  │    [ Assert ]                                                           │
  │    Check DOM State (expect(element).toBeInTheDocument())                │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  5. DEMO CODE
────────────────────────────────────────────────────────────────────────────────

  Unit Test (Jest)
  Testing a pure function reducer.

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // math.js                                                             │
  │  export const calculateTotal = (items, taxRate) => {                    │
  │    if (!items.length) return 0;                                         │
  │    const subtotal = items.reduce((sum, item) => sum + item.price, 0);   │
  │    return subtotal + (subtotal * taxRate);                              │
  │  };                                                                     │
  │                                                                         │
  │  // math.test.js                                                        │
  │  import { calculateTotal } from './math';                               │
  │                                                                         │
  │  describe('calculateTotal', () => {                                     │
  │    it('returns 0 for empty array', () => {                              │
  │      expect(calculateTotal([], 0.1)).toBe(0);                           │
  │    });                                                                  │
  │                                                                         │
  │    it('calculates total with tax correctly', () => {                    │
  │      const items = [{ price: 100 }, { price: 50 }];                     │
  │      expect(calculateTotal(items, 0.1)).toBe(165); // 150 + 15          │
  │    });                                                                  │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

  Component Test (React Testing Library)

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // LoginForm.jsx                                                       │
  │  import { useState } from 'react';                                      │
  │                                                                         │
  │  export const LoginForm = ({ onSubmit }) => {                           │
  │    const [user, setUser] = useState('');                                │
  │                                                                         │
  │    return (                                                             │
  │      <form onSubmit={(e) => { e.preventDefault(); onSubmit(user); }}>   │
  │        <label htmlFor="username">Username</label>                       │
  │        <input id="username" value={user} onChange={e => setUser(e.target.value)} />│
  │        <button type="submit">Login</button>                             │
  │      </form>                                                            │
  │    );                                                                   │
  │  };                                                                     │
  │                                                                         │
  │  // LoginForm.test.jsx                                                  │
  │  import { render, screen } from '@testing-library/react';               │
  │  import userEvent from '@testing-library/user-event';                   │
  │  import { LoginForm } from './LoginForm';                               │
  │                                                                         │
  │  test('submits the form with the typed username', async () => {         │
  │    // 1. Arrange                                                        │
  │    const mockSubmit = jest.fn(); // Create a mock function              │
  │    render(<LoginForm onSubmit={mockSubmit} />);                         │
  │                                                                         │
  │    // Setup userEvent (more realistic than fireEvent)                   │
  │    const user = userEvent.setup();                                      │
  │                                                                         │
  │    // 2. Act                                                            │
  │    const input = screen.getByLabelText(/username/i);                    │
  │    await user.type(input, 'adminuser');                                 │
  │                                                                         │
  │    const submitButton = screen.getByRole('button', { name: /login/i }); │
  │    await user.click(submitButton);                                      │
  │                                                                         │
  │    // 3. Assert                                                         │
  │    expect(mockSubmit).toHaveBeenCalledTimes(1);                         │
  │    expect(mockSubmit).toHaveBeenCalledWith('adminuser');                │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  6. PRODUCTION CODE
────────────────────────────────────────────────────────────────────────────────

  Cypress E2E Test (Authentication Flow)
  E2E tests run in a real browser. Here, we test a login flow and intercept the network request to mock the backend response, preventing our tests from relying on an actual database.

  [Language: Javascript]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  // cypress/e2e/login.cy.js                                             │
  │                                                                         │
  │  describe('Authentication Flow', () => {                                │
  │                                                                         │
  │    beforeEach(() => {                                                   │
  │      // Navigate to the app before each test                            │
  │      cy.visit('/login');                                                │
  │    });                                                                  │
  │                                                                         │
  │    it('shows error on invalid credentials', () => {                     │
  │      // Intercept API call and force a 401 Unauthorized response        │
  │      cy.intercept('POST', '/api/auth/login', {                          │
  │        statusCode: 401,                                                 │
  │        body: { error: 'Invalid credentials' }                           │
  │      }).as('loginRequest');                                             │
  │                                                                         │
  │      // Type into inputs (using robust data-cy attributes or roles)     │
  │      cy.get('input[name="email"]').type('wrong@email.com');             │
  │      cy.get('input[name="password"]').type('badpassword');              │
  │      cy.get('button[type="submit"]').click();                           │
  │                                                                         │
  │      // Wait for the intercepted request to finish                      │
  │      cy.wait('@loginRequest');                                          │
  │                                                                         │
  │      // Assert that the UI displays the error                           │
  │      cy.contains('Invalid credentials').should('be.visible');           │
  │    });                                                                  │
  │                                                                         │
  │    it('logs in successfully and redirects to dashboard', () => {        │
  │      // Intercept and force a 200 Success response                      │
  │      cy.intercept('POST', '/api/auth/login', {                          │
  │        statusCode: 200,                                                 │
  │        body: { token: 'fake-jwt-token', user: { name: 'Alice' } }       │
  │      }).as('loginSuccess');                                             │
  │                                                                         │
  │      cy.get('input[name="email"]').type('alice@example.com');           │
  │      cy.get('input[name="password"]').type('correcthorse');             │
  │      cy.get('button[type="submit"]').click();                           │
  │                                                                         │
  │      cy.wait('@loginSuccess');                                          │
  │                                                                         │
  │      // Assert URL changed                                              │
  │      cy.url().should('include', '/dashboard');                          │
  │      // Assert UI updated                                               │
  │      cy.contains('Welcome back, Alice').should('be.visible');           │
  │                                                                         │
  │      // Check if token was saved to local storage                       │
  │      cy.window().its('localStorage.token').should('eq', 'fake-jwt-token');│
  │    });                                                                  │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

────────────────────────────────────────────────────────────────────────────────
  7. INTERVIEW QUESTIONS
────────────────────────────────────────────────────────────────────────────────

  Q1: What is the philosophy of React Testing Library (RTL)?

  ANSWER:
    "The more your tests resemble the way your software is used, the more confidence they can give you." RTL actively prevents you from testing implementation details (like reading a component's internal useState values) and forces you to test what the user actually sees and interacts with in the DOM.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q2: Why is getByRole preferred over getByTestId?

  ANSWER:
    getByRole ensures your component is accessible. If you use getByRole('button') and it passes, you know screen readers will recognize it as a button. getByTestId is opaque; it doesn't guarantee the user can actually use or understand the element.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q3: Explain the difference between Unit, Integration, and E2E tests.

  ANSWER:
    Unit tests check small isolated pieces of logic (like a math function). Integration tests check how multiple units work together (like a React component rendering with a Redux provider). E2E tests load the entire application in a real browser and simulate an actual user journey.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q4: What is a Mock and when do you use it?

  ANSWER:
    A mock is a fake implementation of a dependency. You use it when you don't want a test to reach out to the real world (e.g., mocking fetch so you don't actually hit a database during a component test, keeping tests fast and deterministic).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q5: What is the difference between queryBy, getBy, and findBy in RTL?

  ANSWER:
    - getBy: Returns the element, throws an error if NOT found. (Used to assert existence).
    - queryBy: Returns the element or null if NOT found. (Used to assert an element is missing).
    - findBy: Returns a Promise. (Used for asynchronous elements that will appear after a fetch or timeout).

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q6: Why is Snapshot Testing sometimes considered controversial?

  ANSWER:
    Snapshots easily become brittle. If you change a CSS class, the snapshot fails. Developers often get "snapshot fatigue" and just blindly press u to update failing snapshots without reviewing them, rendering the tests useless.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q7: What is the difference between fireEvent and userEvent in RTL?

  ANSWER:
    fireEvent dispatches a single DOM event. userEvent simulates full user interactions (e.g., userEvent.type() will trigger focus, keydown, keypress, keyup, input, and change events exactly like a real keyboard). userEvent is highly preferred.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q8: How do you test a component that requires React Context (like Redux or a ThemeProvider)?

  ANSWER:
    You create a custom render function that wraps the component under test inside the necessary Providers before rendering it.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q9: What does "flaky test" mean and what causes them in E2E testing?

  ANSWER:
    A flaky test is one that passes sometimes and fails others without any code changes. In E2E, this is usually caused by relying on arbitrary sleep() timeouts instead of explicitly waiting for elements to appear in the DOM or waiting for specific network requests to resolve.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  Q10: What is Code Coverage and is 100% coverage a good goal?

  ANSWER:
    Coverage measures how many lines/branches of code were executed during tests. While a good metric, chasing 100% is often an anti-pattern. It leads to developers writing meaningless tests just to satisfy the metric, rather than testing critical user flows.

────────────────────────────────────────────────────────────────────────────────
  8. RIDDLES & DEBUGGING CHALLENGES
────────────────────────────────────────────────────────────────────────────────

  CHALLENGE 1: The Asynchronous Trap

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  test('shows success message after submit', () => {                     │
  │    render(<SubmitForm />);                                              │
  │    userEvent.click(screen.getByRole('button', { name: /submit/i }));    │
  │                                                                         │
  │    // Submit triggers an async API call, then shows "Success"           │
  │    expect(screen.getByText('Success')).toBeInTheDocument();             │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? The assertion runs synchronously immediately after the click. Because the API call is asynchronous, the "Success" text isn't in the DOM yet, so getByText throws an error.
    Fix: Use await screen.findByText('Success') and make the test callback async.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 2: The Silent Failure

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  test('modal does not exist initially', () => {                         │
  │    render(<App />);                                                     │
  │    expect(screen.getByTestId('modal')).not.toBeInTheDocument();         │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? getByTestId throws a fatal error if the element is not found, immediately failing and crashing the test before it even reaches the expect assertion.
    Fix: Use queryByTestId (which returns null instead of throwing): expect(screen.queryByTestId('modal')).toBeNull();.

  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─

  CHALLENGE 3: Internal State Testing

  [Language: Jsx]

  ┌─────────────────────────────────────────────────────────────────────────┐
  │  test('counter increments', () => {                                     │
  │    const { component } = render(<Counter />);                           │
  │                                                                         │
  │    // Trying to read the internal useState value                        │
  │    expect(component.state.count).toBe(0);                               │
  │  });                                                                    │
  └─────────────────────────────────────────────────────────────────────────┘

  SOLUTION:
    What's wrong? This is the old way (Enzyme philosophy). RTL does not allow you to access a functional component's internal state. You should not care about the variable count. You should care about what the DOM shows.
    Fix: expect(screen.getByText('0')).toBeInTheDocument();.

────────────────────────────────────────────────────────────────────────────────
  9. WHY THIS MATTERS IN PRODUCTION
────────────────────────────────────────────────────────────────────────────────

  1. Refactoring Confidence: Without tests, upgrading React versions or switching state management libraries is terrifying. With a solid test suite, you can rewrite the entire underlying architecture; if the tests pass, you know the user experience hasn't changed.
  2. Preventing Regressions: Bugs often reappear. When a bug is fixed, writing a test to simulate that exact bug ensures it can never be accidentally reintroduced into the production codebase.
  3. Accessibility (a11y): Using RTL forces you to build accessible UIs. If you can't select an element with getByRole, a blind user using a screen reader can't find it either.

────────────────────────────────────────────────────────────────────────────────
  10. CROSS-REFERENCES
────────────────────────────────────────────────────────────────────────────────

  -> File 058: React Fundamentals (Understanding the DOM output that you are actually testing.)
  -> File 056: JavaScript Async (Understanding how to mock and await asynchronous fetch calls in tests.)
  -> File 060: React StateManagement (Testing components that rely on global Context or Redux providers.)

================================================================================
  END OF FILE 065
================================================================================
