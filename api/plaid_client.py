import os
from datetime import datetime, timedelta

# Try to import Plaid, but handle gracefully if not configured
try:
    import plaid
    from plaid.api import plaid_api
    from plaid.model.transactions_get_request import TransactionsGetRequest
    from plaid.model.accounts_get_request import AccountsGetRequest
    from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
    from plaid.model.link_token_create_request import LinkTokenCreateRequest
    from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
    from plaid.model.country_code import CountryCode
    from plaid.model.products import Products
    from plaid.configuration import Configuration
    from plaid.api_client import ApiClient
    PLAID_AVAILABLE = True
except ImportError:
    PLAID_AVAILABLE = False

class PlaidClient:
    def __init__(self):
        self.client_id = os.environ.get('PLAID_CLIENT_ID')
        self.secret = os.environ.get('PLAID_SECRET')
        self.env = os.environ.get('PLAID_ENV', 'sandbox')
        self.client = None
        
        # Only initialize if we have credentials and Plaid is available
        if PLAID_AVAILABLE and self.client_id and self.secret and self.client_id != 'demo-client-id':
            try:
                # Configure Plaid client
                env_mapping = {
                    'sandbox': plaid.Environment.sandbox,
                    'development': plaid.Environment.development,
                    'production': plaid.Environment.production
                }
                
                configuration = Configuration(
                    host=env_mapping.get(self.env, plaid.Environment.sandbox),
                    api_key={
                        'clientId': self.client_id,
                        'secret': self.secret
                    }
                )
                api_client = ApiClient(configuration)
                self.client = plaid_api.PlaidApi(api_client)
            except Exception as e:
                print(f"Warning: Could not initialize Plaid client: {e}")
                self.client = None
    
    def create_link_token(self, user_id):
        """Create a link token for Plaid Link"""
        if not self.client:
            print("Plaid client not initialized. Please set up your Plaid credentials.")
            return None
            
        try:
            request = LinkTokenCreateRequest(
                products=[Products('transactions')],
                client_name="Finance Mentor AI",
                country_codes=[CountryCode('US')],
                language='en',
                user=LinkTokenCreateRequestUser(client_user_id=str(user_id))
            )
            response = self.client.link_token_create(request)
            return response['link_token']
        except Exception as e:
            print(f"Error creating link token: {e}")
            return None
    
    def exchange_public_token(self, public_token):
        """Exchange public token for access token"""
        if not self.client:
            raise Exception("Plaid client not initialized. Please set up your Plaid credentials.")
            
        try:
            request = ItemPublicTokenExchangeRequest(public_token=public_token)
            response = self.client.item_public_token_exchange(request)
            return response['access_token']
        except Exception as e:
            print(f"Error exchanging public token: {e}")
            raise e
    
    def get_accounts(self, access_token):
        """Get account information"""
        if not self.client:
            raise Exception("Plaid client not initialized. Please set up your Plaid credentials.")
            
        try:
            request = AccountsGetRequest(access_token=access_token)
            response = self.client.accounts_get(request)
            
            accounts = []
            for account in response['accounts']:
                accounts.append({
                    'account_id': account['account_id'],
                    'name': account['name'],
                    'type': account['type'],
                    'subtype': account['subtype'],
                    'balances': {
                        'current': account['balances']['current'],
                        'available': account['balances']['available']
                    }
                })
            
            return accounts
        except Exception as e:
            print(f"Error getting accounts: {e}")
            raise e
    
    def get_transactions(self, access_token, start_date=None, end_date=None, count=500):
        """Get transactions for an account"""
        if not self.client:
            raise Exception("Plaid client not initialized. Please set up your Plaid credentials.")
            
        try:
            if not start_date:
                start_date = datetime.now() - timedelta(days=365)
            if not end_date:
                end_date = datetime.now()
            
            request = TransactionsGetRequest(
                access_token=access_token,
                start_date=start_date.date(),
                end_date=end_date.date(),
                count=count
            )
            
            response = self.client.transactions_get(request)
            
            transactions = []
            for transaction in response['transactions']:
                transactions.append({
                    'transaction_id': transaction['transaction_id'],
                    'account_id': transaction['account_id'],
                    'amount': transaction['amount'],
                    'date': transaction['date'],
                    'name': transaction['name'],
                    'merchant_name': transaction.get('merchant_name'),
                    'category': transaction['category'][0] if transaction['category'] else 'Other',
                    'subcategory': transaction['category'][1] if len(transaction['category']) > 1 else None
                })
            
            return transactions
        except Exception as e:
            print(f"Error getting transactions: {e}")
            raise e
    
    def get_account_balance(self, access_token, account_id):
        """Get current balance for a specific account"""
        if not self.client:
            print("Plaid client not initialized. Please set up your Plaid credentials.")
            return None
            
        try:
            accounts = self.get_accounts(access_token)
            for account in accounts:
                if account['account_id'] == account_id:
                    return account['balances']['current']
            return None
        except Exception as e:
            print(f"Error getting account balance: {e}")
            return None