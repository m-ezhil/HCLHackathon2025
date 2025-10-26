# Smart Bank - Modular Banking Backend System


## Account Creation
### Open Endpoints
Open endpoints require no Authentication.

#### Login (Post): `/auth/login`
##### Negative Test Scenarios:
- Invalid email or password

#### Register (Post): `/auth/signup`
##### Negative Test Scenarios:
- Password Validation
- Email Validation
- PAN No Validation
- Email already exists
- PAN No already exists

### Enpoints that required Authentication
#### Account Creation (Post): `/account/create`
##### Negative Test Scenarios
- Account type already exists for this customer
- Initial deposit must be greater than or equal to zero
- Invalid account type
- Token has expired
- Invalid token

#### Amount Deposit (Post): `/trans/create`
##### Negative Test Scenarios
- Amount must be greater than zero
- Invalid transaction type. Must be 'WITHDRAW' or 'DEPOSIT'.
- Account not found
- Token has expired
- Invalid token

## Database Design
### Customer
- ID: int - PK
- Name: string
- Email: string
- Password: string
- PAN No: string - UK
- Create at: datetime

### Account
- ID: int - PK
- Customer ID: int - FK(Customer.ID)
- Account No: string
- Account Type: string
- Balance: int
- Create at: datetime

### Transaction
- ID: int - PK
- Transaction ID: string
- Account ID: int - FK(Account.ID)
- Transaction Type: string - Possible values [WITHDRAW, DEPOSIT]
- Amount: int
- Create at: datetime


